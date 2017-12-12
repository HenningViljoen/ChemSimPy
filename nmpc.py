from baseclass import baseclass
import globe as globe
import utilities as utilities
from mpcvar import mpcvar
from simulation import simulation
from point import point
from nmpcproperties import nmpcproperties
from nmpcrlsnapshot import nmpcrlsnapshot
from sklearn.neural_network import MLPRegressor
import sys
import numpy as np
import random
from particle import particle
import math
import copy


class nmpc(baseclass):

    #//public List<mpcvar> mvsim0; //This List needs to point to sim0
    #//public List<mpcvar> mvsim1; //This List needs to point to sim1;

    

    #//public double J; //Last objective function run value.

    #//properties for the Interior point 1 ConstrainedLineSearch algorithm ------------------------------------------------------------------------------------------

    #//Properties for the Active Set algorithm 1. -------------------------------------------------------------------------------------------------

    #//public matrix fullconstraintvectoractiveset1; //The total constraint vector with rows zero for ones that are not in the problem.

    def __init__(self, anr, ax, ay, asim):
            #public nmpc(int anr, double ax, double ay, simulation asim) : base(anr, ax, ay)
        super(nmpc, self).__init__(anr, ax, ay)
        self.objecttype = globe.objecttypes.NMPC

        self.name = 'NMPC ' + str(self.nr)

        self.algorithm = globe.DefaultNMPCAlgorithm #The NMPC algorithm that will be used in this controller

        self.callingsimi = 0  #The simulation index in the calling simulation object.
        self.controlleri = -1 #The number of times that the controller has executed.
        self.cvmaster = list() #public List<mpcvar> cvmaster; //This List needs to point to mastersim
        #//mvsim0 = new List<mpcvar>();
        #//mvsim1 = new List<mpcvar>();
        self.mvmaster = list()  # List<mpcvar>()  The master sim's mapping should be to this list.
        self.mvboolmaster = list() #List<mpcvar>().  The master sim's boolean mpc variables will be stored here.  
                                            #This is to enable hybrid nmpc.
        self.systemhasbool = 0 #True (1) if there are boolean mvs in the system.
        self.N = globe.DefaultN  #Optimisation horizon
        self.initialdelay = globe.DefaultInitialDelay #The amount of iterations of the total simulation from T0 to the first execution of nmpc.
        self.runinterval = globe.DefaultRunInterval #The amount of iterations of the total simulation between runs of the NMPC.
        self.controllerhistorylength = int(globe.SimIterations/self.runinterval)
        self.mastersim = asim #simulation object.  This will be copied from the master sim each time update method is run initiated
    
        self.sim0 = simulation() #pointers (sim0 and sim1) to the main simulation will need to be maintained in the NMPC in order to run the 
                               #simulateplant method from within this class.  sim0 will move with update method, and sim1 will 
                               #move with each J calc.
        self.sim0.simulationcopyconstructor(asim)                     
        self.sim1 = simulation()
        self.sim1.simulationcopyconstructor(asim)
        self.J0 = 0.0 #The objective function value at the start of the update() method.
        self.alphak = globe.Defaultalphak #the fraction of the calculated step that will actually be implemented.

        self.nmpcsigma = globe.DefaultNMPCSigma #Multiplied with mubarrier at the end of each iteration.

        #rand = new Random()
        self.mk = 0.0 # the value of the model that is to be minimised.

        self.initjacobian()


    def initjacobian(self): #//This function is used as an Init method for the class, and also to update the class from
                                   #// the dialogue of the properties class.
        self.jacobian = [0.0]*len(self.mvmaster)
        self.hessian = [0.0]*len(self.mvmaster)
        self.jacobianmk = [0.0]*len(self.mvmaster) #The Jacobian of the Objective function with each row begin the derivitive of mk with respect to that MV.
        self.mvmatrix = list() #Record of trajectory of MVs per update iteration.
            
        for i in range(len(self.mvmaster)):
            self.mvmatrix.append([0.0]*self.N)

        #//Interior Point ConstrainedLineSearch algorithm:
        self.nrinequalityconstraints = len(self.mvmaster)*2 #int
        self.interiorpointerror = sys.float_info.max #double.MaxValue;
        self.IDmatrixinterior = np.matrix(np.identity(self.nrinequalityconstraints)) #Identity matrix
     
        self.svector = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #slack variable vector.
        self.Smatrix = np.matrix(np.zeros((self.nrinequalityconstraints, self.nrinequalityconstraints))) #slack variable matrix.
        self.constraintvectorlinesearch = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #//The vector of the cI(x) function, that will reflect the distance from zero for each 
                                          #//constraint: CI(x) >= 0
        self.AInequality = np.matrix(np.zeros((self.nrinequalityconstraints, len(self.mvmaster)))) #//matrix of the x derivative of the contrant function vector.
        self.calcconstraintvector()
        self.calcAInequality()
        self.zvector = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #Lagrange multiplier for inequality constraints.
        self.Zmatrix = np.matrix(np.zeros((self.nrinequalityconstraints, self.nrinequalityconstraints))) #//Lagrange matrix.
        self.mubarrier = globe.DefaultMuBarrier  #mu value barrier parameter in the algorithm.
        for i in range(self.nrinequalityconstraints):
            self.svector[i,0] = self.constraintvectorlinesearch[i,0] * globe.DefaultsvalueMultiplier
            self.zvector[i,0] = self.mubarrier / (self.svector[i,0] + globe.Epsilon)
        self.updateSmatrix()
        self.updateZmatrix()
        
        self.sizeprimedual = len(self.mvmaster) + self.nrinequalityconstraints * 2 #int
        self.Amatrixconstrainedlinesearch = np.matrix(np.zeros((self.sizeprimedual, self.sizeprimedual))) #This is the A matrix of the AX = B primal dual system
        self.Bvectorconstrainedlinesearch = np.matrix(np.zeros((self.sizeprimedual, 1))) #This is the B vector of the AX = B primal dual system.
        self.jacobianconstrainedvectorlinesearch = np.matrix(np.zeros((len(self.mvmaster),1)))
        self.jacobianconstrainedvectorlinesearchbase = np.matrix(np.zeros((len(self.mvmaster), 1))) #the one at the start of the controller iteration that will be used to compare against.
        self.hessianconstrainedlinesearch = np.matrix(np.zeros((len(self.mvmaster), len(self.mvmaster))))
        self.deltaoptim = np.matrix(np.zeros((self.sizeprimedual, 1))) #vector of delta for mvs, s and z vectors.

        #//Active Set algorithm 1 :
        self.sizeactiveset1 = len(self.mvmaster) + self.nrinequalityconstraints #Row size of A and B matrices.
        self.constraintaccountingvector = [0]*self.nrinequalityconstraints  #The indices of the active constraints.
        #//fullconstraintvectoractiveset1 = new matrix(nrinequalityconstraints, 1); 
        self.fulllambdaactiveset1 = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #The full multiplier vector with rows zero for constraints that are not in the problem at a particular point
                                                    #//in time.
        self.activeconstraintvector0 = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #Constraints in the problem at a particular point in time, for active set 1 algorithm.
        self.activeconstraintvector1 = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #A temp version of the previous that can be set equal to the previous at some point when needed.
        self.activelambdaactiveset1 = np.matrix(np.zeros((self.nrinequalityconstraints, 1))) #Lagrangian multiplier for Active Set 1 algorithm.
        self.jacobianactiveset1 = np.matrix(np.zeros((len(self.mvmaster), 1)))
        self.Amatrixactiveset1 = np.matrix(np.zeros((self.sizeactiveset1, self.sizeactiveset1))) #This is the A matrix of the AX = B active set 1 system.
        self.Bvectoractiveset1 = np.matrix(np.zeros((self.sizeactiveset1, 1))) #This is the B vector of the AX = B active set 1 system.
        self.nractiveconstraints = 0 #int

        #//Init depending on type of algorithm to be used:
        if (self.algorithm == globe.nmpcalgorithm.GeneticAlgorithm1): self.initgeneticalgorithm1()
        elif (self.algorithm == globe.nmpcalgorithm.ParticleSwarmOptimisation1): self.initparticleswarmoptimisation1()
        elif (self.algorithm == globe.nmpcalgorithm.ReinforcementLearning): self.initrl()


    #Unconstrained optimisation -------------------------------------------------------------------------------------------------------------

    def calcobjectivefunction(self): #//The objective function will always be calced with sim1
        function = 0.0 #local double 
        self.sim1.copyfrom(self.mastersim)
        for i in range(self.N): #//i can be started here at index as well.  But I thought it might be best to start it at zero to get a better jacobian calc done all through the opimisation horizon.
            self.mastersim.simulateplant(False)
            for j in range(len(self.cvmaster)):
                function += self.cvmaster[j].weight / self.cvmaster[j].target.simvector[callingsimi + i] * \
                        math.pow(self.cvmaster[j].var.v - self.cvmaster[j].target.simvector[callingsimi + i], 2)  #//The cv vector will have to poin to sim1's variables.
            self.mastersim.simi += 1
        self.mastersim.copyfrom(self.sim1)
        return function


    def calcjacobian(self):
        #//J = calcobjectivefunction();
        #//mastersim.copyfrom(sim1);
        JT1 = 0.0 #//This will be J value after each MV move.
        oldmv = 0.0
        for i in range(len(self.mvmaster)):
            #//sim1.copyfrom(mastersim)
            oldmv = self.mvmaster[i].var.v
            h = self.mvmaster[i].var.v * globe.limitjacnmpc
            self.mvmaster[i].var.v += h
            JT1 = calcobjectivefunction() 
            self.jacobian[i] = (JT1 - self.J0) / h
            self.mvmaster[i].var.v = oldmv
        #//J = JT0;


    def calchessian(self): #//this assumes that the jacobian has just been calculated, and it will be used in this calc.  
                                   #//Hessian will be calculated by stepping back the mv, where jacobian stepped it forward, and then calculating rate of 
                                   #//change of slopes.
        self.sim1.copyfrom(self.mastersim)
        JT1 = 0.0 #//This will be J value after each MV move.
        oldmv = 0.0
        for i in range(len(self.mvmaster)):
            #//sim1.copyfrom(mastersim)
            oldmv = self.mvmaster[i].var.v
            h = self.mvmaster[i].var.v * globe.limitjacnmpc
            self.mvmaster[i].var.v -= h #//in the oposite direction as for first Jacobian calc.
            JT1 = self.calcobjectivefunction() 
            self.hessian[i] = (self.J0 - JT1) / h #//Temporary variable for storing this value, to calc full Hessian in next line.
            self.hessian[i] = (self.jacobian[i] - self.hessian[i]) / h
            self.mvmaster[i].var.v = oldmv


    def calcmk(self, dk): #private void calcmk(double dk) this is the model as specified in unconstrained optimisation in nmpc book
        pass


    def calcjacobianmk(self):
        self.calcjacobian()
        self.calchessian()
        for i in range(len(self.mvmaster)):
            #//sim1.copyfrom(mastersim);
            dk = self.mvmaster[i].var.v * globe.limitjacnmpc
            self.jacobianmk[i] = (dk*self.jacobian[i] + 0.5*dk*self.hessian[i]*dk) / dk


    #//Interior Point 1 ------------------ Contrained Line Search -----------------------------------------------------------------------------------------

    def calclagrangianconstrainedlinesearch(self):
        #matrix mat
        #double d
        predictweight = 0.0 #//Weight to be applied to each step until N.
        lagrangian = 0.0
        barrier = 0.0
        self.sim1.copyfrom(self.mastersim)
        self.calcconstraintvector(); #//This is for the mvs, if there are cvs also that have constraints, then this will need to be in the loop below.
        if (self.sim1.simi + self.N > globe.SimIterations):
            phorison = globe.SimIterations - self.sim1.simi
        else:
            phorison = self.N
        for i in range(phorison): #//i can be started here at index as well.  But I thought it might be best to start it at zero to get a better jacobian calc 
                                        #//done all through the opimisation horizon.
            self.mastersim.simulateplant(False)
            if (i < phorison): #//(i == phorison - 1) #//only have final value at the moment at the end of the phorison
                if (i < phorison - 1):
                    predictweight = globe.NMPCIPWeightPreTerm/self.N
                else:
                    predictweight = globe.NMPCIPWeightTerminal
                for j in range(len(self.cvmaster)):
                    lagrangian += predictweight*self.cvmaster[j].weight * \
                            math.pow((self.cvmaster[j].var.v - self.cvmaster[j].target.simvector[self.callingsimi + i])/(self.cvmaster[j].max - self.cvmaster[j].min + globe.Epsilon), 2)  #//The cv vector will have to poin to sim1's variables.
                for j in range(self.nrinequalityconstraints):
                    barrier += math.log(self.constraintvectorlinesearch.m[j][0])
                lagrangian += -self.mubarrier * barrier
            #//mat = matrix.transpose(zvector) * (constraintvectorlinesearch - svector); //as long as the constraints are only mvs, this step can 
            #//be put before the loop, but if there are cvs in the 
            #//constraints, then this needs to be moved earlier.
            #//d = mat.m[0][0]; //mat will be a 1x1 matrix.
            #//lagrangian += -d;
            self.mastersim.simi += 1
            
        self.mastersim.copyfrom(self.sim1)
        return lagrangian


    def selectbestnodeip1(self): #//For choosing teh best branch and bound node for hybrid.  And also implementing it.
        bestlagriangian = sys.float_info.max
        permutationlagrangian = 0.0
        bestmvboolmaster = [0.0]*len(self.mvboolmaster)
        #//for (int i = 0; i < mvboolmaster.Count; i++) { mvboolmaster[i].var.v = 0; }
        for i in range(math.pow(2, self.mvboolmaster.Count)):
            boolstring = ""        
            interrimstring = format(i, 'b')  #Convert.ToString(i, 2)
            boolstring = interrimstring.zfill(len(self.mvboolmaster))
            for j in range(len(self.mvboolmaster)):
                if (boolstring[j].Equals('0')):
                    self.mvboolmaster[j].var.v = self.mvboolmaster[j].min
                else:
                    self.mvboolmaster[j].var.v = self.mvboolmaster[j].max
            permutationlagrangian = self.calclagrangianconstrainedlinesearch()
            if (permutationlagrangian < bestlagriangian):
                for j in range(len(self.mvboolmaster)):
                    bestmvboolmaster[j] = self.mvboolmaster[j].var.v
                bestlagriangian = permutationlagrangian
        for i in len(self.mvboolmaster.Count):
            self.mvboolmaster[i].var.v = bestmvboolmaster[i]


    def calcjacobianconstrainedlinesearch(self, nrrows):
        LT0 = self.calclagrangianconstrainedlinesearch()
        LT1 = 0.0 #//This will be J value after each MV move.
        oldmv = 0.0
        for i in range(nrrows):
            #//sim1.copyfrom(mastersim);
            oldmv = mvmaster[i].var.v
            h = (self.mvmaster[i].max - self.mvmaster[i].min) * globe.limitjacnmpc
            self.mvmaster[i].var.v += h
            LT1 = self.calclagrangianconstrainedlinesearch()
            self.jacobianconstrainedvectorlinesearch.m[i][0] = (LT1 - LT0) / h
            self.mvmaster[i].var.v = oldmv
            #//calcconstraintvector(); //THIS CAN BE OPTIMISED so that not all the constraints and MVs have to be evaluated each time.


    def calchessianconstrainedlinesearch(self): #//will calculate the Hessian of the Lagrangian, in the case of constrained line search. Only one half is triangle (half) is calced, 
                                                        #//as the other half is an exact transpose of it.
        #//calcjacobianconstrainedlinesearch(mvmaster.Count);
        JT0 = copy.deepcopy(jacobianconstrainedvectorlinesearchbase)
        HT1 = 0.0 #//This will be J value after each MV move.
        oldmv = 0.0
        for c in range(len(self.mvmaster)):
            #//sim1.copyfrom(mastersim);
            oldmv = self.mvmaster[c].var.v
            h = (self.mvmaster[c].max - self.mvmaster[c].min) * globe.limitjacnmpc
            self.mvmaster[c].var.v += h
            self.calcjacobianconstrainedlinesearch(c + 1)
            for r in range(c):
                self.hessianconstrainedlinesearch.m[r][c] = (self.jacobianconstrainedvectorlinesearch.m[r][0] - JT0[r,0]) / h
            self.mvmaster[c].var.v = oldmv
            #//calcconstraintvector(); //THIS CAN BE OPTIMISED so that not all the constraints and MVs have to be evaluated each time.
        for c in range(len(self.mvmaster) - 1):
            for r in range(len(self.mvmaster)):
                self.hessianconstrainedlinesearch[r,c] = self.hessianconstrainedlinesearch[c,r]


    def calcBvectorconstrainedlinesearch(self):
        self.calcjacobianconstrainedlinesearch(len(self.mvmaster))
        self.jacobianconstrainedvectorlinesearchbase.copyfrom(jacobianconstrainedvectorlinesearch)
        self.updateSmatrix()
        self.calcconstraintvector()
        mat1 = self.jacobianconstrainedvectorlinesearchbase - matrix.transpose(self.AInequality) * self.zvector
        mat2 = self.Smatrix * self.zvector - self.mubarrier * self.IDmatrixinterior
        mat3 = self.constraintvectorlinesearch - self.svector
        #THIS LINE BELOW WILL NEED TO BE ADDED BACK IF YOU WANT TO USE THIS FUNCTION
        #interiorpointerror = Math.Max(matrix.euclideannorm(mat1), Math.Max(matrix.euclideannorm(mat2), matrix.euclideannorm(mat3)))
        for r in range(len(self.mvmaster)):
            self.Bvectorconstrainedlinesearch[r,0] = mat1.m[r][0]

        for r in range(self.nrinequalityconstraints):
            self.Bvectorconstrainedlinesearch[self.mvmaster.Count + r,0] = mat2.m[r][0]

        for r in range(self.nrinequalityconstraints):
            self.Bvectorconstrainedlinesearch[self.mvmaster.Count + self.nrinequalityconstraints + r,0] = mat3[r,0]


    def calcAmatrixconstrainedlinesearch(self):
        #//calcBvectorconstrainedlinesearch();
        self.calchessianconstrainedlinesearch()
        l = np.matrix(np.zeros(len(self.mvmaster), len(self.mvmaster)))
        d = np.matrix(np.zeros(len(self.mvmaster), len(self.mvmaster)))
        #IF YOU WANT TO USE THIS FUNCTION THIS LINE WILL NEED TO BE ADDED IN
        #matrix.choleskyLDLT(self.hessianconstrainedlinesearch, l, d)
        for i in range(len(self.mvmaster)):
            if (d[i,i] < globe.CholeskyDelta):
                d[i,i] = globe.CholeskyDelta
            #//else 
            #//{
            #//    double maxvalue = 
            #//}
        self.hessianconstrainedlinesearch = l * d * l.transpose()
        self.updateZmatrix()
        #//matrix Bvectorbase = new matrix(Bvectorconstrainedlinesearch);
        #//double oldmv = 0;
        for r in range(len(self.mvmaster)):
            for c in range(len(self.mvmaster)):
                self.Amatrixconstrainedlinesearch[r,c] = self.hessianconstrainedlinesearch[r,c]
            for c in range(self.nrinequalityconstraints):
                self.Amatrixconstrainedlinesearch[r,c + len(self.mvmaster) + self.nrinequalityconstraints] = -1 * self.AInequality[c,r] #//note the transpose of AIineq by swapping c and r.

        for r in range(self.nrinequalityconstraints):
            for c in range(self.nrinequalityconstraints):
                self.Amatrixconstrainedlinesearch[r + len(self.mvmaster),c + len(self.mvmaster)] = self.Zmatrix[r,c]
                self.Amatrixconstrainedlinesearch[r + len(self.mvmaster),c + len(self.mvmaster) + self.nrinequalityconstraints] = self.Smatrix[r,c]
                self.Amatrixconstrainedlinesearch[r + len(self.mvmaster) + self.nrinequalityconstraints,c + self.mvmaster.Count] = -1*self.IDmatrixinterior[r,c]
            for c in range(len(self.mvmaster)):
                self.Amatrixconstrainedlinesearch[r + len(self.mvmaster) + self.nrinequalityconstraints,c] = self.AInequality[r,c]


    def updateSmatrix(self):
        for i in range(self.nrinequalityconstraints):
            self.Smatrix[i,i] = self.svector[i,0]


    def updateZmatrix(self):
        for i in range(self.nrinequalityconstraints):
            self.Zmatrix[i,i] = self.zvector[i,0]


    def calcAInequality(self):
        self.calcconstraintvector()
        C0 = copy.deepcopy(self.constraintvectorlinesearch)
        oldmv = 0.0
        for c in range(len(self.mvmaster)):
            oldmv = self.mvmaster[c].var.v
            h = (self.mvmaster[c].max - self.mvmaster[c].min) * globe.limitjacnmpc
            self.mvmaster[c].var.v += h
            self.calcconstraintvector()
            for r in range(len(self.mvmaster)):
                self.AInequality[r][c] = (self.constraintvectorlinesearch[r,0] - C0[r,0]) / h
                self.AInequality[r + len(self.mvmaster),c] = (self.constraintvectorlinesearch[r + \
                    len(self.mvmaster),0] - C0[r + len(self.mvmaster),0]) / h
            self.mvmaster[c].var.v = oldmv
            #//calcconstraintvector();


    def calcconstraintvector(self):
        #// At this point we will assume that the MVs are the only variables with constraints.  They will be included in the vector.
        #//The minimum constraints will be defined first, and then the maximum.
        for i in range(len(self.mvmaster)):
            self.constraintvectorlinesearch[i,0] = self.mvmaster[i].var.v - self.mvmaster[i].min
            self.constraintvectorlinesearch[i + len(self.mvmaster),0] = self.mvmaster[i].max - self.mvmaster[i].var.v


    #//update methods  ------------------------------------------------------------------------------------------------------------------------------

    def updatetarget(self, simi):  #public void updatetarget(int simi)
        for i in range(len(self.cvmaster)):
            if (self.cvmaster[i].target.datasource == self.datasourceforvar.Exceldata):
                if (simi >= self.cvmaster[i].target.excelsource.data.Length): #some pythonising needed here later.
                    j = self.cvmaster[i].target.excelsource.data.Length - 1
                else:
                    j = simi
                self.cvmaster[i].target.v = self.cvmaster[i].target.excelsource.data[j]


    def updateinteriorpoint1(self):
        news = 0.0
        newz = 0.0 #//new values for the interior point method iteration.
        scompare = 0.0
        zcompare = 0.0 #//values to compare the new s and z against.
        maxmove = 0.0
        absdeltaoptim = 0.0
        self.selectbestnodeip1()
        if (len(self.mvmaster.Count)):
            self.calcBvectorconstrainedlinesearch()
            self.calcAmatrixconstrainedlinesearch()
            if (self.interiorpointerror >= globe.DefaultIPErrorTol):
                Bvector = -1 * Bvectorconstrainedlinesearch #local matrix 
                self.deltaoptim = np.linalg.solve(self.Amatrixconstrainedlinesearch, self.Bvector)
                #matrix.solveAXequalsB(self.Amatrixconstrainedlinesearch, self.deltaoptim, self.Bvector)
                self.deltaoptim = self.alphak * self.deltaoptim
                for r in range(len(self.mvmaster)):
                    maxmove = globe.MVMaxMovePerSampleTT0 * (self.mvmaster[r].max - self.mvmaster[r].min)
                    absdeltaoptim = abs(self.deltaoptim[r,0])
                    if (absdeltaoptim > maxmove):
                        self.deltaoptim[r,0] = maxmove * (self.deltaoptim[r,0] / absdeltaoptim) #//Keep the sign of deltaoptim, but limt abs value.
                    mvmaster[r].var.v += self.deltaoptim[r,0]
                    if (self.mvmaster[r].var.v >= self.mvmaster[r].max):
                        self.mvmaster[r].var.v = self.mvmaster[r].max - globe.Epsilon
                    elif (self.mvmaster[r].var.v <= self.mvmaster[r].min):
                        self.mvmaster[r].var.v = self.mvmaster[r].min + globe.Epsilon
                for r in range(self.nrinequalityconstraints):
                    news = self.svector[r,0] + self.deltaoptim[r + self.mvmaster.Count,0]
                    scompare = (1 - globe.DefaulttauIP) * self.svector[r,0]
                    if (news >= scompare):
                        self.svector[r,0] = news
                    else: self.svector[r,0] = scompare
                for r in range(self.nrinequalityconstraints):
                    newz = self.zvector[r,0] + self.deltaoptim[r + self.mvmaster.Count + self.nrinequalityconstraints,0]
                    zcompare = (1 - globe.DefaulttauIP) * self.zvector[r,0]
                    if (newz >= zcompare):
                        self.zvector[r,0] += newz 
                    else: self.zvector[r,0] += zcompar
                self.mubarrier *= self.nmpcsigma


    def update(self, simi, historise):  #public override void update(int simi, bool historise)
        if ((simi - self.initialdelay) % self.runinterval == 0):
            self.callingsimi = simi
            self.controlleri += 1
            if (self.algorithm == globe.nmpcalgorithm.UnconstrainedLineSearch):
                self.J0 = self.calcobjectivefunction()
                self.mk = self.J0
                for index in range(1,2): #//this loop was going until N.  No need for this as we will only implement the first move anyway.
                    self.calcjacobianmk()
                    for j in range(len(self.mvmaster)):
                        if (self.jacobianmk[j] == 0):
                            invslope = 0.0
                        else: invslope = 1.1 / self.jacobianmk[j]
                        reductioninvar = invslope * self.mk * self.alphak
                        self.mvmaster[j].var.v = self.mvmaster[j].var.v - reductioninvar
                        self.mvmatrix[j][index] = self.mvmaster[j].var.v
                    #//mastersim.simulateplant(false);
                    #//mastersim.simi++;
                #//mastersim.copyfrom(sim0);
            elif (self.algorithm == globe.nmpcalgorithm.InteriorPoint1):
                self.updateinteriorpoint1()
            elif (self.algorithm == globe.nmpcalgorithm.ActiveSet1):
                self.evaluateconstraintsactiveset1()
                self.calcAmatrixactiveset1()
                Bvector = -1 * self.Bvectoractiveset1 #local matrix
                self.deltaoptim, = np.linalg.solve(self.Amatrixactiveset1, self.Bvector)
                self.deltaoptim = self.alphak * self.deltaoptim
                for r in range(len(self.mvmaster)):
                    self.mvmaster[r].var.v += self.deltaoptim[r,0]
                for r in range(self.nractiveconstraints):
                    self.activelambdaactiveset1[r,0] += self.deltaoptim[r + self.mvmaster.Count,0]
            elif (self.algorithm == globe.nmpcalgorithm.GeneticAlgorithm1):
                self.replacechromosomes()
                self.crossoverchromosomes()
                self.mutatechromosomes()
                self.assignfitness()
                self.rankchromosomes()
                self.implementchromosome()
            elif (self.algorithm == globe.nmpcalgorithm.ParticleSwarmOptimisation1):
                self.updateparticles()
                self.assignparticlefitness()
                self.bestparticle()
                self.implementparticle()
            elif self.algorithm == globe.nmpcalgorithm.ReinforcementLearning:
                self.updaterl()
            #//for (int j = 0; j < mvmaster.Count; j++) //The mastersim's mv list will now be copied from the mvmatrix' first column.
            #//{
            #//    mvmaster[j].var.v = mvmatrix[j][1]; //T1 is the one to implement.  T0 is the current value.
            #//}



