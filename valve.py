import unitop as unitop
import globe as globe
import math
import controlvar as controlvar
import point as point
import utilities as utilities
from valveproperties import valveproperties

class valve(unitop.unitop):
    def __init__(self, anr, ax, ay, aCv, aop):
                #public valve(int anr, double ax, double ay, double aCv, double aop)
                #: base(anr, ax, ay, 1, 1)
        super(valve, self).__init__(anr, ax, ay, 1, 1)

        #//variables
        self.deltapressure = controlvar.controlvar()#//Pa  public controlvar 
        #//public double[] deltapressuresimvector #//Pa; history sim vector.
        self.Cv = 0.0 #//Valve coeficient, public double 
        self.op = controlvar.controlvar() #//Fraction : valve opening as a fraction, public controlvar 
        #//public double[] opsimvector

        self.deltapressurenew = 0.0; #//Pa, public double 
        self.ddeltapressuredt = 0.0; #//Pa/s, public double 

        self.initvalve(anr, ax, ay, aCv, aop)
    


    def valvecopyconstructor(self, baseclasscopyfrom):
    #public valve(baseclass baseclasscopyfrom)
            #: base(0, 0, 0, 1, 1) //these numbes do not matter much since they will be sorted anyway by the copymethods down the 
                                    #//hierarchy
        self.initvalve(0, 0, 0, 0, 0)
        self.copyfrom(baseclasscopyfrom)



    def initvalve(self, anr, ax, ay, aCv, aop):
                #public void initvalve(int anr, double ax, double ay, double aCv, double aop)
        self.objecttype = globe.objecttypes.Valve

        self.deltapressure = controlvar.controlvar()
        self.op = controlvar.controlvar()

        self.name = str(self.nr) + " " + str(self.objecttype)

        self.controlpropthisclass = []
        self.controlpropthisclass = ["deltapressure", "op"]
        self.nrcontrolpropinherited = len(self.controlproperties)
        self.controlproperties = self.controlproperties + self.controlpropthisclass

        self.Cv = aCv
        self.op.v = aop
        self.deltapressure.v = 0.0
            #//deltapressuresimvector = new double[global.SimVectorLength]
            #//opsimvector = new double[global.SimVectorLength]

        self.actualvolumeflow.v = 0.0

        self.deltapressurenew = 0.0 # //Pa
        self.ddeltapressuredt = 0.0

        self.updateinoutpointlocations()

        self.update(0, False)
    

    def copyfrom(self, baseclasscopyfrom):
        valvecopyfrom = baseclasscopyfrom
        #valve valvecopyfrom = (valve)baseclasscopyfrom

        super(valve, self).copyfrom(valvecopyfrom)
        #base.copyfrom(valvecopyfrom)

        self.deltapressure.v = valvecopyfrom.deltapressure.v #//Pa
        self.Cv = valvecopyfrom.Cv #//Valve coeficient
        self.op.v = valvecopyfrom.op.v #//Fraction : valve opening as a fraction

        self.deltapressurenew = valvecopyfrom.deltapressurenew #//Pa
        self.ddeltapressuredt = valvecopyfrom.ddeltapressuredt


    def selectedproperty(self, selection):
        #public override controlvar selectedproperty(int selection)
        if (selection >= self.nrcontrolpropinherited):
            diff = selection - self.nrcontrolpropinherited
            if diff == 0:
                return self.deltapressure
            elif diff == 1:
                return self.op
            else:
                return None
        else: return super(valve, self).selectedproperty(selection)


    def ddt(self, simi):
        #public void ddt(int simi)
        self.ddeltapressuredt = -1 / globe.ValveHydraulicTau * self.deltapressure.v + \
            1 / globe.ValveHydraulicTau * self.deltapressurenew



    def update(self, simi, historise):
        #public override void update(int simi, bool historise)
        if (self.inflow[0] != None and self.outflow[0] != None):
            self.mat.copycompositiontothisobject(self.inflow[0].mat)
            self.mat.density.v = self.inflow[0].mat.density.v
            self.mat.T.v = self.inflow[0].mat.T.v
            self.massflow.v = self.inflow[0].massflow.v
            self.actualvolumeflow.v = self.massflow.v/self.mat.density.v
            self.deltapressurenew = math.pow(self.actualvolumeflow.v / (self.Cv * math.pow(globe.ValveEqualPercR, self.op.v - 1)), 2)
            self.ddt(simi)
            self.deltapressure.v += self.ddeltapressuredt * globe.SampleT       
            self.inflow[0].mat.P.v = self.outflow[0].mat.P.v + self.deltapressure.v   
            self.calcmolarflowfrommassflow()
            self.calcstandardflowfrommoleflow()
            self.outflow[0].mat.copycompositiontothisobject(self.mat)
            self.outflow[0].massflow.v = self.massflow.v
            self.outflow[0].mat.density.v = self.mat.density.v
            self.outflow[0].mat.T.v = self.mat.T.v

        #//if (op.v > 1) { op.v = 1 }
        if (self.op.v < 0.00): self.op.v = 0.00

        if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
            index = int(simi / globe.SimVectorUpdatePeriod)
            if (self.deltapressure.simvector != None):
                self.deltapressure.simvector[index] = self.deltapressure.v
            if (self.op.simvector != None): self.op.simvector[index] = self.op.v
            if (self.actualvolumeflow.simvector != None):
                self.actualvolumeflow.simvector[index] = self.actualvolumeflow.v
            if (self.standardvolumeflow.simvector != None):
                self.standardvolumeflow.simvector[index] = self.standardvolumeflow.v
            if (self.massflow.simvector != None):
                self.massflow.simvector[index] = self.massflow.v
            if (self.molarflow.simvector != None):
                self.molarflow.simvector[index] = self.molarflow.v              



        #//public void sizevalvefromstandardflow()
        #//{
        #//    calcmassflowfromstandardflow();
        #//    calcactualvolumeflowfrommassflow();
        #//    if (Math.Abs(deltapressure) > 0) { Cv = actualvolumeflow / (op * Math.Sqrt(Math.Abs(deltapressure))); }
        #//}


    def sizevalvefromactualvolumeflow(self):
        if (abs(self.deltapressure.v) > 0):
            self.Cv = self.actualvolumeflow.v / (self.op.v * math.sqrt(abs(self.deltapressure.v)))
    


    def showtrenddetail(self):
        if not self.detailtrended:
            self.detailtrended = True
            self.allocatememory()
        else:
            self.detailtrended = False
            self.deallocatememory()


    def allocatememory(self):
        if (self.deltapressure.simvector == None):
            self.deltapressure.simvector = [0.0]*globe.SimVectorLength
        if (self.op.simvector == None):
            self.op.simvector = [0.0]*globe.SimVectorLength
        if (self.actualvolumeflow.simvector == None):
            self.actualvolumeflow.simvector = [0.0]*globe.SimVectorLength
        if (self.standardvolumeflow.simvector == None):
            self.standardvolumeflow.simvector = [0.0]*globe.SimVectorLength
        if (self.massflow.simvector == None):
            self.massflow.simvector = [0.0]*globe.SimVectorLength
        if (self.molarflow.simvector == None):
            self.molarflow.simvector = [0.0]*globe.SimVectorLength


    def deallocatememory(self):
        self.deltapressure.simvector = None
        self.op.simvector = None
        self.actualvolumeflow.simvector = None
        self.standardvolumeflow.simvector = None
        self.massflow.simvector = None
        self.molarflow.simvector = None


    def dodetailtrend(self, plt):
        if self.detailtrended:
            x = globe.SimTimeVector
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.massflow.simvector)
            axarr[0].set_title('Mass flow (kg/s) - ' + self.name)
            axarr[1].plot(x, self.deltapressure.simvector)
            axarr[1].set_title('Delta Pressure (Pa) - ' + self.name)
            axarr[2].plot(x, self.op.simvector)
            axarr[2].set_title('Valve opening (fraction) - ' + self.name)


    def mouseover(self, x, y): #public override bool mouseover(double x, double y)
        return (utilities.distance(x - self.location.x, y - self.location.y) <= globe.ValveLength)


    def updateinoutpointlocations(self):
        self.inpoint[0].x = self.location.x - globe.ValveLength / 2 - globe.InOutPointWidth
        self.inpoint[0].y = self.location.y
        self.outpoint[0].x = self.location.x + globe.ValveLength / 2 + globe.InOutPointWidth
        self.outpoint[0].y = self.location.y

        super(valve, self).updateinoutpointlocations()


    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        self.update(asim.simi, False)
        diag = valveproperties(self, asim, aroot)
        #valveproperties valveprop = new valveproperties(this, asim);
        #valveprop.Show();


    def draw(self, canvas):
        self.updateinoutpointlocations()
        #canvas.create_rectangle(self.location.x, self.location.y, self.location.x + 50, self.location.y + 20)

        #GraphicsPath plot1;
        #    en plotPen;
        #float width = 1;

        #plot1 = new GraphicsPath();
        #plotPen = new Pen(Color.Black, width);

        point0 = point.point(globe.OriginX + int(globe.GScale*(self.location.x - globe.ValveLength/2)), \
            globe.OriginY + int(globe.GScale*(self.location.y - globe.ValveWidth/2)))
        point1 = point.point(globe.OriginX + int(globe.GScale*(self.location.x + globe.ValveLength / 2)), 
                globe.OriginY + int(globe.GScale*(self.location.y + globe.ValveWidth/2)))
        point2 = point.point(globe.OriginX + int(globe.GScale*(self.location.x + globe.ValveLength / 2)), 
                    globe.OriginY + int(globe.GScale*(self.location.y - globe.ValveWidth/2)))
        point3 = point.point(globe.OriginX + int(globe.GScale*(self.location.x - globe.ValveLength / 2)),
                globe.OriginY + int(globe.GScale*(self.location.y + globe.ValveWidth/2)))
        
        polygon = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)
        #print(point0.x,point0.y)
        #print(point1.x,point1.y)
        
        #canvas.create_rectangle(point0.x, point0.y, point1.x, point1.y)
        #Point[] myArray = new Point[] 
        #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - global.ValveLength/2)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y - global.ValveWidth/2))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + global.ValveLength / 2)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + global.ValveWidth/2))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + global.ValveLength / 2)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y - global.ValveWidth/2))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - global.ValveLength / 2)),
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + global.ValveWidth/2)))};

        #plot1.AddPolygon(myArray);

        #plotPen.Color = Color.Black;

        #SolidBrush brush = new SolidBrush(Color.White);
        #print(self.highlighted)
        if (self.highlighted == True):
            canvas.itemconfig(polygon, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(polygon, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(polygon, fill='black')
        #G.FillPath(brush, plot1);
        #G.DrawPath(plotPen, plot1);

        super(valve, self).draw(canvas)




