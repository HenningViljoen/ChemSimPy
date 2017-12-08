from unitop import unitop
import globe as globe
from controlvar import controlvar
import sys
import math
from point import point
from heatexchangersimpleproperties import heatexchangersimpleproperties

class heatexchangersimple(unitop):
    
        
    #//This simple heatexchanger will not be modelled with hundreds of small diameter pipes going through the exchanger.  Total flow in will be referenced
    #//only, and total flow out.  No sections will be modelled in the exchanger.  Only flow, temperature, and pressure in, and flow and T and P out.

    #//For the first application, namely the cooling water circuit, flow through the exchangers will be calculated based on the delta pressure over it.
        
    #//The heat exchanger will be modelled as 2 streams flowing and exchanging heat.  Will be accronymed with str1 and str2.  Strm1 will be shell side, Strm2 tube side.
    #//For the sake of equation signs of terms, it is assumed that str1 is the warmer stream.  But this does not need to be the case, in the case of 
    #//str2 being the warmer stream, the math should still work with heat terms just being negative.
    #//For the analogy with the steam generator unitop, str1 is the gas stream, and str2 is the water/steam stream.

    

        
    def __init__(self, anr, ax, ay):
                #public heatexchangersimple(int anr, double ax, double ay)
                #: base(anr, ax, ay, global.HeatExchangerNIn, global.HeatExchangerNOut)
        super(heatexchangersimple, self).__init__(anr, ax, ay, globe.HeatExchangerNIn, globe.HeatExchangerNOut)
        self.initheatexchangersimple()


    def heatexchangersimplecopyconstructor(self, baseclasscopyfrom):
                #public heatexchangersimple(baseclass baseclasscopyfrom) :
                #base(0, 0, 0, global.HeatExchangerNIn, global.HeatExchangerNOut)
        self.initheatexchangersimple()
        self.copyfrom(baseclasscopyfrom)
        

    def initheatexchangersimple(self):
        self.objecttype = globe.objecttypes.HeatExchangerSimple

        self.U = controlvar(globe.HeatExchangerSimpleDefaultU) #// W/(m^2*K) ; Overall heat exchanger coefficient for heat exchanger.  Not sure if this is going to be used now.
        #self.U.simvector = [0.0]*globe.SimVectorLength  #I do not think we have to allocate mem to these at this point.
        self.A = controlvar(globe.HeatExchangerSimpleDefaultA) #// m^2 ; The contact area for the fluids with each other in the heat exchanger.  Not sure if this is going to be used now.  
        #self.A.simvector = [0.0]*globe.SimVectorLength
        self.K = 0.0 #//constants used in calculating the new output temperatures of teh HX.

        self.name = 'HX ' + str(self.nr)

        self.controlpropthisclass = []
        self.controlpropthisclass += ["U", "A", "strm1temptau", "strm2temptau", "strm2flowcoefficient"]
        self.nrcontrolpropinherited = len(self.controlproperties)
        self.controlproperties += self.controlpropthisclass

        self.strm1flowcoefficient = globe.HESStrm1FlowCoefficient
        self.strm1temptau = controlvar(globe.HESStrm1TempTau)
        #self.strm1temptau.simvector = new double[globe.SimVectorLength]
        self.strm1flowtau = globe.HESStrm1FlowTau

        self.strm2flowcoefficient = controlvar(globe.HESStrm2FlowCoefficient)
        self.strm2temptau = controlvar(globe.HESStrm2TempTau)
        #self.strm2temptau.simvector = new double[globe.SimVectorLength]
        self.strm2flowtau = globe.HESStrm2FlowTau

        self.strm1massflownew = globe.HESMassFlowStrm1T0 #//kg/s
        self.dstrm1massflowdt = 0.0 #//kg/s/s
        self.strm1pressureinnew = globe.HEPStrm1Inlet #//Pa
        self.dstrm1pressureindt = 0.0 #//Pa/s
        self.strm1temperatureoutnew = globe.HETStrm1Outlet #//Kelvin
        self.dstrm1temperatureoutnewdt = 0.0  #Kelvin/s

        self.strm2massflownew = globe.HESMassFlowStrm2T0 #//kg/s
        self.dstrm2massflowdt = 0.0 #//kg/s/s
        self.strm2pressureinnew = globe.HEPStrm2Inlet #//Pa
        self.dstrm2pressureindt = 0.0 #//Pa/s
        self.strm2temperatureoutnew = globe.HETStrm2Outlet #//Kelvin
        self.dstrm2temperatureoutnewdt = 0.0  #Kelvin/s


    def copyfrom(self, baseclasscopyfrom):
        #public override void copyfrom(baseclass baseclasscopyfrom)
        heatexchangersimplecopyfrom = baseclasscopyfrom
        #heatexchangersimple heatexchangersimplecopyfrom = (heatexchangersimple)baseclasscopyfrom

        super(heatexchangersimple,self).copyfrom(heatexchangersimplecopyfrom)

        self.U.v = heatexchangersimplecopyfrom.U.v
        self.A.v = heatexchangersimplecopyfrom.A.v 
        self.K = heatexchangersimplecopyfrom.K

        self.strm1flowcoefficient = heatexchangersimplecopyfrom.strm1flowcoefficient
        self.strm1temptau.v = heatexchangersimplecopyfrom.strm1temptau.v
        self.strm1flowtau = heatexchangersimplecopyfrom.strm1flowtau
        self.strm2flowcoefficient = heatexchangersimplecopyfrom.strm2flowcoefficient
        self.strm2temptau.v = heatexchangersimplecopyfrom.strm2temptau.v
        self.strm2flowtau = heatexchangersimplecopyfrom.strm2flowtau

        self.strm1massflownew = heatexchangersimplecopyfrom.strm1massflownew #//kg/s
        self.dstrm1massflowdt = heatexchangersimplecopyfrom.dstrm1massflowdt #//kg/s/s
        self.strm1pressureinnew = heatexchangersimplecopyfrom.strm1pressureinnew #//Pa
        self.dstrm1pressureindt = heatexchangersimplecopyfrom.dstrm1pressureindt #//Pa/s
        self.strm1temperatureoutnew = heatexchangersimplecopyfrom.strm1temperatureoutnew #//Kelvin
        self.dstrm1temperatureoutnewdt = heatexchangersimplecopyfrom.dstrm1temperatureoutnewdt #//Kelvin

        #//Stream 2 flow
        self.strm2massflownew = heatexchangersimplecopyfrom.strm2massflownew #//kg/s
        self.dstrm2massflowdt = heatexchangersimplecopyfrom.dstrm2massflowdt #//kg/s
        self.strm2pressureinnew = heatexchangersimplecopyfrom.strm2pressureinnew #//Pa
        self.dstrm2pressureindt = heatexchangersimplecopyfrom.dstrm2pressureindt #//Pa/s
        self.strm2temperatureoutnew = heatexchangersimplecopyfrom.strm2temperatureoutnew #//Kelvin
        self.dstrm2temperatureoutnewdt = heatexchangersimplecopyfrom.dstrm2temperatureoutnewdt #//Kelvin


    def selectedproperty(self, selection):  #public override controlvar selectedproperty(int selection)
        if (selection >= self.nrcontrolpropinherited):
            diff = selection - self.nrcontrolpropinherited
            if diff == 0:
                return self.U
            elif diff == 1:
                return self.A
            elif diff == 2:
                return self.strm1temptau
            elif diff == 3:
                return self.strm2temptau
            elif diff == 4:
                return self.strm2flowcoefficient
            else:
                return None
        else:
            return super(heatexchangersimple, self).selectedproperty(selection)


    #//private void calcCpm(int i) //I think this method will not be needed anymore.
    #//{
    #//    Cpm[i] = 128.1 * Math.Log(Tmave[i]) - 264.11;  //Equation is from Excel sheet.
    #//}

    def ddt(self, simi):  #public void ddt(int simi)  #//Differential equations
        self.dstrm1pressureindt = \
            -1 / self.strm1flowtau * self.inflow[0].mat.P.v + 1 / self.strm1flowtau * self.strm1pressureinnew
        self.dstrm2pressureindt = \
            -1 / self.strm2flowtau * self.inflow[1].mat.P.v + 1 / self.strm2flowtau * self.strm2pressureinnew
        self.dstrm1temperatureoutnewdt = \
            -1 / self.strm1temptau.v * self.outflow[0].mat.T.v + 1 / self.strm1temptau.v * self.strm1temperatureoutnew
        self.dstrm2temperatureoutnewdt = \
            -1 / self.strm2temptau.v * self.outflow[1].mat.T.v + 1 / self.strm2temptau.v * self.strm2temperatureoutnew


    def update(self, simi, historise):  #public override void update(int simi, bool historise)
        #//strm1massflownew = global.HESStrm1FlowCoefficient * Math.Sqrt((inflow[0].mat.P.v - outflow[0].mat.P.v + global.Epsilon) * inflow[0].mat.density.v);
        #//strm2massflownew = global.HESStrm2FlowCoefficient * Math.Sqrt((inflow[1].mat.P.v - outflow[1].mat.P.v + global.Epsilon) * inflow[1].mat.density.v);

        self.strm1pressureinnew = self.outflow[0].mat.P.v + \
            math.pow(self.inflow[0].massflow.v / self.strm1flowcoefficient, 2) * \
            (self.inflow[0].mat.density.v + globe.Epsilon)
        self.strm2pressureinnew = self.outflow[1].mat.P.v + \
            math.pow(self.inflow[1].massflow.v / self.strm2flowcoefficient.v, 2) * \
            (self.inflow[1].mat.density.v + globe.Epsilon)

        #6 local vars here below:
        f1 = self.inflow[0].massflow.v
        f2 = self.inflow[1].massflow.v
        C1 = self.inflow[0].mat.totalCp / self.inflow[0].mat.massofonemole
        C2 = self.inflow[1].mat.totalCp / self.inflow[1].mat.massofonemole
        T1in = self.inflow[0].mat.T.v
        T2in = self.inflow[1].mat.T.v

        #//After the flow variables have been solved we can solve the temperature variables static solutions.
        Knew = self.U.v * self.A.v * (1 / (f1*C1 + globe.Epsilon) - 
            1/(f2*C2 + globe.Epsilon)) #local var

        if not math.isnan(Knew): self.K = Knew

        self.outflow[0].mat.copycompositiontothismat(self.inflow[0].mat)
        self.outflow[1].mat.copycompositiontothismat(self.inflow[1].mat)

        strm1temperatureoutnewden = (f2 * C2 * math.exp(self.K) - f1 * C1 + globe.Epsilon) #local var
        if (math.isinf(strm1temperatureoutnewden)):
            strm1temperatureoutnewden = sys.float_info.max
        elif (strm1temperatureoutnewden != 0):
            self.strm1temperatureoutnew = \
                (f2 * C2 * (T1in + math.exp(self.K) * T2in - T2in) - f1 * C1 * T1in) / strm1temperatureoutnewden
            T1out = self.strm1temperatureoutnew #local var
            strm2temperatureoutnew = (f1*C1*(T1in - T1out) + f2*C2*T2in)/(f2*C2 + globe.Epsilon)

        self.ddt(simi)

        #//inflow[0].massflow.v += dstrm1massflowdt * global.SampleT;
        #//inflow[0].update(simi);
        self.inflow[0].mat.P.v += self.dstrm1pressureindt * globe.SampleT
        self.outflow[0].massflow.v = self.inflow[0].massflow.v
        self.outflow[0].mat.density.v = self.inflow[0].mat.density.v

        #//inflow[1].massflow.v += dstrm2massflowdt * global.SampleT;
        #//inflow[1].update(simi);
        self.inflow[1].mat.P.v += self.dstrm2pressureindt * globe.SampleT
        self.outflow[1].massflow.v = self.inflow[1].massflow.v
        self.outflow[1].mat.density.v = self.inflow[1].mat.density.v

        self.outflow[0].mat.T.v += self.dstrm1temperatureoutnewdt * globe.SampleT
        self.outflow[1].mat.T.v += self.dstrm2temperatureoutnewdt * globe.SampleT

        #//outflow[0].update(simi);  I do not think we need to update these here, since they will be updated in the simulation class sim method.
        #//outflow[1].update(simi);

        if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
            index = int(simi / globe.SimVectorUpdatePeriod)
            if (self.U.simvector != None):
                self.U.simvector[index] = self.U.v 
            if (self.A.simvector != None):
                self.A.simvector[index] = self.A.v
            if (self.strm1temptau.simvector != None):
                self.strm1temptau.simvector[index] = self.strm1temptau.v
            if (self.strm2temptau.simvector != None):
                self.strm2temptau.simvector[index] = self.strm2temptau.v
            if (self.strm2flowcoefficient.simvector != None):
                self.strm2flowcoefficient.simvector[index] = self.strm2flowcoefficient.v                 


    #//private void calcdynviscosity(int i) //Dynamic Viscosity in watersegment[i]
    #//{
    #//    strm2dynviscosity[i] = globe.DynViscA * Math.Exp(globe.DynViscB * strm2segments[i].T.v);
    #//}

    def showtrenddetail(self):
        if not self.detailtrended:
            self.detailtrended = True
            self.allocatememory()
        else:
            self.detailtrended = False
            self.deallocatememory()

    
    def allocatememory(self):
        if (self.U.simvector == None):
            self.U.simvector = [0.0]*globe.SimVectorLength
        if (self.A.simvector == None):
            self.A.simvector = [0.0]*globe.SimVectorLength
        if (self.strm1temptau.simvector == None):
            self.strm1temptau.simvector = [0.0]*globe.SimVectorLength
        if (self.strm2temptau.simvector == None):
            self.strm2temptau.simvector = [0.0]*globe.SimVectorLength
        if (self.strm2flowcoefficient.simvector == None):
            self.strm2flowcoefficient.simvector = [0.0]*globe.SimVectorLength


    def deallocatememory(self):
        self.U.simvector = None
        self.A.simvector = None
        self.strm1temptau.simvector = None
        self.strm2temptau.simvector = None
        self.strm2flowcoefficient.simvector = None


    def dodetailtrend(self, plt):
        if self.detailtrended:
            x = globe.SimTimeVector
            f, axarr = plt.subplots(5, sharex=True)
            axarr[0].plot(x, self.U.simvector)
            axarr[0].set_title('HX U - ' + self.name)
            axarr[1].plot(x, self.A.simvector)
            axarr[1].set_title('HX A - ' + self.name)
            axarr[2].plot(x, self.strm1temptau.simvector)
            axarr[2].set_title('strm1temptau - ' + self.name)
            axarr[3].plot(x, self.strm2temptau.simvector)
            axarr[3].set_title('strm2temptau - ' + self.name)
            axarr[4].plot(x, self.strm2flowcoefficient.simvector)
            axarr[4].set_title('strm2flowcoefficient - ' + self.name)


    #//public override void updatetrenddetail(simulation asim)
    #//{
    #//    if (detailtrends != null && detailtrends.Visible) { detailtrends.Invalidate(); }
    #//}


    def mouseover(self, x, y):   #public override bool mouseover(double x, double y)
        return (x >= (self.location.x - globe.HeatExchangerWidth / 2) and \
            x <= (self.location.x + globe.HeatExchangerWidth / 2) and \
            y >= (self.location.y - globe.HeatExchangerRadius) and y <= (self.location.y + globe.HeatExchangerRadius))


    def updateinoutpointlocations(self):
        #//Update in and out point locations;
        self.inpoint[0].x = self.location.x - 0.5*globe.HeatExchangerWidth + globe.HeatExchangerInPointsFraction[0] * \
            globe.HeatExchangerWidth
        self.inpoint[0].y = self.location.y - globe.HeatExchangerRadius - globe.InOutPointWidth
        self.inpoint[1].x = self.location.x - 0.5 * globe.HeatExchangerWidth + globe.HeatExchangerInPointsFraction[1] * \
            globe.HeatExchangerWidth
        self.inpoint[1].y = self.location.y + globe.HeatExchangerRadius + globe.InOutPointWidth
        self.outpoint[0].x = self.location.x - 0.5 * globe.HeatExchangerWidth + globe.HeatExchangerInPointsFraction[0] * \
            globe.HeatExchangerWidth
        self.outpoint[0].y = self.location.y + globe.HeatExchangerRadius + globe.InOutPointWidth
        self.outpoint[1].x = self.location.x - 0.5 * globe.HeatExchangerWidth + globe.HeatExchangerInPointsFraction[1] * \
            globe.HeatExchangerWidth
        self.outpoint[1].y = self.location.y - globe.HeatExchangerRadius - globe.InOutPointWidth
        super(heatexchangersimple, self).updateinoutpointlocations()


    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        diag = heatexchangersimpleproperties(self, asim, aroot)


    #public override void setproperties(simulation asim)
    #{
    #    heatexchangersimpleproperties heatexchangersimpleprop = new heatexchangersimpleproperties(this, asim);
    #    heatexchangersimpleprop.Show();
    #}

    def draw(self, canvas): #//public override void draw(Graphics G)
        self.updateinoutpointlocations()
        #G = canvas
        #//Draw main tank
        #GraphicsPath tankmain
        #Pen plotPen
        #float width = 1

        #tankmain = new GraphicsPath()
        #plotPen = new Pen(Color.Black, width)

        #Point[] myArray = new Point[] 
        point0 = point(globe.OriginX + int(globe.GScale*(self.location.x - 0.5*globe.HeatExchangerWidth)), 
                globe.OriginY + int(globe.GScale*(self.location.y + globe.HeatExchangerRadius)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.location.x - 0.5*globe.HeatExchangerWidth)), 
                globe.OriginY + int(globe.GScale*(self.location.y - globe.HeatExchangerRadius)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.location.x + 0.5*globe.HeatExchangerWidth)), 
                globe.OriginY + int(globe.GScale*(self.location.y - globe.HeatExchangerRadius)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.location.x + 0.5*globe.HeatExchangerWidth)),
                globe.OriginY + int(globe.GScale*(self.location.y + globe.HeatExchangerRadius)))
        
        polygon = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)
        if (self.highlighted == True):
            canvas.itemconfig(polygon, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(polygon, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(polygon, fill='grey')
        #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - 0.5*global.HeatExchangerWidth)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + global.HeatExchangerRadius))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - 0.5*global.HeatExchangerWidth)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y - global.HeatExchangerRadius))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + 0.5*global.HeatExchangerWidth)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y - global.HeatExchangerRadius))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + 0.5*global.HeatExchangerWidth)),
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + global.HeatExchangerRadius)))}
        #tankmain.AddPolygon(myArray)
        #plotPen.Color = Color.Black
        #SolidBrush brush = new SolidBrush(Color.White)
        #brush.Color = (highlighted) ? Color.Orange : Color.White
        #G.FillPath(brush, tankmain)
        #G.DrawPath(plotPen, tankmain)

        #//The writing of the name of the unitop in the unitop.
        #GraphicsPath unitopname = new GraphicsPath()
        #StringFormat format = StringFormat.GenericDefault
        #FontFamily family = new FontFamily("Arial")
        #int myfontStyle = (int)FontStyle.Bold
        #int emSize = 10
        #PointF namepoint = new PointF(global.OriginX + Convert.ToInt32(global.GScale*(location.x) - name.Length*emSize/2/2),
        #    global.OriginY + Convert.ToInt32(global.GScale*(location.y)))
        #unitopname.AddString(name, family, myfontStyle, emSize, namepoint, format)
        #G.FillPath(Brushes.Black, unitopname)
        emSize = 10 #local int
        hxnamepoint = point(globe.OriginX + int(globe.GScale*(self.location.x) - len(self.name)*emSize/2/2), \
            globe.OriginY + int(globe.GScale*(self.location.y)))
        nametext = canvas.create_text(hxnamepoint.x, hxnamepoint.y)
        canvas.itemconfig(nametext, text=self.name, fill='black')

        #//Draw inpoint
        super(heatexchangersimple, self).draw(canvas)