# Reinforcement Learning algorithm -------------------------------------------------------------------------------------

    def initrl(self):
        self.rlstatelength = len(self.cvmaster)*2
        self.rlstatehalflength = len(self.cvmaster)
        if self.rlstatelength == 0: self.rlstatelength = 2
        self.rlactionlength = len(self.mvmaster)
        if self.rlactionlength == 0: self.rlactionlength = 1
        self.rlreward = 0.0 #in our case we are going to treat the reward signals at this stage as 
        self.rlaction = np.zeros(self.rlactionlength) #the actions to be taken
        self.rlstate = np.zeros(self.rlstatelength) #the states will be the CVs as well as their targets/setpoints. 
                                                    #The first half othe state will be the set points, and then the CVs.
        self.rlnewstate = self.rlstate = np.zeros(self.rlstatelength)
        if len(self.cvmaster) > 0:
            for i in range(self.rlstatehalflength): #will only init these SPs once the cv master list has been populated.
                self.rlstate[i] = self.cvmaster[i].targetfracofrange()
            for i in range(self.rlstatehalflength, self.rlstatelength):
                self.rlstate[i] = self.cvmaster[i - self.rlstatehalflength].fracofrange()
        if len(self.mvmaster) > 0:
            for i in range(self.rlactionlength):
                self.rlaction[i] = self.mvmaster[i].fracofrange()
        colsinbuffer = self.rlstatelength + self.rlactionlength + 1 + self.rlstatelength #local int
        self.rlbuffer = np.zeros((self.controllerhistorylength, colsinbuffer)) #at this point the buffer will just be as large as the simulation horison, will be changed later.
        self.y = np.zeros(self.controllerhistorylength) #the list calculated rewards from the samples N from buffer R
        self.rlcritic = MLPRegressor()
        self.rlcritic.fit(np.ones((5,self.rlstatelength + self.rlactionlength)), np.ones((5,1)).reshape(-1, 1))
        self.rlactor = MLPRegressor()
        self.rlactor.fit(np.ones((5,self.rlstatelength)), np.ones((5,self.rlactionlength)))


    def updaterl(self):
        self.calcrewardrl()
        for i in range(self.rlstatehalflength, self.rlstatelength):
            self.rlnewstate[i] = self.cvmaster[i - self.rlstatehalflength].fracofrange()
        self.rlbuffer[self.controlleri,:] = np.hstack((self.rlstate, self.rlaction, self.rlreward, self.rlnewstate))
        self.y[self.controlleri] = self.rlreward + globe.RLGamma*\
            self.rlcritic.predict(np.hstack((self.rlnewstate, self.rlactor.predict(self.rlnewstate))))

        #self.controlleri

        self.rlaction = self.rlactor.predict(self.rlnewstate)
        for i in range(self.rlactionlength):
            self.rlaction[i] += np.random.normal()/24.0
            #print(self.rlaction[i])
            if self.rlaction[i] > 1.0: self.rlaction[i] = 1.0
            elif self.rlaction[i] < 0.0: self.rlaction[i] = 0.0
            self.mvmaster[i].var.v = self.mvmaster[i].rangetoeu(self.rlaction[i])

        self.rlstate = np.copy(self.rlnewstate)


    def calcrewardrl(self):
        self.rlreward = 0.0 #this reward is actually an objective to be minimised.
        for j in range(len(self.cvmaster)):
            self.rlreward += self.cvmaster[j].weight * \
                        math.pow((self.cvmaster[j].var.v - self.cvmaster[j].target.v) / \
                        (self.cvmaster[j].max - self.cvmaster[j].min + globe.Epsilon), 2) 


    #// Genetic Algorithm1 (GA) ---------------------------------------------------------------------------------------------------------------------

