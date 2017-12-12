import controlvar as controlvar
import globe as globe
import numpy as np
import copy
import component as component
import math
from functools import cmp_to_key

class material(object):
    def __init__(self): #default constructor
        pass

    def materialconstructor1(self,aV): #aVolume                
        #public double hL; //Joule/mol.  Molar enthalpy for the liquid phase, e.g. on a stage in a distillation column.
        #public double hV; //Joule/mol.  Molar enthalpy for the vapour phase, e.g. on a stage in a distillation column.
        #public double ML; //moles.  Total molar liquid hold-up.
        #public double MV; //moles.  Total molar vapour hold-up.

        #double totalumolar; //last calculation of the total vmolar;

        #public double[] fugacityV; //

        #public double[] K;  //
        #public double bs; //Used in scarlet cubic solver. bs for bscarlet, This is for another cubic solver: http://home.scarlet.be/~ping1339/cubic.htm
        #public double cs; //Used in scarlet cubic solver.
        #public double ds; //Used in scarlet cubic solver.
        #public double rs; // Used in scarlet cubic solver.
        #public double es; //Used in scarlet cubic solver.
        #public double fs; //Used in scarlet cubic solver.

        #public double totalCp; //Heat capacity of the material in totallity, with all its components includded.

        #public double massofonemole; //kg/mole
        #public double volumeofonemole; //m^3/mole
        #public materialphase phase;

        #//public int componentindex; //Index in the fuildpackage of the component of this material.  At this stage only 1 component
        #//can be included per material in ChemSim.  To be updated later.  
         #                   //This should be taken out later.  Only reason it is here, is to make the convergence of the flashing algorithm work better at the moment.





        self.P = controlvar.controlvar() #//Pa
        self.V = controlvar.controlvar() #m3.  This will be total stage volume in the case of a distillation column.
        self.vmolar = controlvar.controlvar() #m3/mole.  Total volume per mole for the total material all phases.
        self.vmolarL = controlvar.controlvar() #m3/mole.  Total volume per mole for the total liquid phase.
        self.vmolarV = controlvar.controlvar() #m3/mole.  Total volume per mole for the total vapour phase.
        self.density = controlvar.controlvar() #kg/m3
        self.T = controlvar.controlvar() #Kelvin
        self.mass = controlvar.controlvar(); #kg
        self.n = controlvar.controlvar() #amount of moles of the material (all phases) for all components.
        self.f = controlvar.controlvar() #fraction.  Vapour molar fraction.
        self.U = controlvar.controlvar() #Joule. Internal energy.
        self.umolar = controlvar.controlvar() #Joule/mol.  Molar internal energy.
        self.relativehumidity = controlvar.controlvar()  #% ; Using relative humidity at the moment since 
                                                        #that is the data that we have on site.

        oldn = 0.0
        self.hL = 0.0  #Joule/mol.  Molar enthalpy for the liquid phase, e.g. on a stage in a distillation column.
        self.hV = 0.0 #Joule/mol.  Molar enthalpy for the vapour phase, e.g. on a stage in a distillation column.
        self.ML = 0.0  #moles.  Total molar liquid hold-up.
        self.MV = 0.0  #moles.  Total molar vapour hold-up.
        self.composition = list() #list of component objects.  mass in kg for each component in the material
        for i in range(len(globe.fluidpackage)):
            if (globe.fluidpackage[i].n != 0):
                self.composition.append(globe.fluidpackage[i])
                oldn += composition[composition.Count - 1].n

        self.x = [0.0]*len(self.composition) # list of doubles. new double[composition.Count]; 
                            #Molar fraction of the total liquid of the material per component.
        self.y = [0.0]*len(self.composition) #new double[composition.Count]; Molar fraction of the total vapour of the material per component.
        self.z = [0.0]*len(self.composition) #new double[composition.Count]; fraction.  Molar fraction per component of the total moles in the material.
        self.fugacityL = [0.0]*len(self.composition) #new double[composition.Count]; fugacity per component for the liquid phase.
        self.fugacityV = [0.0]*len(self.composition) #new double[composition.Count] #fugacity per component for the vapour phase.
        self.K = [0.0]*len(self.composition) #new double[composition.Count]; dimensionless - depends on omega.
        self.Z = list() #new double[composition.Count][]; 
            #Compressibility factor. More than one value should be present based on the amount of phases in the material
        for i in range(len(self.composition)):
            self.Z.append([0, 0, 0, 0, 0, 0]) #Z[i] = new double[6];
            nullZ(i)

        self.discriminantZ = [0.0]*len(self.composition) # double[composition.Count]; The discriminant of the cubig PR equation for Z;
        self.Tr = [0.0]*len(self.composition) #new double[composition.Count]; reduced temperature.
        self.ac = [0.0]*len(self.composition) #new double[composition.Count]; 
                            #kg⋅m^5 / (s^2 ⋅mol^2 ) ; figure used in Peng Robinson equation.
        self.aT = [0.0]*len(self.composition) #new double[composition.Count]; 
                            #kg⋅m^5 /( s^2 ⋅mol^2 ); figure used in Peng Robinson equation.
        self.alpha = [0.0]*len(self.composition) #new double[composition.Count]; 
                            #part of the equation for aT, and used in other equations in the Peng Robinson collection.
        self.b = [0.0]*len(self.composition) #new double[composition.Count];
                            #m^3/mol ; figure used in Peng Robinson equation.
        self.A = [0.0]*len(self.composition) #new double[composition.Count]; used in equation for compressibility factor.
        self.B = [0.0]*len(self.composition) #new double[composition.Count]; used in equation for compressibility factor.
        self.delta0 = [0.0]*len(self.composition) #new double[composition.Count]; used to solve the cubic equation for Z.
        self.delta1 = [0.0]*len(self.composition) #new double[composition.Count]; used to solve the cubic equation for Z.
        self.C = [0.0]*len(self.composition) #new double[composition.Count]; used to solve the cubic equation for Z.
        self.Cc = [complex()]*len(self.composition)  #new complex[composition.Count]; used to solve the cubic equation for Z.
        self.Cp = [0.0]*len(self.composition) #new double[composition.Count]; 
                                #Heat capacity of constant pressure for an ideal gas type scenario per component.

        self.umolarL = [0.0]*len(self.composition) #new double[composition.Count]; 
                                #Joule/mol.  Molar internal energy for the total liquid phase.
        self.umolarV = [0.0]*len(self.composition) #new double[composition.Count];
                                #Joule/mol.  Molar internal energy for the total vapour phase.
        self.umolarideal = [0.0]*len(self.composition) #new double[composition.Count];
                                #Joule/mol.  Molar internal energy for the ideal gas case.

        self.acomp = [0.0]*len(self.composition) #new double[composition.Count]; //Cubic equation for compressibility factor coeficients.
        self.bcomp = [0.0]*len(self.composition) #new double[composition.Count]; //Cubic equation for compressibility factor coeficients.
        self.ccomp = [0.0]*len(self.composition) #new double[composition.Count]; //Cubic equation for compressibility factor coeficients.
        self.dcomp = [0.0]*len(self.composition) #new double[composition.Count]; //Cubic equation for compressibility factor coeficients.

        self.a = list() #new double[composition.Count][]; 
                    #used to solve the cubic equation for Z by making use of an alternative closed form formulat for them.
        for i in range(len(self.composition)):
            self.a.append([0.0]*3)

        self.Qc = [0.0]*len(self.composition) #new double[composition.Count]; //used in alternative formula.
        self.Rc = [0.0]*len(self.composition) #new double[composition.Count]; //used in alternative formula.
        self.Dc = [0.0]*len(self.composition) #new double[composition.Count]; //used in alternative formula.
        self.Sc = [0.0]*len(self.composition) #new complex[composition.Count]; //used in alternative formula.
        self.Tc = [0.0]*len(self.composition) #new complex[composition.Count]; //used in alternative formula.

        self.zs = [complex()]*6 #//Used in scarlet cubic solver.
        self.us = [complex()]*2 #//Used in scarlet cubic solver.
        self.ys = [complex()]*6 #//Used in scarlet cubic solver.

        self.uvflashsize = 2 * len(self.composition) + 3  #The size of the k variables k equations problem 
                                        #to be solved for the UV flash.
        self.xvector = [0.0]*self.uvflashsize # new double[uvflashsize];
        for i in range(len(composition)):
            self.x[i] = 1.0 / len(composition) #//Add 0.5 to get starting values that can converge.
            self.y[i] = 1.0 / len(composition)
        if len(composition) == 1: self.uvflashsize = 3  #x and y does not need to be part of the model anymore.
        self.origuvflashsize = self.uvflashsize

        self.jacobian = np.matrix(np.zeros((self.uvflashsize, self.uvflashsize)))  # new matrix(uvflashsize, uvflashsize);
                                    #The jacobian matrix for the system of equations as defined below in fflash().

        self.V.v = aV
        self.P.v = globe.baseprocessclassInitPressure
        self.T.v = globe.baseprocessclassInitTemperature
        self.f.v = globe.fdefault

        self.mapvarstox() #//Variables are allocated according to the Flatby article sequence of equations.
        self.n.v = self.V.v / self.calcvmolaranddensity()

        for i in range(len(composition)):
            self.composition[i].n = self.composition[i].n / oldn * self.n.v
        self.calcmass()

        self.U.v = self.n.v * self.calcumolar()
        #//density.v = mass.v / V.v;

        self.calccompz()
        self.uvflash() # // This is commented out now, but needs to be put back in soon again.
        #//P.simvector = new double[global.SimIterations];
        #//T.simvector = new double[global.SimIterations];
        #//f.simvector = new double[global.SimIterations];
        #//n.simvector = new double[global.SimIterations];
        #//U.simvector = new double[global.SimIterations];
        #self.density.simvector = new double[global.SimVectorLength]; #Should only have to allocate this memory when needed


    def materialconstructor2(self, acomposition, aTemp, aV, aP, af):
        #materialsecondconstructor(List<component> acomposition, double aTemp, double aV, double aP, double af)
                #second constructor
        self.P = controlvar.controlvar() # //Pa
        self.V = controlvar.controlvar() #; //m3.  This will be total stage volume in the case of a distillation column.
        self.vmolar = controlvar.controlvar() #; //m3/mole.  Total volume per mole for the total material all phases.
        self.vmolarL = controlvar.controlvar() #; //m3/mole.  Total volume per mole for the total liquid phase.
        self.vmolarV = controlvar.controlvar() #; //m3/mole.  Total volume per mole for the total vapour phase.
        self.density = controlvar.controlvar() #; //kg/m3
        self.T = controlvar.controlvar() #; //Kelvin
        self.mass = controlvar.controlvar() # //kg
        self.n = controlvar.controlvar() #; //amount of moles of the material (all phases) for all components.
        self.f = controlvar.controlvar() #; //fraction.  Vapour molar fraction.
        self.U = controlvar.controlvar() #; //Joule. Internal energy.
        self.umolar = controlvar.controlvar() #;
        self.relativehumidity = controlvar.controlvar() #;
        self.composition = list() #new List<component>();

        self.init(acomposition, aTemp, aV, aP, af)

        #//P.simvector = new double[global.SimIterations];
        #//T.simvector = new double[global.SimIterations];
        #//f.simvector = new double[global.SimIterations];
        #//n.simvector = new double[global.SimIterations];
        #//U.simvector = new double[global.SimIterations];
        #density.simvector = new double[global.SimVectorLength];


    def copyfrom(self, materialcopyfrom):  #material materialcopyfrom
        self.P.v = materialcopyfrom.P.v #; //Pa
        self.V.v = materialcopyfrom.V.v #; //m3.  This will be total stage volume in the case of a distillation column.
        self.vmolar.v = materialcopyfrom.vmolar.v #; //m3/mole.  Total volume per mole for the total material all phases.
        self.vmolarL.v = materialcopyfrom.vmolarL.v #; //m3/mole.  Total volume per mole for the total liquid phase.
        self.vmolarV.v = materialcopyfrom.vmolarV.v #; //m3/mole.  Total volume per mole for the total vapour phase.
        self.density.v = materialcopyfrom.density.v #; //kg/m3
        self.T.copyfrom(materialcopyfrom.T) #; //Kelvin
        self.mass.v = materialcopyfrom.mass.v #; //kg
        self.n.v = materialcopyfrom.n.v #; //amount of moles of the material (all phases) for all components.
        self.f.v = materialcopyfrom.f.v #; //fraction.  Vapour molar fraction.
        self.U.v = materialcopyfrom.U.v #; //Joule. Internal energy.
        self.relativehumidity.v = materialcopyfrom.relativehumidity.v

        self.x = copy.deepcopy(materialcopyfrom.x)  #Array.Copy(materialcopyfrom.x, x, materialcopyfrom.x.Length); //Molar fraction of the total liquid of the material per component.
        self.y = copy.deepcopy(materialcopyfrom.y)  #Array.Copy(materialcopyfrom.y, , materialcopyfrom.y.Length); //Molar fraction of the total vapour of the material per component.
        self.hL = materialcopyfrom.hL #; //Joule/mol.  Molar enthalpy for the liquid phase, e.g. on a stage in a distillation column.
        self.hV = materialcopyfrom.hV #; //Joule/mol.  Molar enthalpy for the vapour phase, e.g. on a stage in a distillation column.
        self.ML = materialcopyfrom.ML #; //moles.  Total molar liquid hold-up.
        self.MV = materialcopyfrom.MV #; //moles.  Total molar vapour hold-up.
        self.z = copy.deepcopy(materialcopyfrom.z) #Array.Copy(materialcopyfrom.z, z, materialcopyfrom.z.Length); //fraction.  Molar fraction per component of the total moles in the material.

        self.umolar.v = materialcopyfrom.umolar.v  #; //Joule/mol.  Molar internal energy.
        self.umolarL = copy.deepcopy(materialcopyfrom.umolarL) #Array.Copy(materialcopyfrom.umolarL, umolarL, materialcopyfrom.umolarL.Length); //Joule/mol.  Molar internal energy for the total liquid phase.
        self.umolarV = copy.deepcopy(materialcopyfrom.umolarV) #Array.Copy(materialcopyfrom.umolarV, umolarV, materialcopyfrom.umolarV.Length); //Joule/mol.  Molar internal energy for the total vapour phase.
        self.totalumolar = materialcopyfrom.totalumolar; #this one was a local var in the C#//last calculation of the total vmolar;
        self.umolarideal = copy.deepcopy(materialcopyfrom.umolarideal) #  Array.Copy(materialcopyfrom.umolarideal, umolarideal, materialcopyfrom.umolarideal.Length); //Joule/mol.  Molar internal energy for the ideal gas case.
        self.fugacityL = copy.deepcopy(materialcopyfrom.fugacityL) #Array.Copy(materialcopyfrom.fugacityL, fugacityL, materialcopyfrom.fugacityL.Length); //fugacity per component for the liquid phase.
        self.fugacityV = copy.deepcopy(materialcopyfrom.fugacityV) #Array.Copy(materialcopyfrom.fugacityV, fugacityV, materialcopyfrom.fugacityV.Length); //fugacity per component for the vapour phase.
        self.aT = copy.deepcopy(materialcopyfrom.aT) #Array.Copy(materialcopyfrom.aT, aT, materialcopyfrom.aT.Length); //kg⋅m^5 /( s^2 ⋅mol^2 ); figure used in Peng Robinson equation.
        self.ac = copy.deepcopy(materialcopyfrom.ac) #Array.Copy(materialcopyfrom.ac, ac, materialcopyfrom.ac.Length); // kg⋅m^5 / (s^2 ⋅mol^2 ) ; figure used in Peng Robinson equation.
        self.alpha = copy.deepcopy(materialcopyfrom.alpha) #Array.Copy(materialcopyfrom.alpha, alpha, materialcopyfrom.alpha.Length); //part of the equation for aT, and used in other equations in the Peng Robinson collection.
        self.b = copy.deepcopy(materialcopyfrom.b) #Array.Copy(materialcopyfrom.b, b, materialcopyfrom.b.Length);  // m^3/mol ; figure used in Peng Robinson equation.
        self.K = copy.deepcopy(materialcopyfrom.K) #Array.Copy(materialcopyfrom.K, K, materialcopyfrom.K.Length);  //dimensionless - depends on omega.
        self.A = copy.deepcopy(materialcopyfrom.A) #Array.Copy(materialcopyfrom.A, A, materialcopyfrom.A.Length);  //used in equation for compressibility factor.
        self.B = copy.deepcopy(materialcopyfrom.B) #Array.Copy(materialcopyfrom.B, B, materialcopyfrom.B.Length);  //used in equation for compressibility factor.
        self.Z = copy.deepcopy(materialcopyfrom.Z) #Array.Copy(materialcopyfrom.Z, Z, materialcopyfrom.Z.Length);  //Compressibility factor. More than one value should be present based on the amount of phases in the material
        self.discriminantZ = copy.deepcopy(materialcopyfrom.Z) # Array.Copy(materialcopyfrom.discriminantZ, discriminantZ, materialcopyfrom.discriminantZ.Length); //The discriminant of the cubig PR equation for Z;
        self.Tr = copy.deepcopy(materialcopyfrom.Tr) # Array.Copy(materialcopyfrom.Tr, Tr, materialcopyfrom.Tr.Length); //reduced temperature.
        self.acomp = copy.deepcopy(materialcopyfrom.acomp) #  Array.Copy(materialcopyfrom.acomp, acomp, materialcopyfrom.acomp.Length); //Cubic equation for compressibility factor coeficients.
        self.bcomp = copy.deepcopy(materialcopyfrom.bcomp) #Array.Copy(materialcopyfrom.bcomp, bcomp, materialcopyfrom.bcomp.Length); //Cubic equation for compressibility factor coeficients.
        self.ccomp = copy.deepcopy(materialcopyfrom.ccomp) # Array.Copy(materialcopyfrom.ccomp, ccomp, materialcopyfrom.ccomp.Length); //Cubic equation for compressibility factor coeficients.
        self.dcomp = copy.deepcopy(materialcopyfrom.dcomp) #  Array.Copy(materialcopyfrom.dcomp, dcomp, materialcopyfrom.dcomp.Length); //Cubic equation for compressibility factor coeficients.
        self.bs = materialcopyfrom.bs#; #//Used in scarlet cubic solver. bs for bscarlet, This is for another cubic solver: http://home.scarlet.be/~ping1339/cubic.htm
        self.cs = materialcopyfrom.cs#; //Used in scarlet cubic solver.
        self.ds = materialcopyfrom.ds#; //Used in scarlet cubic solver.
        self.rs = materialcopyfrom.rs#; // Used in scarlet cubic solver.
        self.es = materialcopyfrom.es#; //Used in scarlet cubic solver.
        self.fs = materialcopyfrom.fs#; //Used in scarlet cubic solver.
        #public complex[] zs; //Used in scarlet cubic solver. I DO NOT THINK WE NEED TO COPY THESE VALUES AS THEY ARE INITED ON EACH ITERATION.
         #   //public complex[] us; //Used in scarlet cubic solver.
         #   //public complex[] ys; //Used in scarlet cubic solver.


        self.delta0  = copy.deepcopy(materialcopyfrom.delta0) #Array.Copy(materialcopyfrom.delta0, delta0, materialcopyfrom.delta0.Length); //used to solve the cubic equation for Z.
        self.delta1 = copy.deepcopy(materialcopyfrom.delta1) #Array.Copy(materialcopyfrom.delta1, delta1, materialcopyfrom.delta1.Length); //used to solve the cubic equation for Z.
        self.C = copy.deepcopy(materialcopyfrom.C) #copy.deepcopy(Array.Copy(materialcopyfrom.C, C, materialcopyfrom.C.Length); //used to solve the cubic equation for Z.
        self.Cc = copy.deepcopy(materialcopyfrom.Cc) #Array.Copy(materialcopyfrom.Cc, Cc, materialcopyfrom.Cc.Length); //used to solve the cubic equation for Z.
        self.a = copy.deepcopy(materialcopyfrom.a) #Array.Copy(materialcopyfrom.a, a, materialcopyfrom.a.Length); //used to solve the cubid equation for Z by making use of an alternative closed form formulat for them.
        self.Qc = copy.deepcopy(materialcopyfrom.Qc) #Array.Copy(materialcopyfrom.Qc, Qc, materialcopyfrom.Qc.Length); //used in alternative formula.
        self.Rc = copy.deepcopy(materialcopyfrom.Rc) #Array.Copy(materialcopyfrom.Rc, Rc, materialcopyfrom.Rc.Length); //used in alternative formula.
        self.Dc = copy.deepcopy(materialcopyfrom.Dc) # Array.Copy(materialcopyfrom.Dc, Dc, materialcopyfrom.Dc.Length); //used in alternative formula.
        self.Sc = copy.deepcopy(materialcopyfrom.Sc) #Array.Copy(materialcopyfrom.Sc, Sc, materialcopyfrom.Sc.Length); //used in alternative formula.
        self.Tc = copy.deepcopy(materialcopyfrom.Tc) #Array.Copy(materialcopyfrom.Tc, Tc, materialcopyfrom.Tc.Length); //used in alternative formula.
        self.Cp = copy.deepcopy(materialcopyfrom.Cp)  # Array.Copy(materialcopyfrom.Cp, Cp, materialcopyfrom.Cp.Length); //Heat capacity of constant pressure for an ideal gas type scenario per component.

        self.totalCp = materialcopyfrom.totalCp #; //Heat capacity of the material in totallity, with all its components includded.
        self.xvector = copy.deepcopy(materialcopyfrom.xvector) # Array.Copy(materialcopyfrom.xvector, xvector, materialcopyfrom.xvector.Length)
            #//public matrix jacobian; //The jacobian matrix for the system of equations as defined below in fflash().
        self.uvflashsize = materialcopyfrom.uvflashsize #; //The size of the k variables k equations problem to be solved for the UV flash.
        self.origuvflashsize = materialcopyfrom.origuvflashsize


        self.copycompositiontothismat(materialcopyfrom)
        self.massofonemole = materialcopyfrom.massofonemole #; //kg/mole
        self.volumeofonemole = materialcopyfrom.volumeofonemole #; //m^3/mole
        self.phase = materialcopyfrom.phase 

        #    //componentindex = materialcopyfrom.componentindex; 


    def copycompositiontothismat(self, amat): #material amat
        self.composition = []
        for i in range(len(amat.composition)):
            self.composition.append(component.component())
            self.composition[-1].copytothisobject(amat.composition[i])
            #//componentindex = i; //this will fall away later when there is more than one component per stream.
            self.composition[-1].molefraction = amat.composition[i].molefraction
            #//composition[composition.Count - 1].n = amat.composition[i].n / amat.n.v * n.v;  //this one will need to be tested might not be right.
    
    
    @staticmethod
    def copycompositiontothiscomposition(compositioncopyto, compositioncopyfrom):
        #ref List<component> compositioncopyto, List<component> compositioncopyfrom
        compositioncopyto = []
        for i in len(compositioncopyfrom):
            compositioncopyto.append(component.component())
            compositioncopyto[-1].copytothisobject(compositioncopyfrom[i])
            compositioncopyto[-1].molefraction = compositioncopyfrom[i].molefraction



    def init(self, acomposition, aTemp, aV, aP, af):
            #public void init(List<component> acomposition, double aTemp, double aV, double aP, double af)
        self.phase = globe.MaterialInitPhase

        self.composition = []
        for i in range(len(acomposition)):
            #//if (global.fluidpackage[i].m.name == componentname)
            #//{
            self.composition.append(component.component())

            self.composition[-1].copytothisobject(acomposition[i])
            #//componentindex = i; //Should not be needed anymore soon.
            #//}
        self.x = [0.0]*len(self.composition)
        self.y = [0.0]*len(self.composition)
        self.z = [0.0]*len(self.composition)
        self.fugacityL = [0.0]*len(self.composition)
        self.fugacityV = [0.0]*len(self.composition)
        self.K = [0.0]*len(self.composition)

        self.Z = list()
        for i in range(len(self.composition)):
            self.Z.append([0.0]*6)
            self.nullZ(i)

        self.discriminantZ = [0.0]*len(self.composition)
        self.Tr = [0.0]*len(self.composition)
        self.ac = [0.0]*len(self.composition)
        self.aT = [0.0]*len(self.composition)
        self.alpha = [0.0]*len(self.composition)
        self.b = [0.0]*len(self.composition)
        self.A = [0.0]*len(self.composition)
        self.B = [0.0]*len(self.composition)
        self.delta0 = [0.0]*len(self.composition)
        self.delta1 = [0.0]*len(self.composition)
        self.C = [0.0]*len(self.composition)
        self.Cc = [0.0]*len(self.composition)
        #//for (int i = 0; i < composition.Count; i++)
        #//{
        #//    Cc[i] = new complex(0, 0);
        #//}


        self.volumeofonemole = 0.0
        self.Cp = [0.0]*len(self.composition)
        self.totalCp = 0

        self.hL = 0.0  #Joule/mol.  Molar enthalpy for the liquid phase, e.g. on a stage in a distillation column.
        self.hV = 0.0 #Joule/mol.  Molar enthalpy for the vapour phase, e.g. on a stage in a distillation column.
        self.ML = 0.0  #moles.  Total molar liquid hold-up.
        self.MV = 0.0  #moles.  Total molar vapour hold-up.

        self.totalumolar = 0.0
        self.umolarL = [0.0]*len(self.composition)
        self.umolarV = [0.0]*len(self.composition)
        self.umolarideal = [0.0]*len(self.composition)

        self.acomp = [0.0]*len(self.composition) #//Cubic equation for compressibility factor coeficients.
        self.bcomp = [0.0]*len(self.composition) #//Cubic equation for compressibility factor coeficients.
        self.ccomp = [0.0]*len(self.composition) #//Cubic equation for compressibility factor coeficients.
        self.dcomp = [0.0]*len(self.composition) #//Cubic equation for compressibility factor coeficients.

        self.a = list()
        for i in range(len(self.composition)): self.a.append([0.0]*3)

        self.Qc = [0.0]*len(self.composition) #  new double[composition.Count]; //used in alternative formula.
        self.Rc = [0.0]*len(self.composition) #new double[composition.Count]; //used in alternative formula.
        self.Dc = [0.0]*len(self.composition) #new double[composition.Count]; //used in alternative formula.
        self.Sc = [complex()]*len(self.composition) #new complex[composition.Count]; //used in alternative formula.
        self.Tc = [complex()]*len(self.composition) #new complex[composition.Count]; //used in alternative formula.

        self.zs = [complex()]*6 # //Used in scarlet cubic solver.
        self.us = [complex()]*2 #new complex[2]; //Used in scarlet cubic solver.
        self.ys = [complex()]*6 # //Used in scarlet cubic solver.

        self.uvflashsize = 2 * len(self.composition) + 3
        self.xvector = [0.0]*self.uvflashsize
        for i in range(len(self.composition)):
            self.x[i] = 1.0 / (len(self.composition)) # //Add 0.5 to get starting values that can converge.
            self.y[i] = 1.0 / (len(self.composition))
        if (len(self.composition) == 1): self.uvflashsize = 3 #//x and y does not need to be part of the model anymore.
        self.origuvflashsize = self.uvflashsize

        self.jacobian = np.matrix(np.zeros((self.uvflashsize, self.uvflashsize)))

        self.PTfVflash(aTemp, aV, aP, af)
        #//calccompz(); Already done in the previous flash ptfv



    def setxybasedonf(self): #/If f = 0 or f = 1, then the values of x and y can be preset based on z and full flashing is not needed
            #public void setxybasedonf()
        for i in range(len(self.composition)):
            if (self.f.v == 0):
                self.x[i] = self.z[i]
                self.y[i] = 0
            elif (self.f.v == 1):
                self.x[i] = 0
                self.y[i] = self.z[i]



    def PTfVflash(self, aTemp, aV, aP, af):
            #public void PTfVflash(double aTemp, double aV, double aP, double af)
        #//composition.Clear();
        #//for (int i = 0; i < acomposition.Count; i++)
        #//{
        #//    //if (global.fluidpackage[i].m.name == componentname)
        #//    //{
        #//    composition.Add(new component());

        #//    composition[composition.Count - 1].copytothisobject(acomposition[i]);
        #//    //componentindex = i;
        #//    //}
        #//}

        self.P.v = aP
        self.T.v = aTemp
        self.f.v = af
        self.V.v = aV
        self.calccompz()
        self.setxybasedonf()
        self.mapvarstox() #; //Variables are allocated according to the Flatby article sequence of equations.
        #//U.v = 10000000.0;
        #//uvflash();
        self.vmolar = controlvar.controlvar(self.calcvmolaranddensity())
        self.n.v = (self.V.v / self.vmolar.v)
        #//composition[0].n = n.v;  //ASSUMING ONLY ONE COMPONENT AT THE MOMENT.  Should not be needed anymore.

        #//calcn(); //Should not be needed anymore.
        self.calcmass()
        #//massofonemole = mass.v / n.v; Already caculated in calcvmolarandensity;

        self.umolar.v = self.calcumolar()
        self.U.v = self.n.v * self.umolar.v
        self.calctotalCp()
           


    def nullZ(self, j):
        for i in range(3):
            self.Z[j][i] = globe.ZNotDefined




        #//public void calcn() //This method could not be needed anymore.
        #//{
        #//    n.v = 0;
        #//    for (int i = 0; i < composition.Count; i++)
        #//    {
        #//        n.v += composition[i].n;
        #//    }
        #//}

        #//public void calcmassanddensity()
        #//{
        #//    calcn();
        #//    massofonemole = 0;
        #//    volumeofonemole = 0;
        #//    double masscontribution, volumecontribution, moleof1kg = 0;
        #//    for (int i = 0; i < composition.Count; i++)
        #//    {
        #//        moleof1kg += composition[i].massfraction / composition[i].m.molarmass;
        #//    }
        #//    for (int i = 0; i < composition.Count; i++)
        #//    {
        #//        composition[i].molefraction = composition[i].massfraction / composition[i].m.molarmass / moleof1kg;
        #//        masscontribution = composition[i].molefraction * composition[i].m.molarmass;
        #//        volumecontribution = masscontribution / (composition[i].m.density + 0.00001); //Adding a small number to negate 
        #//        //very singularities.
        #//        massofonemole += masscontribution;
        #//        volumeofonemole += volumecontribution;
        #//    }
        #//    density.v = massofonemole / volumeofonemole;
        #//}


    def calcmass(self):
        self.mass.v = 0.0
        for i in range(len(self.composition)):
            self.mass.v += self.n.v*self.composition[i].molefraction * self.composition[i].m.molarmass



    def match(self, aname):    #public component match(string aname)
        c = None
        for i in range(len(self.composition)):
            if (self.composition[i].m.name == aname): c = self.composition[i]

        return c


        #//public double totalmolefraction()
        #//{
        #//    double total = 0;
        #//    for (int i = 0; i < composition.Count; i++) { total += composition[i].molefraction; } //This should now be adding up to 100%, if it
        #//    //does not add up, then a scaling will need to
        #//    //be done in order to have the total to be 100%
        #//    return total;
        #//}

    def copycompositiontothisobject(self, m):    #public void copycompositiontothisobject(material m)
        for i in range(len(self.composition)):
            self.composition[i].copytothisobject(m.composition[i])


    def mapvarstox(self):   # //Variables are allocated according to the Flatby article sequence of equations.
        self.xvector[0] = self.T.v
        self.xvector[1] = self.P.v
        self.xvector[2] = self.f.v
        for i in range (len(self.composition)):
            self.xvector[3 + i] = self.x[i]
            self.xvector[3 + len(self.composition) + i] = self.y[i]




    def mapxtovars(self):  # //Variables are allocated according to the Flatby article sequence of equations.
        self.T.v = self.xvector[0]
        self.P.v = self.xvector[1]
        self.f.v = self.xvector[2]

        for i in range(len(composition)):
            self.x[i] = self.xvector[3 + i]
            self.y[i] = self.xvector[3 + composition.Count + i]




    def calcxk(self, u, j):  #private complex calcxk(complex u, int j)
        return -1.0 / (3.0 * self.acomp[j]) * (self.bcomp[j] + u * self.Cc[j] + self.delta0[j] / (u * self.Cc[j]))


    def angle(self, comp): #c is complex
        if (comp.imag == 0 and comp.real < 0): return -math.pi
        elif (comp.real == 0 and comp.imag > 0): return math.pi / 2.0
        elif (comp.real == 0 and comp.imag < 0): return -math.pi / 2.0
        else: return math.atan(comp.imag / comp.real)

    
    def complex_pow(self, comp, y, n = 0):
            #public static complex pow(complex x, double y, int n = 0) //the specific root that is looked for will be specified here.  Could be a number between 0 and 1/y.  
            #//This is assuming that y is smaller than 1.
        #These are all local variables
        r = float(abs(comp))
        al = self.angle(comp)
        newr = r**y
        newalpha = 0.0
        if (y < 1):
            newalpha = al * y + 2.0 * math.pi * y * n
        else:
            newalpha = al * y
        ans = complex(newr * math.cos(newalpha), newr * math.sin(newalpha))
        return ans


    def compcomplex(self, x, y): #x and y are complex()
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


    def calcZ(self, j):   #public void calcZ(int j)
                #//Calculate the roots of the compressibility equation for the particular component.
        if (self.composition[j].m.omega <= 0.49):
            self.K[j] = 0.37464 + 1.54226 * self.composition[j].m.omega - \
            0.26992 * self.composition[j].m.omega**2.0
        else:
            self.K[j] = 0.379642 + 1.48503 * self.composition[j].m.omega - \
            0.164423 * self.composition[j].m.omega**2.0 + 0.016666 * self.composition[j].m.omega**3.0

        self.Tr[j] = self.xvector[0] / self.composition[j].m.Tc # //T / composition[j].m.Tc;
        self.ac[j] = 0.45724 * globe.R**2.0 * self.composition[j].m.Tc**2.0 / self.composition[j].m.Pc
        self.alpha[j] = (1 + self.K[j] * (1 - math.sqrt(self.Tr[j])))**2.0
        self.aT[j] = self.alpha[j] * self.ac[j]
        self.b[j] = 0.07780 * globe.R * self.composition[j].m.Tc / self.composition[j].m.Pc
        self.A[j] = self.aT[j] * self.xvector[1] / (globe.R**2.0 * self.xvector[0]**2.0) #//xvector[1]: P
        self.B[j] = self.b[j] * self.xvector[1] / (globe.R * self.xvector[0])

        self.acomp[j] = 1.0
        self.bcomp[j] = (self.B[j] - 1.0)
        self.ccomp[j] = self.A[j] - 2.0 * self.B[j] - 3.0 * self.B[j]**2.0
        self.dcomp[j] = self.B[j]**3.0 + self.B[j]**2.0 - self.A[j] * self.B[j]

        #//Delta = 18abcd -4b^3d + b^2c^2 - 4ac^3 - 27a^2d^2
        self.discriminantZ[j] = 18.0 * self.acomp[j] * self.bcomp[j] * self.ccomp[j] * self.dcomp[j] - \
                4.0 * self.bcomp[j]**3.0 * self.dcomp[j] + self.bcomp[j]**2.0 * self.ccomp[j]**2.0 - \
                4.0 * self.acomp[j] * self.ccomp[j]**3.0 - 27.0 * self.acomp[j]**2.0 * self.dcomp[j]**2.0

        #//Delta_0 = b^2-3 a c
        #//delta0[j] = Math.Pow(bcomp[j], 2.0) - 3.0 * acomp[j] * ccomp[j];

        #//Delta_1 = 2 b^3-9 a b c+27 a^2 d
        #//delta1[j] = 2.0 * Math.Pow(bcomp[j], 3.0) - 9.0 * acomp[j] * bcomp[j] * ccomp[j] + 27.0 * Math.Pow(acomp[j], 2.0) * dcomp[j];

        #//C[j] = Math.Pow((delta1[j] + Math.Sqrt(Math.Pow(delta1[j], 2.0) - 4.0 * Math.Pow(delta0[j], 3.0))) / 2.0, 1.0 / 3.0);

        #//Cc[j].a = Cc[j].b = 0.0;
        #//complex Coper = new complex(Math.Pow(delta1[j], 2.0) - 4.0 * Math.Pow(delta0[j], 3.0), 0.0);
        #//if (Coper < 0) { Cc[j].b = Math.Sqrt(-Coper); }
        #//else { Cc[j].a = Math.Sqrt(Coper); }
        #//Cc[j] = complex.Pow((delta1[j] - complex.Pow(Coper,0.5))/2.0, 1.0/3.0);

        self.nullZ(j)
        xk = [complex()]*3  #  local variable complex[] 
        #//complex[] u = new complex[] {new complex(1,00), new complex(-0.5,Math.Pow(3,0.5)/2.0), new complex(-0.5, -Math.Pow(3,0.5)/2.0)};

        #//Now an alternative way of getting the roots will be tried.  Wolfram algorithm.
        self.a[j][0] = self.dcomp[j] / self.acomp[j]
        self.a[j][1] = self.ccomp[j] / self.acomp[j]
        self.a[j][2] = self.bcomp[j] / self.acomp[j]
        #//Qc[j] = (3.0 * a[j][1] - Math.Pow(a[j][2], 2.0)) / 9.0;
        #//Rc[j] = (9.0 * a[j][2] * a[j][1] - 27.0 * a[j][0] - 2.0 * Math.Pow(a[j][2], 3.0)) / 54.0;
        #//Dc[j] = Math.Pow(Qc[j], 3.0) + Math.Pow(Rc[j], 3.0);
        #//Sc[j] = complex.pow(Rc[j] + complex.pow(Dc[j], 0.5), 1.0/3.0);
        #//Tc[j] = complex.pow(Rc[j] - complex.pow(Dc[j], 0.5), 1.0/3.0);
        #//xk[0] = -1.0 / 3.0 * a[j][2] + Sc[j] + Tc[j];
        #//xk[1] = -1.0 / 3.0 * a[j][2] - 1.0 / 2.0 * (Sc[j] + Tc[j]) + 1.0 / 2.0 * complex.I * Math.Pow(3.0, 0.5) * (Sc[j] - Tc[j]);
        #//xk[2] = -1.0 / 3.0 * a[j][2] - 1.0 / 2.0 * (Sc[j] + Tc[j]) - 1.0 / 2.0 * complex.I * Math.Pow(3.0, 0.5) * (Sc[j] - Tc[j]);

        #//This is still another algorithm for the solution.  The scarlet algorithm.  http://home.scarlet.be/~ping1339/cubic.htm

        #List<complex> xs = new List<complex>(); #local variable  //Used in scarlet cubic solver.
        xs = list() #will be list of complex()

        self.bs = self.a[j][2]
        self.cs = self.a[j][1]
        self.ds = self.a[j][0]
        self.rs = -self.bs / 3.0

        #//bs = 8.0/15.0;
        #//cs = -7.0/45.0;
        #//ds = -2.0/45.0;
        #//rs = -bs / 3.0;

        #//y^3  + (3 r + b) y^2  + (3 r^2  + 2 r b + c) y + r^3  + r^2  b + r c + d = 0
        #//y^3  + e y + f = 0
        self.es = 3.0 * self.rs**2.0 + 2 * self.rs * self.bs + self.cs
        self.fs = self.rs**3.0 + self.rs**2.0 * self.bs + self.rs * self.cs + self.ds

        bqz = self.fs; #local variable double//The b term of the quadratic equation in z
        cqz = -(self.es**3.0) / 27.0 #; #local variable

        self.us[0] = (-bqz + (((bqz**2.0) - 4 * cqz)**0.5)) / (2.0)
        self.us[1] = (-bqz - (((bqz**2.0) - 4 * cqz)**0.5)) / (2.0)

        self.zs[0] = self.complex_pow(self.us[0], 1.0 / 3.0, 0)
        self.zs[1] = self.complex_pow(self.us[0], 1.0 / 3.0, 1)
        self.zs[2] = self.complex_pow(self.us[0], 1.0 / 3.0, 2)
        self.zs[3] = self.complex_pow(self.us[1], 1.0 / 3.0, 0)
        self.zs[4] = self.complex_pow(self.us[1], 1.0 / 3.0, 1)
        self.zs[5] = self.complex_pow(self.us[1], 1.0 / 3.0, 2)

        temp = -self.es / 3.0

        self.ys[0] = self.zs[0] - self.es / (3.0 * self.zs[0])
        self.ys[1] = self.zs[1] - self.es / (3.0 * self.zs[1])
        self.ys[2] = self.zs[2] - self.es / (3.0 * self.zs[2])
        self.ys[3] = self.zs[3] - self.es / (3.0 * self.zs[3])
        self.ys[4] = self.zs[4] - self.es / (3.0 * self.zs[4])
        self.ys[5] = self.zs[5] - self.es / (3.0 * self.zs[5])

        xs.append(self.ys[0] - self.bs / 3.0)
        xs.append(self.ys[1] - self.bs / 3.0)
        xs.append(self.ys[2] - self.bs / 3.0)
        xs.append(self.ys[3] - self.bs / 3.0)
        xs.append(self.ys[4] - self.bs / 3.0)
        xs.append(self.ys[5] - self.bs / 3.0)

        #complexcomparer complexcompare = new complexcomparer();
        #xs.Sort(complexcompare);
        xs = sorted(xs, key=cmp_to_key(self.compcomplex))

        #print(xs)
        k = 1
        flag = True
        while flag:
            if (round(xs[k].real, 6) == round(xs[k - 1].real, 6)):
                xs.pop(k)  #index=k
            k += 1
            if k >= len(xs): flag = False



        #//int nbelow05 = 0; //nr of roots that are below 0.5.
        #//for (int k = 0; k < xs.Count; k++)
        #//{
        #//    if (xs[k].a < 0.5 && Math.Abs(xs[k].b) < global.ZeroImaginary) { nbelow05++; }
        #//}
        if (len(xs) == 3): xs.pop(1) # index=1#//Assume that the higher root value should be taken out.  To be verified.
        #//End of Scarlet algorithm.

        #various local variables: ints
        Zsvalid = 0
        Zsnotvalid = 0
        Zthatsvalid = 0
        Zthatsnotvalid = 0
        badZi = len(xs) - 1
        goodZi = 0
        rightiforZ = 0

        for k in range(len(xs)):
            #//xk[k] = calcxk(u[k], j);
            if (abs(xs[k].imag) < globe.ZeroImaginary and xs[k].real >= 0):
                self.Z[j][goodZi] = xs[k].real
                Zsvalid += 1
                Zthatsvalid = goodZi
                rightiforZ = goodZi
                #//for (int l = goodZi - 1; l >= 0; l--)
                #//{
                #//    if (Z[j][l] > Z[j][goodZi]) {rightiforZ = l;}
                #//}
                #//for (int m = goodZi; m > rightiforZ; m--)
                #//{
                #//    Z[j][m] = Z[j][m - 1];
                #//}
                #//Z[j][rightiforZ] = xk[k].a;

                goodZi += 1
            else:
                self.Z[j][badZi] = globe.ZNotDefined
                badZi -= 1
                Zsnotvalid += 1


        if (Zsvalid > 1):
            if (self.f.v == 0 or self.xvector[2] == 0):
                pass
                #//f.v = 0.1;
                #//xvector[2] = f.v;
            elif (self.f.v == 1 or self.xvector[2] == 1):
                pass
                #//f.v = 0.9;
                #//xvector[2] = f.v;
        elif (Zsvalid == 1):
            if (self.Z[j][Zthatsvalid] < 0.5 and len(self.composition) == 1):
                f.v = 0
                xvector[2] = f.v
             # //only liquid
            elif (self.Z[j][Zthatsvalid] > 0.5 and len(self.composition) == 1):
                self.f.v = 1
                self.xvector[2] = self.f.v
             # //only vapour

        dummy = 0  #local var
        for k in range(3):
            if (self.Z[j][k] == globe.ZNotDefined): self.Z[j][k] = self.Z[j][Zthatsvalid]




            #//if (discriminantZ[j] < 0) //Should be the case if there is only one phase of the molecule present
            #//{
            #//    Z[j][0] = -1 / (3 * acomp[j]) * (bcomp[j] + C[j] + delta0[j] / C[j]);
            #//    Z[j][1] = Z[j][0];
            #//}
            #//else
            #//{
            #//    Z[j][0] = (9*acomp[j]*dcomp[j] - bcomp[j]*ccomp[j])/(2*delta0[j]); //This should be the liquid root.
            #//    Z[j][1] = (4*acomp[j]*bcomp[j]*ccomp[j] - 9*Math.Pow(acomp[j],2)*dcomp[j] - Math.Pow(bcomp[j],3))/(acomp[j]*delta0[j]); //This should be the gas root.
            #//}


    def calcfugacity(self, j): #int j#//assume that Z has already been calculated for both roots.  Z[j][0] is the liquid root, Z[j][1] is the gas root.
        logtheta = [0.0, 0.0] #double[] logtheta = new double[] { 0, 0 };
        self.calcZ(j)
        for i in range(2):
            if (self.Z[j][i] != globe.ZNotDefined):
                logtheta[i] = (self.Z[j][i] - 1.0) - math.log(self.Z[j][i] - B[j]) - \
                        A[j] / (2.0 * math.sqrt(2.0) * B[j]) * math.log((self.Z[j][i] + \
                        (math.sqrt(2.0) + 1.0) * self.B[j]) / (self.Z[j][i] - (math.sqrt(2.0) - 1.0) * self.B[j]))

        self.fugacityL[j] = math.exp(logtheta[0]) * self.xvector[1]
        self.fugacityV[j] = math.exp(logtheta[1]) * self.xvector[1]
        #//if (Z[j][0] == global.ZNotDefined) {fugacityL[j] = fugacityV[j];}
        #//else if (Z[j][1] == global.ZNotDefined) { fugacityV[j] = fugacityL[j]; }


    def calcumolarwithZ(self, j, Zi):  #int j, int Zi
                #//calcs the molar internal energy for the given root of the Z equation, and for component j.
        return -self.A[j] / (self.B[j] * math.sqrt(8.0)) * (1.0 + self.K[j] * math.sqrt(self.Tr[j]) / \
                math.sqrt(self.alpha[j])) * \
                math.log((self.Z[j][Zi] + (1.0 + math.sqrt(2.0)) * self.B[j]) / (self.Z[j][Zi] + \
                (1.0 - math.sqrt(2.0)) * self.B[j])) * globe.R * self.xvector[0] +  \
                self.umolarideal[j]  # #//xvector[0]: T


    def calcumolarpercomponent(self):
        for j in range(len(self.composition)):
            self.calcZ(j)
            self.Cp[j] = self.composition[j].m.calcCp(self.xvector[0])
            self.umolarideal[j] = (self.Cp[j] - globe.R) * self.xvector[0]
            #//umolarideal[j] = 0.0;
            self.umolarL[j] = self.calcumolarwithZ(j, 0)
            self.umolarV[j] = self.calcumolarwithZ(j, 1)


    def calctotalCp(self):
        self.calccompz()
        self.totalCp = 0
        for i in range(len(self.composition)):
            self.totalCp += self.Cp[i]*self.z[i]


    def calcumolar(self):
        self.calcumolarpercomponent()
        totalumolarL = 0.0 #local var
        totalumolarV = 0.0 #local var
        for k in range(len(self.composition)):
            totalumolarL += self.umolarL[k] * self.xvector[3 + k]*self.composition[k].molefraction
            totalumolarV += self.umolarV[k] * self.xvector[3 + len(self.composition) + k] * \
                self.composition[k].molefraction
        totalumolar = (1 - self.xvector[2]) * totalumolarL + self.xvector[2] * totalumolarV  #; //f: xvector[2]
        return totalumolar


    def calcvmolaranddensity(self): 
        totalvmolar = 0.0 #local var
        totalvmolarL = 0.0 #local var
        totalvmolarV = 0.0 #local var
        self.massofonemole = 0.0
        for k in range(len(self.composition)):
            self.calcZ(k)
            totalvmolarL += self.b[k] * self.Z[k][0] / self.B[k] * self.xvector[3 + k] * self.composition[k].molefraction
            totalvmolarV += self.b[k] * self.Z[k][1] / self.B[k] * self.xvector[3 + len(self.composition) + k] * \
                self.composition[k].molefraction
            #//totalvmolarL += Z[k][0] * global.R * xvector[0] / (xvector[1] + 0.0000001) * xvector[3 + k];
            #//totalvmolarV += Z[k][1] * global.R * xvector[0] / (xvector[1] + 0.0000001) * xvector[3 + composition.Count + k];
            self.massofonemole += self.composition[k].m.molarmass * self.composition[k].molefraction

        totalvmolar = (1 - self.xvector[2]) * totalvmolarL + self.xvector[2] * totalvmolarV
        self.density.v = self.massofonemole / totalvmolar
        return totalvmolar


    def dfdx(self, fi, xi):  #dfdx(int fi, int xi)
        y0 = fflash(fi) #local var
        x0 = self.xvector[xi] #local var
        #//xvector[xi] *= global.epsilonfrac;
        self.xvector[xi] += globe.epsilonadd
        den = self.xvector[xi] - x0 #local var
        y1 = fflash(fi) #local var
        self.xvector[xi] = x0
        return (y1 - y0) / den


    def fflash(self, i):  #fflash(int i) //function that will define the functions to be solved for the UV flash
        ffreturn = 0.0 #local var; //the value that will be returned.
        if (i == 0): #//internal molar energy equation.
            ffreturn = self.umolar.v - calcumolar() #//f: xvector[2]
            return ffreturn

        elif (i == 1): #//molar volume equation
            #//vmolar = calcvmolar(); //We are nulling this equation just for this particular case now.
            ffreturn = self.vmolar.v - self.calcvmolaranddensity()
            return ffreturn

        elif (i >= 2 and i < len(composition) + 2): #//fugacity equation
            self.calcfugacity(i - 2)
            if (self.xvector[2] == 0.0): ffreturn = 0.0
            else:
                ffreturn = self.xvector[3 + len(self.composition) + i - 2] * self.fugacityV[i - 2] -  \
                        self.xvector[3 + i - 2] * self.fugacityL[i - 2]
             #//y[j]*fl[j] - x[j]*fv[j] }
            return ffreturn

        elif (i >= len(self.composition) + 2 and i < 2 * len(self.composition) + 2):  #//(1 - f)*x[j] + f*y[j] - z[j] 
            ffreturn = (1 - self.xvector[2]) * self.xvector[3 + (i - len(self.composition) - 2)] + \
                    self.xvector[2] * self.xvector[3 + len(self.composition) + (i - len(self.composition) - 2)] - \
                    self.z[i - len(self.composition) - 2]
            return ffreturn
        elif (i == 2 * len(self.composition) + 2): #//composition sum
            sum = 0 #local var
            for k in range(len(self.composition)):
                sum += xvector[3 + len(self.composition) + k] - self.xvector[3 + k]
            return sum

        else: return 0



    def calcjacobian(self):
        for r in range(len(self.uvflashsize)):
            for c in range(len(self.uvflashsize)):
                self.jacobian[r,c] = dfdx(r, c)


    def limitxvector(self):
        if (self.xvector[0] < 0.0): self.xvector[0] = 0.1 #//T
        if (self.xvector[1] < 0.0): self.xvector[1] = 0.1 #//P
        if (self.xvector[2] < 0.0): self.xvector[2] = 0.0 #//f
        elif (self.xvector[2] > 1.0): self.xvector[2] = 1.0


    def calccompz(self): #//method to calculate the molar fraction of each component in the material
        for i in range(len(self.composition)):
            self.z[i] = self.composition[i].molefraction


    def uvflash(self):
        self.lmatrix = np.matrix(np.zeros((uvflashsize, uvflashsize))) #all matrix objects
        self.umatrix = np.matrix(np.zeros((uvflashsize, uvflashsize)))
        self.deltax = np.matrix(np.zeros((uvflashsize, 1)))
        self.ymatrix = np.matrix(np.zeros((uvflashsize, 1)))
        self.bmatrix = np.matrix(np.zeros((uvflashsize, 1)))

        self.mapvarstox()
        #//calcn();  This calcn will need to come in later when more than once component can be better simulated by the simulation.
        self.umolar.v = self.U.v / self.n.v
        self.vmolar.v = self.V.v / self.n.v

        self.calccompz()

        for i in range(globe.NMaterialIterations):
            if (self.xvector[2] == 0.0 or self.xvector[2] == 1.0):
                self.uvflashsize = 2
            else: self.uvflashsize = self.origuvflashsize

            self.jacobian.resize((uvflashsize, uvflashsize))
            self.lmatrix.resize((uvflashsize, uvflashsize))
            self.umatrix.resize((uvflashsize, uvflashsize))
            self.deltax.resize((uvflashsize, 1))
            self.ymatrix.resize((uvflashsize, 1))
            self.bmatrix.resize((uvflashsize, 1))

            self.calcjacobian()
            #//jacobian.swoprowsinthematrix(1, 3);
            #//jacobian.ludecomposition(lmatrix, umatrix);
            #//jacobian.swoprowsinthematrix(2, 4);
            jacobian.ludecomposition(lmatrix, umatrix)
            #matrix tempm = lmatrix * umatrix;
            for j in range(self.uvflashsize):
                bmatrix[j,0] = -fflash(j)

            self.deltax = np.linalg.solve(jacobian, bmatrix)

            #matrix.solveLYequalsB(lmatrix, ymatrix, bmatrix);
            #matrix tempm2 = lmatrix * ymatrix;
            #matrix.solveUXequalsY(umatrix, deltax, ymatrix);
            #matrix tempm3 = umatrix * deltax;
            for j in range(self.uvflashsize):
                self.xvector[j] += self.deltax[j,0]
            self.limitxvector()
            self.f.v = self.xvector[2]

        self.mapxtovars()




        #//public void addtothisobject(material m)
        #//{
        #//    for (int i = 0; i < composition.Length; i++)
        #//    {
        #//        composition[i].massfraction += m.composition[i].massfraction;
        #//    }
        #//}

    def zero(self):
        for i in range(len(self.composition)):
            self.composition[i].n = 0



    def update(self, simi, historise):   #(int simi, bool historise)
        if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
            index = int(simi/globe.SimVectorUpdatePeriod)
            if (self.T.simvector != None): self.T.simvector[index] = self.T.v
            if (self.P.simvector != None): self.P.simvector[index] = self.P.v
            if (self.f.simvector != None): self.f.simvector[index] = self.f.v
            if (self.n.simvector != None): self.n.simvector[index] = self.n.v
            if (self.U.simvector != None): self.U.simvector[index] = self.U.v
            if (self.density.simvector != None): self.density.simvector[index] = self.density.v



        
