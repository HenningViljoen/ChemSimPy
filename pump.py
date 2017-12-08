from unitop import unitop
import math
import numpy as np
import globe as globe
from controlvar import controlvar
import utilities as utilities
from point import point
from pumpproperties import pumpproperties


class pump(unitop):
    def __init__(self, anr, ax, ay, amaxdeltapressure, amindeltapressure, 
             amaxactualflow, anactualvolumeflow, aon):
                #public pump(int anr, double ax, double ay, double amaxdeltapressure, double amindeltapressure, 
                #double amaxactualflow, double anactualvolumeflow, double aon)
                #: base(anr, ax, ay, 1, 1)
        super(pump, self).__init__(anr, ax, ay, 1, 1)
        self.initpump(amaxdeltapressure, amindeltapressure, amaxactualflow, anactualvolumeflow, aon)


    def pumpcopyconstructor(self, baseclasscopyfrom):
        self.initpump(0, 0, 0, 0, 0)
        self.copyfrom(baseclasscopyfrom)


    def initpump(self, amaxdeltapressure, amindeltapressure, amaxactualflow, anactualvolumeflow, aon):
            #public void initpump(double amaxdeltapressure, double amindeltapressure,
            #double amaxactualflow, double anactualvolumeflow, double aon)
        self.objecttype = globe.objecttypes.Pump

        self.name = 'Pump ' + str(self.nr)

        self.controlpropthisclass = []
        self.controlpropthisclass +=  ["on","deltapressure", "maxactualvolumeflow","pumpspeed","pumppower"]
        self.nrcontrolpropinherited = len(self.controlproperties)
        self.controlproperties += self.controlpropthisclass

        self.on = controlvar(1, True)  #0 for off, 1 for on.
        self.deltapressure = controlvar() #Pa
        self.pumpspeed = controlvar(globe.PumpCurveSpeedT0) #rev per second
        self.pumpspeeddynamic = globe.PumpCurveSpeedT0 #will trail the main pumpspeed set point which is the controlvar above.
        self.dpumpspeeddt = 0.0
        self.speedtau = globe.PumpSpeedTau

        self.maxdeltapressure = amaxdeltapressure #Pa
        self.mindeltapressure = amindeltapressure #Pa

        self.pumpcurvem = 0.0
        self.pumpcurvec = 0.0

        self.pumpcurvea0 = 0.0
        self.pumpcurvea1 = 0.0
        self.pumpcurvea2 = 0.0
  
        #deltapressuresimvector = new double[global.SimVectorLength]
        self.maxactualvolumeflow = controlvar(amaxactualflow)    #actual m3/s
        self.actualvolumeflow.v = anactualvolumeflow  #actual m3/s
        #actualvolumeflow.simvector = new double[global.SimVectorLength]
        self.actualvolumeflow.v = 0
        self.on.v = aon #on or off
        self.calcmethod = globe.calculationmethod.DetermineFlow

        self.calcpumpcurve()

        self.pumppower = controlvar(0.0) #W
        self.newpumppower = 0.0; #W; The future steady state fan power.
        self.pumppowerstatespacex1 = 0.0
        self.pumppowerstatespacex2 = 0.0
        self.ddtpumppowerstatespacex1 = 0.0
        self.ddtpumppowerstatespacex2 = 0.0

        self.outletlocation = point(0, 0)
        self.updateinoutpointlocations()


    def copyfrom(self, baseclasscopyfrom):
        pumpcopyfrom = baseclasscopyfrom

        super(pump, self).copyfrom(pumpcopyfrom)

        self.on.v = pumpcopyfrom.on.v
        self.deltapressure.v = pumpcopyfrom.deltapressure.v #Pa
        self.pumpspeed.v = pumpcopyfrom.pumpspeed.v
        self.pumpspeeddynamic = pumpcopyfrom.pumpspeeddynamic
        self.dpumpspeeddt = pumpcopyfrom.dpumpspeeddt
        self.speedtau = pumpcopyfrom.speedtau
        self.on = pumpcopyfrom.on #on or off
        self.maxdeltapressure = pumpcopyfrom.maxdeltapressure #Pa
        self.mindeltapressure = pumpcopyfrom.mindeltapressure #Pa
        self.maxactualvolumeflow.v = pumpcopyfrom.maxactualvolumeflow.v     #
        self.pumpcurvem = pumpcopyfrom.pumpcurvem
        self.pumpcurvec = pumpcopyfrom.pumpcurvec
        self.pumpcurvea0 = pumpcopyfrom.pumpcurvea0
        self.pumpcurvea1 = pumpcopyfrom.pumpcurvea1
        self.pumpcurvea2 = pumpcopyfrom.pumpcurvea2

        self.pumppower.v = pumpcopyfrom.pumppower.v
        self.newpumppower = pumpcopyfrom.newpumppower #W; The future steady state fan power.
        self.pumppowerstatespacex1 = pumpcopyfrom.pumppowerstatespacex1
        self.pumppowerstatespacex2 = pumpcopyfrom.pumppowerstatespacex2
        self.ddtpumppowerstatespacex1 = pumpcopyfrom.ddtpumppowerstatespacex1
        self.ddtpumppowerstatespacex2 = pumpcopyfrom.ddtpumppowerstatespacex2

        self.outletlocation.copyfrom(pumpcopyfrom.outletlocation)
        self.calcmethod = pumpcopyfrom.calcmethod


    def selectedproperty(self, selection): #public override controlvar selectedproperty(int selection)
        if selection >= self.nrcontrolpropinherited:
            diff = selection - self.nrcontrolpropinherited
            if diff == 0:
                return self.on
            elif diff == 1:
                return self.deltapressure
            elif diff == 2:
                return self.maxactualvolumeflow
            elif diff == 3:
                return self.pumpspeed
            elif diff == 4:
                return self.pumppower
            else:
                return None
        else:
            return super(pump, self).selectedproperty(selection)


    def calcpumpcurve(self):
        self.pumpcurvem = -self.maxdeltapressure / self.maxactualvolumeflow.v
        self.pumpcurvec = self.maxdeltapressure

        self.maxactualvolumeflow.v = globe.PumpCurvef2
        p1 = globe.PumpCurvep1 #local double
        f1 = globe.PumpCurvef1 #local double
        f2 = globe.PumpCurvef2 #local double
        self.pumpcurvea0 = globe.PumpCurveYAxis / math.pow(self.pumpspeed.v, 2)
        self.pumpcurvea2 = (self.pumpspeed.v * f2 * p1 - f2 * self.pumpcurvea0 * math.pow(self.pumpspeed.v, 3) + \
            self.pumpcurvea0 * math.pow(self.pumpspeed.v, 3) * f1) / \
            (-math.pow(f2, 2) * self.pumpspeed.v * f1 + math.pow(f1, 2) * self.pumpspeed.v * f2)
        self.pumpcurvea1 = (-self.pumpcurvea0 * math.pow(self.pumpspeed.v, 2) - self.pumpcurvea2 * math.pow(f2, 2)) / \
            (self.pumpspeed.v * f2)


    def calcdeltapressurequadratic(self, actualflow):
        return self.pumpcurvea0 * math.pow(self.pumpspeeddynamic, 2) + \
                self.pumpcurvea1 * self.pumpspeeddynamic * actualflow + \
                self.pumpcurvea2 * math.pow(actualflow, 2)


    def calcpumppower(self, volumeflow, pressure):
        return volumeflow * pressure


    def calcactualvolumeflowquadratic(self):
        xfinal = 0.0
        if self.on.v >= 0.5:
            ison = 1
        else:
            ison = 0
        #double ison = (on.v >= 0.5) ? 1 : 0
        a = self.pumpcurvea2
        b = self.pumpcurvea1 * self.pumpspeeddynamic
        c = self.pumpcurvea0 * math.pow(self.pumpspeeddynamic, 2) - self.deltapressure.v
        sqrtarg = b * b - 4 * a * c
        if (sqrtarg >= 0):
            x1 = (-b + math.sqrt(sqrtarg)) / (2.0 * a)
            x2 = (-b - math.sqrt(sqrtarg)) / (2.0 * a)
            if x1 >= x2: xfinal = x1
            else: xfinal = x2
        else: xfinal = globe.PumpMinActualFlow
        self.actualvolumeflow.v = ison * xfinal


    def ddt(self):
        self.pumppowerstatespacex1 = self.pumppower.v
        self.ddtpumppowerstatespacex1 = self.pumppowerstatespacex2
        self.ddtpumppowerstatespacex2 = -globe.Rotatinga0 * self.pumppowerstatespacex1 - \
            globe.Rotatinga1 * self.pumppowerstatespacex2 + globe.Rotatingb0 * self.newpumppower

        self.dpumpspeeddt = -1 / globe.PumpSpeedTau * self.pumpspeeddynamic + 1 / globe.PumpSpeedTau * self.pumpspeed.v


    def update(self, simi, historise):
        if (self.inflow[0] != None and self.outflow[0] != None):
            self.deltapressure.v = self.outflow[0].mat.P.v - self.inflow[0].mat.P.v
                
            if (self.deltapressure.v > self.maxdeltapressure): self.deltapressure.v = self.maxdeltapressure
            elif (self.deltapressure.v < self.mindeltapressure): self.deltapressure.v = self.mindeltapressure

            if (self.inflow[0].hasmaterial):
                if (self.calcmethod == globe.calculationmethod.DetermineFlow):
                    self.calcactualvolumeflowquadratic()
                    #//actualvolumeflow.v = ison*(deltapressure.v - pumpcurvec) / pumpcurvem; #//whether this is actual or standard flow needs to be checked and updated.
                else:
                    self.deltapressure.v = self.calcdeltapressurequadratic(self.actualvolumeflow.v)
                    #//deltapressure.v = actualvolumeflow.v * pumpcurvem + pumpcurvec
                    self.outflow[0].mat.P.v = self.inflow[0].mat.P.v + self.deltapressure.v
            else:
                self.actualvolumeflow.v = 0

            self.newpumppower = self.calcpumppower(self.actualvolumeflow.v, self.deltapressure.v)

            self.ddt()
            self.pumppowerstatespacex1 += self.ddtpumppowerstatespacex1 * globe.SampleT
            self.pumppowerstatespacex2 += self.ddtpumppowerstatespacex2 * globe.SampleT
            self.pumpspeeddynamic += self.dpumpspeeddt * globe.SampleT

            self.pumppower.v = self.pumppowerstatespacex1
            if (self.pumppower.v < 0): self.pumppower.v = 0

            self.inflow[0].massflow.v = self.actualvolumeflow.v * self.inflow[0].mat.density.v
            self.outflow[0].massflow.v = self.actualvolumeflow.v * self.inflow[0].mat.density.v
            self.outflow[0].mat.copycompositiontothismat(self.inflow[0].mat)
            self.outflow[0].mat.T.v = self.inflow[0].mat.T.v

            if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
                index = int(simi / globe.SimVectorUpdatePeriod)
                if (self.deltapressure.simvector != None):
                    self.deltapressure.simvector[index] = self.deltapressure.v
                if (self.actualvolumeflow.simvector != None):
                    self.actualvolumeflow.simvector[index] = self.actualvolumeflow.v
                if (self.pumpspeed.simvector != None):
                    self.pumpspeed.simvector[index] = self.pumpspeed.v
                if (self.pumppower.simvector != None):
                    self.pumppower.simvector[index] = self.pumppower.v
                if (self.on.simvector != None):
                    self.on.simvector[index] = self.on.v


    def mouseover(self, x, y):
        return (utilities.distance(x - self.location.x, y - self.location.y) <= globe.PumpInitRadius)


    def updateinoutpointlocations(self):
        self.outletlocation.setxy(self.location.x - globe.PumpInitOutletLength / 2, self.location.y - globe.PumpInitRadius)

        #//Update in and out point locations;
        self.inpoint[0].x = self.location.x + globe.PumpInitRadius + globe.InOutPointWidth
        self.inpoint[0].y = self.location.y
        self.outpoint[0].x = self.location.x - globe.PumpInitOutletLength - globe.InOutPointWidth
        self.outpoint[0].y = self.outletlocation.y

        super(pump, self).updateinoutpointlocations()


    def setproperties(self, asim, aroot):   #public override void setproperties(simulation asim)
        diag = pumpproperties(self, asim, aroot)


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
        if (self.actualvolumeflow.simvector == None):
            self.actualvolumeflow.simvector = [0.0]*globe.SimVectorLength
        if (self.pumpspeed.simvector == None):
            self.pumpspeed.simvector = [0.0]*globe.SimVectorLength
        if (self.pumppower.simvector == None):
            self.pumppower.simvector = [0.0]*globe.SimVectorLength


    def deallocatememory(self):
        self.deltapressure.simvector = None
        self.actualvolumeflow.simvector = None
        self.pumpspeed.simvector = None
        self.pumppower.simvector = None


    def dodetailtrend(self, plt):
        if self.detailtrended:
            x = globe.SimTimeVector
            f, axarr = plt.subplots(2, sharex=True)
            axarr[0].plot(x, self.pumppower.simvector)
            axarr[0].set_title('Pump power (W) : ' + self.name)
            axarr[1].plot(x, self.pumpspeed.simvector)
            axarr[1].set_title('Pump speed (RPS) : ' + self.name)


    def draw(self, canvas):
        self.updateinoutpointlocations()

        #GraphicsPath plot1
        #Pen plotPen
        #float width = 1

        #plot1 = new GraphicsPath()
        #plotPen = new Pen(Color.Black, width)

        point0 = point(globe.OriginX + int(globe.GScale*(self.outletlocation.x - globe.PumpInitOutletLength / 2)), 
                    globe.OriginY + int(globe.GScale*(self.outletlocation.y + globe.PumpInitOutletRadius)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.outletlocation.x - globe.PumpInitOutletLength / 2)), 
                    globe.OriginY + int(globe.GScale*(self.outletlocation.y - globe.PumpInitOutletRadius)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.outletlocation.x + globe.PumpInitOutletLength / 2)), 
                    globe.OriginY + int(globe.GScale*(self.outletlocation.y - globe.PumpInitOutletRadius)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.outletlocation.x + globe.PumpInitOutletLength / 2)),
                    globe.OriginY + int(globe.GScale*(self.outletlocation.y + globe.PumpInitOutletRadius)))
        
        polygon = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)

        #Point[] myArray = new Point[] 
        #    {new Point(global.OriginX + Convert.ToInt32(global.GScale*(outletlocation.x - global.PumpInitOutletLength / 2)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(outletlocation.y + global.PumpInitOutletRadius))), 
        #    new Point(global.OriginX + Convert.ToInt32(global.GScale*(outletlocation.x - global.PumpInitOutletLength / 2)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(outletlocation.y - global.PumpInitOutletRadius))), 
         #   new Point(global.OriginX + Convert.ToInt32(global.GScale*(outletlocation.x + global.PumpInitOutletLength / 2)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(outletlocation.y - global.PumpInitOutletRadius))), 
        #    new Point(global.OriginX + Convert.ToInt32(global.GScale*(outletlocation.x + global.PumpInitOutletLength / 2)),
        #            global.OriginY + Convert.ToInt32(global.GScale*(outletlocation.y + global.PumpInitOutletRadius)))}

        #plot1.AddPolygon(myArray)

        x0 = globe.OriginX + int(globe.GScale * (self.location.x - globe.PumpInitRadius))
        y0 = globe.OriginY + int(globe.GScale * (self.location.y - globe.PumpInitRadius))
        x1 = x0 + int(globe.GScale * (globe.PumpInitRadius * 2))
        y1 = y0 + int(globe.GScale * (globe.PumpInitRadius * 2))

        circle = canvas.create_oval(x0, y0, x1, y1)

        if self.highlighted:
            canvas.itemconfig(circle, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(circle, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(circle, fill='gray')

        #plot1.AddEllipse(global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.PumpInitRadius)),
        #                    global.OriginY + Convert.ToInt32(global.GScale * (location.y - global.PumpInitRadius)),
         #                   Convert.ToInt32(global.GScale * (global.PumpInitRadius * 2)),
         #                   Convert.ToInt32(global.GScale * (global.PumpInitRadius * 2)))

        #plotPen.Color = Color.Black

        #SolidBrush brush = new SolidBrush(Color.White)
        #if (highlighted) { brush.Color = Color.Orange }
        #G.FillPath(brush, plot1)
        #G.DrawPath(plotPen, plot1)

        super(pump, self).draw(canvas)