#//Properties for the Genetic Algorithm 1 -----------------------------------------------------------------------------------------------------

    
    

    #private Random rand;

    
    #private chromosomecomparerfit comparerfitness;
    #private IComparer<chromosome> chromosomecomparer;

    def compccomplex(self, x, y): #x and y are complex()
        if (abs(x.imag) < globe.ZeroImaginary and abs(y.imag) >= globe.ZeroImaginary):
            return -1
        elif (abs(x.imag) >= globe.ZeroImaginary and abs(y.imag) < globe.ZeroImaginary):
            return 1
        elif (abs(x.imag) < globe.ZeroImaginary and abs(y.imag) < globe.ZeroImaginary):
            if (x.real < y.real): return -1
            elif (x.real > y.real): return 1
            else: return 0
        else:
            return 0

    def compchromosomes(self, x, y): #public int compcchromosome(chromosome x, chromosome y)
        if (x == None):
            if (y == None):
                #// If x is null and y is null, they're
                #// equal. 
                return 0
            else:
                #// If x is null and y is not null, y
                #// is greater. 
                return 1
        else:
            #// If x is not null...
            #//
            if (y == None):
            #// ...and y is null, x is greater.
                return 1
            else:
                #// ...and y is not null, compare first the basket, then the ranking
                #//
                if (x.fitness < y.fitness): return -1  #//we want the list of chromosomes listed from smallest objective function (fit) at the top
                                                             #// to largest objective function (least fit) at the bottom.
                elif (x.fitness > y.fitness):
                    return 1
                else:
                    return 1


    def initgeneticalgorithm1(self):
        self.nrchromosomes = globe.DefaultNrChromosomes #The total number of total solutions that will be kept in memory each iteration.
        self.nrsurvivingchromosomes = globe.DefaultNrSurvivingChromosomes #Nr of chromosomes that will be passed to the next iteration and not replaced by new random ones.
        self.nrpairingchromosomes = globe.DefaultNrPairingChromosomes #The nr of chromosomes of the total population that will be pairing and producing children.
        self.chromosomelistsize = self.nrchromosomes + self.nrpairingchromosomes #Total memory to be allocated.
        self.defaultprobabilityofmutation = globe.DefaultProbabilityOfMutation #The probability that a child will be mutated in one bit.
        self.nriterations = globe.DefaultNrIterations #The number of iterations until the best GA solution will be passed to the update method.
        self.crossoverpoint = globe.DefaultCrossOverPoint; #Bit index nr (starting from zero) from right to left in the binary representation, where
                                            #//cross over and mutation will start.

        self.chromosomes = list() #List<chromosome>() . The solutions that are kept in memory for the GA.  This list will be sorted in each iteration.
        #comparerfitness = new chromosomecomparerfit();
        #chromosomecomparer = comparerfitness;

        for i in range(self.chromosomelistsize):
            self.chromosomes.append(chromosome(mvmaster.Count))


    def calcfitnessga1(self):
        #//matrix mat;
        #//double d;
        fitness = 0.0
        self.sim1.copyfrom(self.mastersim)
        #//calcconstraintvectoractiveset1(); //This is for the mvs, if there are cvs also that have constraints, then this will need to be in the loop below.
        if (self.sim1.simi + self.N > globe.SimIterations):
            phorison = globe.SimIterations - self.sim1.simi
        else:
            phorison = self.N
        for i in range(phorison): #//i can be started here at index as well.  But I thought it might be best to start it at zero to get a better jacobian calc done all through the opimisation horizon.
            self.mastersim.simulateplant(False)
            for j in range(len(self.cvmaster)):
                fitness += self.cvmaster[j].weight * \
                        math.pow((self.cvmaster[j].var.v - self.cvmaster[j].target.simvector[self.callingsimi + i]) / \
                        (self.cvmaster[j].max - self.cvmaster[j].min + globe.Epsilon), 2)  #//The cv vector will have to poin to sim1's variables.

            #//if (nractiveconstraints > 0)
            #//{
            #//    mat = matrix.transpose(activeconstraintvector1) * activelambdaactiveset1; //as long as the constraints are only mvs, this step can 
            #//    //be put before the loop, but if there are cvs in the 
            #//    //constraints, then this needs to be moved earlier.
            #//    d = mat.m[0][0]; //mat will be a 1x1 matrix.
            #//    lagrangian += -d;
            #//}
            self.mastersim.simi += 1
        self.mastersim.copyfrom(self.sim1)
        return fitness


    def replacechromosomes(self): #//the bottom ranked chromosomes will be replaced with new ones.
        for i in range(self.nrsurvivingchromosomes, self.nrchromosomes):
            self.chromosomes[i].initrandom()


    def replaceat(self, inputstr, index, newChar): #public void replaceat(ref string inputstr, int index, char newChar)
        if (inputstr == None):
            #throw new ArgumentNullException("input");
            raise ValueError('input')
        chars = list(inputstr)
        chars[index] = newChar
        inputstr = '',join(chars)
        return inputstr


    def crossoverchromosomes(self):
        parent1 = ''
        parent2 = ''
        child1 = ''
        child2 = '' #4 local strings
        for i in range(self.nrpairingchromosomes / 2):
            #//chromosomes[nrchromosomes + i * 2].copyfrom(chromosomes[i * 2]);
            #//chromosomes[nrchromosomes + i * 2 + 1].copyfrom(chromosomes[i * 2 + 1]);
            for j in range(len(self.mvmaster)):
                #parent1 = Convert.ToString(self.chromosomes[i * 2].mvs[j], 2);
                parent1 = format(self.chromosomes[i * 2].mvs[j], 'b') 
                #parent2 = Convert.ToString(self.chromosomes[i * 2 + 1].mvs[j], 2);
                parent2 = format(self.chromosomes[i * 2 + 1].mvs[j], 'b')
                #child1 = Convert.ToString(self.chromosomes[i * 2].mvs[j], 2);
                child1 = format(self.chromosomes[i * 2].mvs[j], 'b')
                #child2 = Convert.ToString(self.chromosomes[i * 2 + 1].mvs[j], 2);
                child2 = format(self.chromosomes[i * 2 + 1].mvs[j], 'b')
                minparentlength = math.min(len(parent1), len(parent2))
                maxcrossoverpoint = math.min(minparentlength, self.crossoverpoint)
                for k in range(maxcrossoverpoint): #// k starts at 2^0 and works to the left in the binary number as string.
                    child1 = self.replaceat(child1, child1.Length - 1 - k, parent2[parent2.Length - 1 - k])
                    child2 = self.replaceat(child2, child2.Length - 1 - k, parent1[parent1.Length - 1 - k])
                self.chromosomes[self.nrchromosomes + i * 2].mvs[j] = int(child1, 2)
                self.chromosomes[self.nrchromosomes + i * 2 + 1].mvs[j] = int(child2, 2)


    def mutatechromosomes(self):
        pass


    def assignfitness(self):
        oldmv = [0.0]*len(self.mvmaster) #local list doubles
        for j in range(len(self.mvmaster)):
            oldmv[j] = self.mvmaster[j].var.v
        for i in range(len(self.chromosomes)):
            for j in range(len(self.mvmaster)):
                self.mvmaster[j].var.v = self.mvmaster[j].rangetoeu(self.chromosomes[i].mvs[j] / 100.0)
            self.chromosomes[i].fitness = self.calcfitnessga1()
        for j in range(len(self.mvmaster)):
            self.mvmaster[j].var.v = oldmv[j]


    def rankchromosomes(self):
        self.chromosomes = sorted(self.chromosomes, key=cmp_to_key(self.compchromosomes))


    def implementchromosome(self):
        for i in range(len(self.mvmaster)):
            self.mvmaster[i].var.v += (self.mvmaster[i].rangetoeu(self.chromosomes[0].mvs[i] / 100.0) - \
                self.mvmaster[i].var.v)*self.alphak


    #//Particle Swarm Optimisation 1 (PSO) -----------------------------------------------------------------------------------------------

    #//Properties for the Particle Swarm Optimisation 1 -----------------------------------------------------------------------------------------------------
    #//public int nrparticles;
    

    
    

    #public double[] mvboolinterrim; //An internal class array used for interrim storage of the boolean mvs of various particles.


    def initparticleswarmoptimisation1(self):  #//The boolean MVs will be implemented as one extra real/floating point MV.  Coded from the different bits.
        defaultboolmv = 0.0 #local double
        #//nrparticles = global.DefaultNrParticles;
        self.nrcontinuousparticles = globe.DefaultNrContinuousParticles #The total number of total continuous solutions that will be kept in memory each iteration.
        self.nrbooleanparticles = globe.DefaultNrBooleanParticles #The total number of total continuous solutions that will be kept in memory each iteration.
        self.bestsolutioncontinuousparticleindex = 0 #//The particle that has had the best solution to the problem so far.
        self.bestsolutionbooleanparticleindex = 0 #The particle that has had the best solution to the problem so far.
        self.bestfitnesscontinuous = sys.float_info.max #the fitness of the best particle historically.
        self.bestfitnessboolean = sys.float_info.max #the fitness of the best particle historically.

        self.continuousparticles = list() #List<particle>();
        self.booleanparticles = list() #List<particle>();
        #//mvboolinterrim = new double[mvboolmaster.Count];
        #//systemhasbool = (mvboolmaster.Count > 0) ? 1 : 0;
        #//if (systemhasbool > 0) {defaultboolmv = convertboolmvstopsomv();}
        for i in range(self.nrcontinuousparticles):
            self.continuousparticles.append(particle(len(self.mvmaster), globe.DefaultMaxValueforMVs)) #/#/continuous as one extra mv that will combine all the booleans in each particle.
            for j in range(len(self.mvmaster)):
                self.continuousparticles[i].bestmvs[j] = self.mvmaster[j].fracofrange() * 100.0 #//Set best solution for now to be equal to the current mvs. Use percentage.

        for i in range(self.nrbooleanparticles):
            self.booleanparticles.append(particle(len(self.mvboolmaster), 1.0)) #//continuous as one extra mv that will combine all the booleans in each particle.
            for j in range(len(self.mvboolmaster)):
                self.booleanparticles[i].bestmvs[j] = self.mvboolmaster[j].var.v
            #//for (int j = 0; j < mvboolmaster.Count; j++)
            #//{
            #//    //particles[i].bestmvs[j + mvmaster.Count] = rand.Next(Convert.ToInt32(Math.Round(mvboolmaster[j].var.v*50)), 
            #//    //    Convert.ToInt32(Math.Round((mvboolmaster[j].var.v + 1)*50))); //Set best solution for now to be equal to the current mvs. Use percentage.
            #//    //particles[i].bestmvs[j + mvmaster.Count] = rand.NextDouble();
            #//    particles[i].bestmvs[j + mvmaster.Count] = mvboolmaster[j].var.v;
            #//}

            #//if (systemhasbool > 0) { particles[i].bestmvs[mvmaster.Count] = defaultboolmv; }// 50.0; }// defaultboolmv; }


    def convertboolmvstopsomv(self): #//Convert the bit string of boolean mvs to a PSO MV that will fall between 0 and 
                                                      #  //global.DefaultMaxValueforMVs
        boolstring = ""
        for i in range(len(self.mvboolmaster)):
            if (self.mvboolmaster[i].var.v == self.mvboolmaster[i].min):
                boolstring = boolstring + "0"
            else:
                boolstring = boolstring + "1"
        boolstringlength = len(boolstring)
        interrimvalue = int(boolstring, 2)
        interrimdouble = float(interrimvalue)
        return interrimdouble / (math.pow(2.0, boolstringlength) - 1) * globe.DefaultMaxValueforMVs


    def convertpsomvtomvboolinterrim(self, mv): #private void convertpsomvtomvboolinterrim(double mv)
        interrimdouble = mv/100.0*(math.pow(2,self.mvboolmaster.Count) - 1)
        interrimint = int(Math.Round(interrimdouble))
        interrimstring = format(interrimint,'b')
        boolstring = interrimstring.zfill(len(self.mvboolmaster))
        for i in range(len(self.mvboolmaster)):
            if (boolstring[i].Equals('0')):
                self.mvboolinterrim[i] = self.mvboolmaster[i].min
            else: 
                self.mvboolinterrim[i] = self.mvboolmaster[i].max


    def updateparticles(self):
        psi1 = 0.0 
        psi2 = 0.0#//random vars for PSO.
        absbooleanspeed = 0.0
        sigmoidbooleanspeed = 0.5

        for i in range(self.nrcontinuousparticles):
            for j in range(len(self.mvmaster)):
                psi1 = random.random()
                psi2 = random.random()
                self.continuousparticles[i].currentspeed[j] += 2 * psi1 * (self.continuousparticles[i].bestmvs[j] - self.continuousparticles[i].currentmvs[j]) + \
                        2 * psi2 * (self.continuousparticles[self.bestsolutioncontinuousparticleindex].bestmvs[j] - self.continuousparticles[i].currentmvs[j])
                self.continuousparticles[i].currentmvs[j] += self.continuousparticles[i].currentspeed[j]

                if (self.continuousparticles[i].currentmvs[j] < 0):
                    #//particles[i].currentmvs[j] = 0;
                    self.continuousparticles[i].currentmvs[j] = random.randint(0, globe.PSOMVBoundaryBuffer)
                elif (self.continuousparticles[i].currentmvs[j] > globe.DefaultMaxValueforMVs):
                    #//particles[i].currentmvs[j] = global.DefaultMaxValueforMVs;
                    self.continuousparticles[i].currentmvs[j] = random.randint(globe.DefaultMaxValueforMVs - globe.PSOMVBoundaryBuffer, globe.DefaultMaxValueforMVs)

        for i in range(self.nrbooleanparticles):
            for j in range(len(self.mvboolmaster)):
                psi1 = random.random()
                psi2 = random.random()
                self.booleanparticles[i].currentspeed[j] += 2 * psi1 * (self.booleanparticles[i].bestmvs[j] - self.booleanparticles[i].currentmvs[j]) + \
                    2 * psi2 * (self.booleanparticles[self.bestsolutionbooleanparticleindex].bestmvs[j] - self.booleanparticles[i].currentmvs[j])
                absbooleanspeed = abs(self.booleanparticles[i].currentspeed[j])
                if (absbooleanspeed > globe.PSOMaxBooleanSpeed):
                    self.booleanparticles[i].currentspeed[j] = self.booleanparticles[i].currentspeed[j] / absbooleanspeed * globe.PSOMaxBooleanSpeed
                sigmoidbooleanspeed = utilities.sigmoid(self.booleanparticles[i].currentspeed[j])
                if (random.random() < sigmoidbooleanspeed):
                    self.booleanparticles[i].currentmvs[j] = 1.0
                else:
                    self.booleanparticles[i].currentmvs[j] = 0.0
                #//if (particles[i].currentmvs[j] < 0)
                #//{
                #//        //particles[i].currentmvs[j] = rand.Next(0, 50);
                #//        particles[i].currentmvs[j] = rand.Next(0, global.DefaultMaxValueforMVs);
                #//}
                #//else if (particles[i].currentmvs[j] > global.DefaultMaxValueforMVs)
                #//{
                #//        //particles[i].currentmvs[j] = rand.Next(50, global.DefaultMaxValueforMVs);
                #//        particles[i].currentmvs[j] = rand.Next(0, global.DefaultMaxValueforMVs);
                #//}


    def assignparticlefitness(self):
        oldmv = [0.0]*len(self.mvmaster)
        oldmvbool = [0.0]*len(self.mvboolmaster)

        for j in range(len(self.mvmaster)):
            oldmv[j] = self.mvmaster[j].var.v

        for j in range(len(self.mvboolmaster)):
            oldmvbool[j] = self.mvboolmaster[j].var.v

        for i in range(self.nrcontinuousparticles):
            for j in range(len(self.mvmaster)):
                self.mvmaster[j].var.v = self.mvmaster[j].rangetoeu(self.continuousparticles[i].currentmvs[j] / 100.0)

            for j in range(len(self.mvboolmaster)):
                #//mvboolmaster[j].var.v = Math.Round(particles[i].currentmvs[j + mvmaster.Count] / 100.0);
                self.mvboolmaster[j].var.v = self.booleanparticles[i].currentmvs[j]
            self.continuousparticles[i].currentfitness = self.calcfitnessga1()
            self.booleanparticles[i].currentfitness = self.continuousparticles[i].currentfitness

            if (self.continuousparticles[i].currentfitness > self.continuousparticles[i].bestfitness):
                self.continuousparticles[i].bestfitness = self.continuousparticles[i].currentfitness
                self.bestfitnesscontinuous = self.continuousparticles[i].currentfitness

            if (self.booleanparticles[i].currentfitness > self.booleanparticles[i].bestfitness):
                self.booleanparticles[i].bestfitness = self.booleanparticles[i].currentfitness
                self.bestfitnessboolean = self.booleanparticles[i].currentfitness

        #//for (int i = 0; i < nrbooleanparticles; i++)
        #//{
        #//    for (int j = 0; j < mvboolmaster.Count; j++)
        #//    {
        #//        //mvboolmaster[j].var.v = Math.Round(particles[i].currentmvs[j + mvmaster.Count] / 100.0);
        #//        mvboolmaster[j].var.v = booleanparticles[i].currentmvs[j];
        #//    }

        #//    booleanparticles[i].currentfitness = calcfitnessga1();

        #//    if (booleanparticles[i].currentfitness > booleanparticles[i].bestfitness)
        #//    {
        #//        booleanparticles[i].bestfitness = booleanparticles[i].currentfitness;
        #//        bestfitnessboolean = booleanparticles[i].currentfitness;
        #//    }
        #//}
        for j in range(len(self.mvmaster)):
            self.mvmaster[j].var.v = oldmv[j]
        for j in range(len(self.mvboolmaster)):
            self.mvboolmaster[j].var.v = oldmvbool[j]


    def bestparticle(self): #//This routine will check the fittest solutions per particle and update, as well as the global fittest solution 
                                    #// and update.
        for i in range(len(self.continuousparticles)):
            if (self.continuousparticles[i].currentfitness < self.continuousparticles[i].bestfitness):
                self.continuousparticles[i].bestfitness = self.continuousparticles[i].currentfitness
                for j in range(len(self.mvmaster)):
                    self.continuousparticles[i].bestmvs[j] = self.continuousparticles[i].currentmvs[j]
            if (self.continuousparticles[i].currentfitness < self.bestfitnesscontinuous):
                self.bestfitnesscontinuous = self.continuousparticles[i].currentfitness
                self.bestsolutioncontinuousparticleindex = i

        for i in range(len(self.booleanparticles)):
            if (self.booleanparticles[i].currentfitness < self.booleanparticles[i].bestfitness):
                self.booleanparticles[i].bestfitness = self.booleanparticles[i].currentfitness
                for j in range(len(self.mvboolmaster)):
                    self.booleanparticles[i].bestmvs[j] = self.booleanparticles[i].currentmvs[j]
            if (self.booleanparticles[i].currentfitness < self.bestfitnessboolean):
                self.bestfitnessboolean = self.booleanparticles[i].currentfitness
                self.bestsolutionbooleanparticleindex = i


    def implementparticle(self):
        deltaoptim = 0.0
        maxmove = 0.0
        absdeltaoptim = 0.0
        for j in range(len(self.mvmaster)):
            deltaoptim = (self.mvmaster[j].rangetoeu(self.continuousparticles[self.bestsolutioncontinuousparticleindex].\
                bestmvs[j] / 100.0) - self.mvmaster[j].var.v) * self.alphak
            maxmove = globe.MVMaxMovePerSampleTT0 * (self.mvmaster[j].max - self.mvmaster[j].min)
            absdeltaoptim = abs(deltaoptim)
            if (absdeltaoptim > maxmove):
                deltaoptim = maxmove * (deltaoptim / absdeltaoptim)#//Keep the sign of deltaoptim, but limt abs value.
            self.mvmaster[j].var.v += deltaoptim
        #//if (systemhasbool > 0) { convertpsomvtomvboolinterrim(particles[bestsolutionparticleindex].bestmvs[mvmaster.Count]); }

        for j in range(len(self.mvboolmaster)):
            #//mvboolmaster[j].var.v = Math.Round(particles[bestsolutionparticleindex].bestmvs[j + mvmaster.Count] / 100.0);
            self.mvboolmaster[j].var.v = self.booleanparticles[self.bestsolutionbooleanparticleindex].bestmvs[j]


    #//Active Set algorithm 1 ----------------------------------------------------------------------------------------------------------------------

    #private double calclagrangianactiveset1()
    #{
    #    matrix mat;
    #    double d;
