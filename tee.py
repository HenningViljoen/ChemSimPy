from unitop import unitop
import globe as globe
import utilities as utilities
from mixer import mixer
from teeproperties import teeproperties
import copy
from stream import stream
from point import point
import numpy as np
import math


class tee(unitop):
    def __init__(self, anr, ax, ay, anout):
                #public tee(int anr, double ax, double ay, int anout)
                #: base(anr, ax, ay, 1, anout)
        super(tee, self).__init__(anr, ax, ay, 1, anout)
        self.inittee()


    def teecopyconstructor(self, baseclasscopyfrom):
                #public tee(baseclass baseclasscopyfrom)
                #: base(0, 0, 0, 1, ((tee)baseclasscopyfrom).nout) 
        self.inittee()
        self.copyfrom(baseclasscopyfrom)


    def inittee(self):
        self.objecttype = globe.objecttypes.Tee
        self.name = 'Tee ' + str(self.nr)

        #//inflow[0] = new stream(0, ax, ay, ax, ay)

        self.teeinitradius = globe.TeeInitRadiusDefault
        self.linkedmixer = None  #mixer object//Every tee will now have a mixer that is linked to it, so that the flows into the different branches of the tee can 
                                   #// be dynamically calculated during the simulation to make sure all flows into the mixer, has the same pressure.
        self.k = list()  #//Array of constants that will relate F^2*k^2 = deltaP^2 over each branch between the tee and the mixer.
        self.branchmassflow = list()  #double[]//kg/s.  Array of mass flows per branch.
        self.branchdp = list() #double[] //Pascal.  Array of DPs from the tee to the mixer.
        
        self.initk()
        self.initbranchflows()
        self.initbranchdp()

        self.updateinoutpointlocations()


    def copyfrom(self, baseclasscopyfrom):
        teecopyfrom = baseclasscopyfrom

        super(tee, self).copyfrom(teecopyfrom)
        #base.copyfrom(teecopyfrom)

        self.teeinitradius = teecopyfrom.teeinitradius
        #//linkedmixer.copyfrom(teecopyfrom.linkedmixer);  //Every tee will now have a mixer that is linked to it, so that the flows into the different branches of the tee can 
        #//                           // be dynamically calculated during the simulation to make sure all flows into the mixer, has the same pressure.
        self.k = copy.deepcopy(teecopyfrom.k)  #//Array of constants that will relate F^2*k^2 = deltaP^2 over each branch between the tee and the mixer.
        self.branchmassflow = copy.deepcopy(teecopyfrom.branchmassflow) #//kg/s.  Array of mass flows per branch.
        self.branchdp = copy.deepcopy(teecopyfrom.branchdp) #//Pascal.  Array of DPs from the tee to the mixer.


    def initk(self):
        self.k = [0.0]*self.nout


    def initbranchflows(self):
        self.initoutflow()
        self.branchmassflow = [0.0]*self.nout
        for i in range(self.nout):
            self.outflow[i] = stream(i, self.location.x, self.location.y, self.location.x, self.location.y)
            self.outflow[i].massflow.v = self.inflow[0].massflow.v / self.nout  #//Initial value for the outflow until update method runs.


    def initbranchdp(self):
        self.branchdp = [0.0]*self.nout
        for i in range(self.nout):
            self.branchdp[i] = 0


    def update(self, simi, historise):  #public override void update(int simi, bool historise)
        if (self.linkedmixer != None):
            defaultbranchdp = self.inflow[0].mat.P.v - self.linkedmixer.outflow[0].mat.P.v #local var
            if (defaultbranchdp <= 0): defaultbranchdp = globe.Epsilon
            defaultbranchmassflow = self.inflow[0].massflow.v / self.nout  #local var
            if (defaultbranchmassflow == 0): defaultbranchmassflow = globe.Epsilon

            for i in range(self.nout):
                self.outflow[i].mat.copycompositiontothisobject(self.inflow[0].mat)
                self.outflow[i].mat.density = self.inflow[0].mat.density
                self.outflow[i].mat.T = self.inflow[0].mat.T
                #//outflow[i].mat.P = inflow[0].mat.P
                self.branchdp[i] = self.outflow[i].mat.P.v - self.linkedmixer.inflow[i].mat.P.v
                if (self.branchdp[i] <= 0):
                    self.branchdp[i] = defaultbranchdp
                #//{ 
                #//    branchdp[i] = 0;
                #//    nrbranchdpzero++;
                #//}
                if (self.branchmassflow[i] == 0):
                    self.branchmassflow[i] = defaultbranchmassflow
                self.k[i] = math.sqrt(self.branchdp[i]) / self.branchmassflow[i]

            #//Set-up matrices for sollution
            A = np.zeros((self.nout, self.nout))   #local var
            B = np.zeros((self.nout, 1))      #local var
            #matrix lmatrix = new matrix(nout, nout)  #local var
            #matrix umatrix = new matrix(nout, nout)  #local var
            x = np.zeros((self.nout, 1))  #local var
            #matrix ymatrix = new matrix(nout, 1)   #local var
            for r in range(self.nout - 1):
                A[r,r] = self.k[r]
                A[r,r + 1] = -self.k[r + 1]
            for c in range(self.nout):
                A[self.nout - 1,c] = 1
            B[self.nout - 1,0] = self.inflow[0].massflow.v

            #//Solve linear set of equations
            #A.ludecomposition(lmatrix, umatrix)
            #matrix tempm = lmatrix * umatrix
            #matrix.solveLYequalsB(lmatrix, ymatrix, B)
            #matrix tempm2 = lmatrix * ymatrix
            #matrix.solveUXequalsY(umatrix, x, ymatrix)
            #matrix tempm3 = umatrix * x
            x = np.linalg.solve(A, B)

            for j in range(self.nout):
                self.branchmassflow[j] = x[j,0]
            #//}
            totalbranchflow = 0.0 #local var
            for i in range(self.nout):
                totalbranchflow += self.branchmassflow[i]
            if (abs((totalbranchflow - self.inflow[0].massflow.v) / 
                (totalbranchflow + globe.Epsilon)) > globe.ConvergeDiffFrac):
                for i in range(self.nout):
                    self.branchmassflow[i] *= self.inflow[0].massflow.v / (totalbranchflow + globe.Epsilon)

            for j in range(self.nout):
                self.outflow[j].massflow.v = self.branchmassflow[j]
                #//outflow[j].massflow.v = inflow[0].massflow.v/2;
                #//outflow[j].massflow.v = 500000 / 3600.0;

            #//This section will now calculate the upstream pressure.
            massflowtouse = [0.0]*self.nout  #local var
            totalmassflowtouse = 0.0  #local var
            self.inflow[0].mat.P.v = 0.0 #this line was not in the original code, but I think it should be in and could
                                        #be a bug.
            for j in range(self.nout):
                if (self.inflow[0].massflow.v == 0):
                    massflowtouse[j] = 1.0
                else:
                    massflowtouse[j] = self.outflow[j].massflow.v
                totalmassflowtouse += massflowtouse[j]

            for j in range(self.nout):
                self.inflow[0].mat.P.v += self.outflow[j].mat.P.v * massflowtouse[j]

            self.inflow[0].mat.P.v /= (totalmassflowtouse)
        else: #//no linkedmixer, so in this case the dP is given to the network, and flows are calculated in each stream's unitops.
            totalinflow = 0.0  #local var
            #//inflow[0].massflow.v = 0;
            for j in range(self.nout):
                self.outflow[j].mat.P.v = self.inflow[0].mat.P.v
                self.outflow[j].mat.copycompositiontothisobject(self.inflow[0].mat)
                self.outflow[j].mat.density = self.inflow[0].mat.density
                self.outflow[j].mat.T = self.inflow[0].mat.T

                totalinflow += self.outflow[j].massflow.v
            self.inflow[0].massflow.v = totalinflow


    def updateinoutpointlocations(self):
        #//Update in and out point locations;
        self.inpoint[0].x = self.location.x + globe.TeeLength / 2
        self.inpoint[0].y = self.location.y
        for i in range(self.nout):
            self.outpoint[i].x = self.location.x - globe.TeeLength / 2
            self.outpoint[i].y = self.location.y - (self.nout - 1) / 2.0 * globe.TeeDistanceBetweenBranches + \
                    i * globe.TeeDistanceBetweenBranches

        super(tee, self).updateinoutpointlocations()


    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        diag = teeproperties(self, asim, aroot)


    def mouseover(self, x, y):  #public override bool mouseover(double x, double y)
        return (utilities.distance(x - self.location.x, y - self.location.y) <= self.teeinitradius)


    def draw(self, canvas):
        self.updateinoutpointlocations()

        #GraphicsPath plot1
        #Pen plotPen
        #float width = 1

        #plot1 = new GraphicsPath()
        #plotPen = new Pen(Color.Black, width)

        point0 = point(globe.OriginX + int(globe.GScale*(self.inpoint[0].x)), 
                    globe.OriginY + int(globe.GScale*(self.inpoint[0].y - globe.TeeBranchThickness/2)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.inpoint[0].x - globe.TeeLength/2)), 
                    globe.OriginY + int(globe.GScale*(self.inpoint[0].y - globe.TeeBranchThickness/2)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.inpoint[0].x - globe.TeeLength/2)), 
                    globe.OriginY + int(globe.GScale*(self.inpoint[0].y + globe.TeeBranchThickness/2)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.inpoint[0].x)),
                    globe.OriginY + int(globe.GScale*(self.inpoint[0].y + globe.TeeBranchThickness/2)))

        maininput = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)

        #Point[] input = new Point[] 
        #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[0].x)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(inpoint[0].y - global.TeeBranchThickness/2))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[0].x - global.TeeLength/2)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(inpoint[0].y - global.TeeBranchThickness/2))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[0].x - global.TeeLength/2)), 
         #           global.OriginY + Convert.ToInt32(global.GScale*(inpoint[0].y + global.TeeBranchThickness/2))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[0].x)),
        #            global.OriginY + Convert.ToInt32(global.GScale*(inpoint[0].y + global.TeeBranchThickness/2)))}

        #plot1.AddPolygon(input)

        x0 = globe.OriginX + int(globe.GScale * (self.location.x - globe.TeeBranchThickness / 2))
        y0 = globe.OriginY + int(globe.GScale * (self.location.y - (self.nout - 1) / 2.0 * \
            globe.TeeDistanceBetweenBranches))
        x1 = x0 + int(globe.GScale * (globe.TeeBranchThickness))
        y1 = y0 + int(globe.GScale * ((self.nout - 1) * globe.TeeDistanceBetweenBranches))

        upright = canvas.create_rectangle(x0, y0, x1, y1)

        if self.highlighted:
            canvas.itemconfig(upright, fill='red')
        else:
            canvas.itemconfig(upright, fill='black')

        #Rectangle upright = new Rectangle(
        #        global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.TeeBranchThickness / 2)),
        #        global.OriginY + Convert.ToInt32(global.GScale * (location.y - (nout - 1) / 2.0 * global.TeeDistanceBetweenBranches)),
        #        Convert.ToInt32(global.GScale * (global.TeeBranchThickness)),
        #        Convert.ToInt32(global.GScale * ((nout - 1) * global.TeeDistanceBetweenBranches)))
        #plot1.AddRectangle(upright)

        branches = list() #list of Rectangles
        #Rectangle[] branches = new Rectangle[nout]
        for i in range(self.nout):
            x0 = globe.OriginX + int(globe.GScale * (self.location.x - globe.TeeLength / 2))
            y0 = globe.OriginY + int(globe.GScale * (self.location.y - (self.nout - 1) / 2.0 * \
                globe.TeeDistanceBetweenBranches + i * globe.TeeDistanceBetweenBranches))
            x1 = x0 + int(globe.GScale * (globe.TeeLength / 2))
            y1 = y0 + int(globe.GScale * (globe.TeeBranchThickness))
            #branches[i] = new Rectangle(
            #        global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.TeeLength / 2)),
            #        global.OriginY + Convert.ToInt32(global.GScale * (location.y - (nout - 1) / 2.0 * global.TeeDistanceBetweenBranches +
            #        i * global.TeeDistanceBetweenBranches)),
            #        Convert.ToInt32(global.GScale * (global.TeeLength / 2)),
            #        Convert.ToInt32(global.GScale * (global.TeeBranchThickness)))
            rect = canvas.create_rectangle(x0, y0, x1, y1)
            branches.append(rect)
            #plot1.AddRectangle(branches[i])

        #plotPen.Color = Color.Black

        #SolidBrush brush = new SolidBrush(Color.Black)
        #if (highlighted) { brush.Color = Color.Orange; }
        #G.FillPath(brush, plot1)
        #G.DrawPath(plotPen, plot1)

        super(tee, self).draw(canvas)