#
     #   double lagrangian = 0;
     #   sim1.copyfrom(mastersim);
    #    calcconstraintvectoractiveset1(); //This is for the mvs, if there are cvs also that have constraints, then this will need to be in the loop below.
     #   for (int i = 0; i < N; i++) //i can be started here at index as well.  But I thought it might be best to start it at zero to get a better jacobian calc done all through the opimisation horizon.
    #    {
     #       mastersim.simulateplant(false);
     #       for (int j = 0; j < cvmaster.Count; j++)
     #       {
     #           lagrangian += cvmaster[j].weight / cvmaster[j].target.simvector[callingsimi + i] *
     #               Math.Pow(cvmaster[j].var.v - cvmaster[j].target.simvector[callingsimi + i], 2);  //The cv vector will have to poin to sim1's variables.
     #       }

      #      if (nractiveconstraints > 0)
       #     {
      #          mat = matrix.transpose(activeconstraintvector1) * activelambdaactiveset1; //as long as the constraints are only mvs, this step can 
       #         //be put before the loop, but if there are cvs in the 
       #         //constraints, then this needs to be moved earlier.
       #         d = mat.m[0][0]; //mat will be a 1x1 matrix.
       #         lagrangian += -d;
       #     }
       #     mastersim.simi++;
       # }

      #  mastersim.copyfrom(sim1);
     #   return lagrangian;
    #}

   # private void calcconstraintvectoractiveset1() //This will calculate constraint 1 for algorithm 1, based on which constraints are active as per the
    #//constraintaccountingvector.
    #{
    #    int fullindex = 0;
    #    double var = 0;
    #    for (int j = 0; j < nractiveconstraints; j++)
    #    {
     #       fullindex = constraintaccountingvector[j];

     #       if (fullindex < mvmaster.Count)
     #       {
     #           var = mvmaster[fullindex].var.v - mvmaster[fullindex].min;
     #       }
     #       else
    #        {
     #           var = mvmaster[fullindex - mvmaster.Count].max - mvmaster[fullindex - mvmaster.Count].var.v;
     #       }
     #       activeconstraintvector1.m[j][0] = var;
    #    }
   # }

   # private void evaluateconstraintsactiveset1() //At the end of each iteration, the constraints will be evaluated, as well as the sign of the lambdas
   # {
    #    double var = 0;
    #    for (int i = 0; i < nractiveconstraints; i++)
    #    {
    #        fulllambdaactiveset1.m[constraintaccountingvector[i]][0] = activelambdaactiveset1.m[i][0];
    #    }

    #    constraintaccountingvector.Clear();
    #    activeconstraintvector0.m.Clear();
     #   activeconstraintvector1.m.Clear();
    #    activelambdaactiveset1.m.Clear();
    #    nractiveconstraints = 0;
#
    #    for (int i = 0; i < nrinequalityconstraints; i++)
    #    {
    #        if (i < mvmaster.Count)
     #       {
     ##           var = mvmaster[i].var.v - mvmaster[i].min;
     #       }
     #       else
     #       {
     #           var = mvmaster[i - mvmaster.Count].max - mvmaster[i - mvmaster.Count].var.v;
     #       }

     #       if (var <= 0) // && fulllambdaactiveset1.m[i][0] >= 0) //THIS CONDITION CAN BE ADDED AGAIN LATER.
     #       {
     #           activeconstraintvector0.m.Add(new List<double>());
      #          activeconstraintvector0.m[activeconstraintvector0.m.Count - 1].Add(var);
      #          activelambdaactiveset1.m.Add(new List<double>());
      #          activelambdaactiveset1.m[activelambdaactiveset1.m.Count - 1].Add(fulllambdaactiveset1.m[i][0]);
      #          constraintaccountingvector.Add(i);
      ##          nractiveconstraints++;
     #       }
     #   }
     #   activeconstraintvector1.copyfrom(activeconstraintvector0);
    #   sizeactiveset1 = mvmaster.Count + nractiveconstraints;
     #   Amatrixactiveset1.initmatrix(sizeactiveset1, sizeactiveset1);
     #   Bvectoractiveset1.initmatrix(sizeactiveset1, 1);

    #}

    #private void calcjacobianactiveset1()
    #{
    #    double LT0 = calclagrangianactiveset1();
    #    double LT1 = 0; //This will be J value after each MV move.
    #    double oldmv = 0;
     #   for (int i = 0; i < mvmaster.Count; i++)
     #   {

     #       oldmv = mvmaster[i].var.v;
     #       double h = global.limitjacnmpcadd;
     #       mvmaster[i].var.v += h;
     #       LT1 = calclagrangianactiveset1();

    #        jacobianactiveset1.m[i][0] = (LT1 - LT0) / h;
     #       mvmaster[i].var.v = oldmv;
     #       //calcconstraintvector(); //THIS CAN BE OPTIMISED so that not all the constraints and MVs have to be evaluated each time.
     #   }
   # }

    #private void calcBvectoractiveset1()
    #{
     #   calcjacobianactiveset1();
     #   for (int r = 0; r < mvmaster.Count; r++)
     #   {
      #      Bvectoractiveset1.m[r][0] = jacobianactiveset1.m[r][0];
     #   }

      #  calcconstraintvectoractiveset1();
     #   for (int r = 0; r < nractiveconstraints; r++)
      #  {
      #      Bvectoractiveset1.m[mvmaster.Count + r][0] = activeconstraintvector1.m[r][0];
     #   }

   # }

   # private void calcAmatrixactiveset1()
    #{
    #    calcBvectoractiveset1();
    #    matrix Bvectorbase = new matrix(Bvectoractiveset1);
    #    double oldmv = 0;
     #   for (int r = 0; r < sizeactiveset1; r++)
    #    {
     #       for (int c = 0; c < mvmaster.Count; c++)
     #       {

      #          oldmv = mvmaster[c].var.v;
      #          double h = global.limitjacnmpcadd;
      #          mvmaster[c].var.v += h;
       #         calcBvectoractiveset1();

       #         Amatrixactiveset1.m[r][c] = (Bvectoractiveset1.m[r][0] - Bvectorbase.m[r][0]) / h;
        #        mvmaster[c].var.v = oldmv;
       #         //Bvectoractiveset1.copyfrom(Bvectorbase);

      #      }

        #    for (int c = 0; c < nractiveconstraints; c++)
       #     {

        #        oldmv = activelambdaactiveset1.m[c][0];
        #        double h = global.limitjacnmpcadd; ;
        #        activelambdaactiveset1.m[c][0] += h;
        #        calcBvectoractiveset1();

          #      Amatrixactiveset1.m[r][mvmaster.Count + c] = (Bvectoractiveset1.m[r][0] - Bvectorbase.m[r][0]) / h;
          #      activelambdaactiveset1.m[c][0] = oldmv;
         #       //Bvectoractiveset1.copyfrom(Bvectorbase);

         #   }

        #}
   # }

    #//other class methods ------------------------------------------------------------------------------------------------------------------------------------------------------

    def validatesettings(self):
        for i in range(len(self.cvmaster)):
            if ((self.cvmaster[i].min == 0) and (self.cvmaster[i].max == 0)):
                self.cvmaster[i].max = self.cvmaster[i].var.v


    #public override void showtrenddetail(simulation asim, List<Form> detailtrendslist)
    #{
    #   detailtrendslist.Add(new nmpcdetail(this, asim));
    #    detailtrendslist[detailtrendslist.Count - 1].Show();
    #}



    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        diag = nmpcproperties(self, asim, aroot)


    def mouseover(self, x, y):
        return (utilities.distance(x - self.location.x, y - self.location.y) <= globe.PIDControllerInitRadius)


    def draw(self, canvas):
        #//updateinoutpointlocations();

        #//Draw main tank
        #GraphicsPath tankmain;
        #Pen plotPen;
        #float width = 1;

        #tankmain = new GraphicsPath();
        #plotPen = new Pen(Color.Black, width);

        point0 = point(globe.OriginX + int(globe.GScale*(self.location.x - 0.5*globe.NMPCWidth)), 
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.NMPCHeight)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.location.x - 0.5*globe.NMPCWidth)), 
                globe.OriginY + int(globe.GScale*(self.location.y - 0.5*globe.NMPCHeight)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.location.x + 0.5*globe.NMPCWidth)), 
                globe.OriginY + int(globe.GScale*(self.location.y - 0.5*globe.NMPCHeight)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.location.x + 0.5*globe.NMPCWidth)),
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.NMPCHeight)))

        polygon = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)
        if (self.highlighted == True):
            canvas.itemconfig(polygon, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(polygon, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(polygon, fill='grey')

        #Point[] myArray = new Point[] 
        #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - 0.5*global.NMPCWidth)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.NMPCHeight))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - 0.5*global.NMPCWidth)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y - 0.5*global.NMPCHeight))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + 0.5*global.NMPCWidth)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y - 0.5*global.NMPCHeight))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + 0.5*global.NMPCWidth)),
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.NMPCHeight)))};
        #tankmain.AddPolygon(myArray);
        #plotPen.Color = Color.Black;
        #SolidBrush brush = new SolidBrush(Color.White);
        #brush.Color = (highlighted) ? Color.Orange : Color.White;
        #G.FillPath(brush, tankmain);
        #G.DrawPath(plotPen, tankmain);

        #//The writing of the name of the unitop in the unitop.
        emSize = 6 #local int
        nmpcnamepoint = point(globe.OriginX + int(globe.GScale*(self.location.x) - len(self.name)*emSize/2/2), \
            globe.OriginY + int(globe.GScale*(self.location.y)))
        nametext = canvas.create_text(nmpcnamepoint.x, nmpcnamepoint.y)
        canvas.itemconfig(nametext, text=self.name, fill='black', font=('Helvetica', str(emSize)))

        #GraphicsPath unitopname = new GraphicsPath();
        #StringFormat format = StringFormat.GenericDefault;
        #FontFamily family = new FontFamily("Arial");
        #int myfontStyle = (int)FontStyle.Bold;
        #int emSize = 10;
        #PointF namepoint = new PointF(global.OriginX + Convert.ToInt32(global.GScale * (location.x) - name.Length * emSize / 2 / 2),
        #    global.OriginY + Convert.ToInt32(global.GScale * (location.y)));
        #unitopname.AddString(name, family, myfontStyle, emSize, namepoint, format);
        #G.FillPath(Brushes.Black, unitopname);

        #//Draw inpoint
        super(nmpc, self).draw(canvas)


