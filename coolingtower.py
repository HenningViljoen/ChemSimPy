import globe as globe
from unitop import unitop
import numpy as np
import utilities as utilities
from controlvar import controlvar
from material import material
import math
from point import point
from coolingtowerproperties import coolingtowerproperties


class coolingtower(unitop):
    def __init__(self, anr, ax, ay):
                #public coolingtower(int anr, double ax, double ay)
                #: base(anr, ax, ay, global.CTHESNIn, global.CTHESNOut)
        super(coolingtower, self).__init__(anr, ax, ay, globe.CTHESNIn, globe.CTHESNOut)
        self.initcoolingtower()
        self.update(0, True)


    def coolingtowerconstructor(self, baseclasscopyfrom):
        self.initcoolingtower()
        self.copyfrom(baseclasscopyfrom)


    def initcoolingtower(self):
        #public double U; // W/(m^2*K) ; Overall heat exchanger coefficient for heat exchanger.  Not sure if this is going to be used now.
        #public double A; // m^2 ; The contact area for the fluids with each other in the heat exchanger.  Not sure if this is going to be used now.  
        #//public double K; //constants used in calculating the new output temperatures of the HX.

        self.objecttype = globe.objecttypes.CoolingTower
        self.name = 'Cooling tower ' + str(self.nr)

        self.controlpropthisclass = []
        self.controlpropthisclass += ["on", "fanspeed", "fanpower", "ctwatervolumefraction", "masstransfercoefair", \
                "heattransfercoefwater", "heattransfercoefair"]

        self.nrcontrolpropinherited = len(self.controlproperties)
        self.controlproperties += self.controlpropthisclass

        self.nrstages = globe.CTDefaultNrStages
        self.h = globe.SampleT #step size for integration

        self.on = controlvar(1, True) #0 for off, 1 for on.
        self.linkedsprayvalve = None #This is not used at the moment. Every coolingtower will now have feeding spray valve that is linked to it.
        self.fanspeed = controlvar(globe.CTFanSpeedT0)  #revolusions per second.

        self.fanpower = controlvar(0.0) #W
        self.newfanpower = 0.0; #//W; The future steady state fan power.
        self.fanpowerstatespacex1 = 0.0
        self.fanpowerstatespacex2 = 0.0
        self.ddtfanpowerstatespacex1 = 0.0
        self.ddtfanpowerstatespacex2 = 0.0

        self.deltapressure = globe.CTDefaultFanDP #Pa.  The pressure drop over the fan.

        self.watervolumefraction = controlvar(globe.CTWaterVolumeFraction) #//fraction of total volume in tower occupied by water.  This is from Marques article -> 0.01.
        self.CTAirVolumeFraction = 1.0 - self.watervolumefraction.v - globe.CTPackingVolumeFraction
        self.CTTotalWaterVolume = globe.CTTotalVolume * self.watervolumefraction.v
        self.CTNrDroplets = self.CTTotalWaterVolume / globe.CTDropletVolume
        self.CTDefaultSegmentContactArea = self.CTNrDroplets * globe.CTDropletSurfaceArea / self.nrstages #//m^2  interfacial contact area total per segment.
        self.a = self.CTNrDroplets * globe.CTDropletSurfaceArea / (globe.CTTotalVolume)
               #//m^2/m^3  interfacial contact area of water droplets per unit volume of the tower.

        self.tuningfactor = globe.CTTuningFactor #dimensionless.  This factor will be used to tune the simultion 
                                                    #in terms chilling in the cooling tower.

        self.outflow0temperatureoutnew = 0.0 #Kelvin
        self.doutflow0temperatureoutnewdt = 0.0 #Kelvin/sec
            #//U = global.HeatExchangerSimpleDefaultU;
            #//A = global.HeatExchangerSimpleDefaultA;
            #//K = 0;

        self.masstransfercoefair = controlvar(globe.CTDefaultMassTransferCoefficientAir) #kg/(s*m^2) 
        self.masstransfercoefair.simvector = [0.0]*globe.SimVectorLength
        self.heattransfercoefwater = controlvar(globe.CTDefaultHeatTransferCoefficientWater) #W/(m^2*K)
        self.heattransfercoefwater.simvector = [0.0]*globe.SimVectorLength
        self.heattransfercoefair = controlvar(globe.CTDefaultHeatTransferCoefficientAir) #W/(m^2*K)
        self.heattransfercoefair.simvector = [0.0]*globe.SimVectorLength

        self.wetbulbtemperature = 0.0    #Kelvin
        self.calcwetbulbtemp() #//Kelvin

        self.massfluxwater = 0.0 #//m3/s : Mass flux flow of water in the CT.
        self.massfluxair = 0.0 #//m3/s : Mass flux flow of air in the CT.

        self.segmentvolume = list() #m^3 total volume per water segment : includes packing, water,
                                                # and air in each segment.
        for i in range(self.nrstages):
            self.segmentvolume.append(globe.CTWidth * globe.CTLength * globe.CTHeight / self.nrstages)

        self.segmentvolumewater = list() #m^3 volume per water segment
        for i in range(self.nrstages):
            self.segmentvolumewater.append(globe.CTWidth*globe.CTLength*globe.CTHeight*self.watervolumefraction.v \
                    / self.nrstages)       #//times 0.5 since half the volume is for water, and half for air.

        self.segmentvolumeair = list() #m^3 volume per air segment
        for i in range(self.nrstages):
            self.segmentvolumeair.append(globe.CTWidth * globe.CTLength * globe.CTHeight * \
                    self.CTAirVolumeFraction/self.nrstages) #//times 0.5 since half the volume is for air, 
                    #// and half for air.

        self.watersegment = list()
        for i in range(self.nrstages):
            watermaterial = material()
            watermaterial.materialconstructor2(globe.fluidpackage, globe.CTTStrm0Inlet, globe.baseprocessclassInitVolume, \
                    globe.CTPStrm0Inlet, 0)
            self.watersegment.append(watermaterial) #//should maybe again be initialised with water only.

        self.airsegment = list()
        for i in range(self.nrstages):
            airmaterial = material()
            airmaterial.materialconstructor2(globe.fluidpackage, globe.CTTStrm1Inlet, self.segmentvolumeair[i], \
                    globe.CTPStrm1Inlet, 1)
            self.airsegment.append(airmaterial) #//Should maybe again be initialised with Air only.
            for j in range(len(self.airsegment[i].composition)):
                if self.airsegment[i].composition[j].m.name == "Air":   #if j == int(globe.components.Air):
                    self.airsegment[i].composition[j].molefraction = 1.0
                else:
                    self.airsegment[i].composition[j].molefraction = 0.0
            self.airsegment[i].PTfVflash(self.airsegment[i].T.v, self.airsegment[i].V.v, self.airsegment[i].P.v, \
                self.airsegment[i].f.v)

        self.watersegmentflowout = list() #//kg/s. The mass flow out of the particular water segment.
        for i in range(self.nrstages):
            self.watersegmentflowout.append(0.0)

        self.airsegmentdryairflowout = list() #//The mass flow out of the particular air segment.
        for i in range(self.nrstages):
            self.airsegmentdryairflowout.append(0.0)

        self.interfacetemperature = list() #Kelvin.  Temperature at the interface for the segment.
        self.interfacetemperaturesimvector = list()
        for i in range(self.nrstages):
            self.interfacetemperature.append(globe.CTTInterfaceT0)
            self.interfacetemperaturesimvector.append([0.0]*globe.SimVectorLength)

        self.interfaceabshumidity = list() #kg mass water / kg dry air
        self.interfaceabshumiditysimvector = list()
        for i in range(self.nrstages):
            self.interfaceabshumidity.append(\
                self.calcabshumidity(self.calcwatervapourpressuresaturation(self.interfacetemperature[i])))
            self.interfaceabshumiditysimvector.append([0.0]*globe.SimVectorLength)

        self.airabshumidity = list() #kg mass water / kg dry air
        self.airabshumiditysimvector = list()
        for i in range(self.nrstages):
            self.airabshumidity.append(self.calcabshumidity(self.calcwatervapourpressure(self.airsegment[i].T.v)))
            self.airabshumiditysimvector.append([0.0]*globe.SimVectorLength)

        self.massevap = list() #kg/s.  Mass evaporated per second, per segment.
        for i in range(self.nrstages): self.massevap.append(0.0)

        self.segmenttransferarea = list() #m2.  The surface area used to calculate the vapour mass transfer flow.
        for i in range(self.nrstages): self.segmenttransferarea.append(globe.CTTotalInterfaceArea)

        self.segmentcontactarea = list()  #m^2  interfacial contact area of water droplets for each segment of the tower.
        for i in range(self.nrstages): self.segmentcontactarea.append(self.CTDefaultSegmentContactArea)
            
        self.dTwaterdt = list() #K/s Let the first column be the normal derivative, and then column 1 
                                            #and on will be the different k values in RK4.
        for i in range(self.nrstages): self.dTwaterdt.append([0.0]*globe.CTRK4ArraySize)

        self.dTairdt = list() #//K/s
        for i in range(self.nrstages): self.dTairdt.append([0.0]*globe.CTRK4ArraySize)

        self.dhumidityairdt = list()
        for i in range(self.nrstages): self.dhumidityairdt.append([0.0]*globe.CTRK4ArraySize)

        #Properties for stream 0
        self.strm0valveop = globe.CTStrm0ValveOpeningDefault #Fraction.  Spray nozzle modelled as a valve.
        self.strm0cv = globe.CTStrm0Cv #The upstream pressure will be calculated by modelling the spray nozzle as a valve.
        self.strm0temptau = globe.CTStrm0TempTau
        self.strm0flowtau = globe.CTStrm0FlowTau

        #Properties for stream 1
        self.strm1flowcoefficient = globe.CTStrm1FlowCoefficient
        self.strm1temptau = globe.CTStrm1TempTau
        self.strm1flowtau = globe.CTStrm1FlowTau

        #//Variables for stream 0 equations .  In the case of the cooling tower, this will be the hot water stream.
        self.strm0massflownew = globe.CTMassFlowStrm0T0 #//kg/s
        self.dstrm0massflowdt = 0.0 #kg/s/s
        self.strm0pressureinnew = globe.CTPStrm0Inlet #//Pa
        self.dstrm0pressureindt = 0.0 #//Pa/s
        self.strm0temperatureoutnew = globe.CTTStrm0Outlet #//Kelvin
        self.dstrm0temperatureoutnewdt = 0.0

        #//Variables for stream 1 equations
        self.strm1massflownew = globe.CTMassFlowStrm1T0 #//kg/s
        self.dstrm1massflowdt = 0.0 #kg/s/s
        self.strm1pressureoutnew = globe.CTPStrm1Outlet #//Pa
        self.dstrm1pressureoutdt = 0.0 #//Pa/s
        self.strm1temperatureoutnew = globe.CTTStrm1Outlet #//Kelvin
        self.dstrm1temperatureoutnewdt = 0.0


    def copyfrom(self, baseclasscopyfrom):
        coolingtowercopyfrom = baseclasscopyfrom

        super(coolingtower, self).copyfrom(coolingtowercopyfrom)

        self.on.v = coolingtowercopyfrom.on.v
        self.nrstages = coolingtowercopyfrom.nrstages

        self.fanspeed.v = coolingtowercopyfrom.fanspeed.v

        self.fanpower.v = coolingtowercopyfrom.fanpower.v
        self.newfanpower = coolingtowercopyfrom.newfanpower; #W; The future steady state fan power.
        self.fanpowerstatespacex1 = coolingtowercopyfrom.fanpowerstatespacex1
        self.fanpowerstatespacex2 = coolingtowercopyfrom.fanpowerstatespacex2
        self.ddtfanpowerstatespacex1 = coolingtowercopyfrom.ddtfanpowerstatespacex1
        self.ddtfanpowerstatespacex2 = coolingtowercopyfrom.ddtfanpowerstatespacex2

        self.deltapressure = coolingtowercopyfrom.deltapressure

        self.tuningfactor = coolingtowercopyfrom.tuningfactor

        #U = coolingtowercopyfrom.U;
        #A = coolingtowercopyfrom.A;
        #//K = coolingtowercopyfrom.K;

        self.masstransfercoefair = coolingtowercopyfrom.masstransfercoefair
        self.heattransfercoefwater = coolingtowercopyfrom.heattransfercoefwater
        self.heattransfercoefair = coolingtowercopyfrom.heattransfercoefair

        self.wetbulbtemperature = coolingtowercopyfrom.wetbulbtemperature #Kelvin

        self.massfluxwater = coolingtowercopyfrom.massfluxwater #m3/s : Volume flow of water in the CT
        self.massfluxair = coolingtowercopyfrom.massfluxair #m3/s : Volume flow of air in the CT.

        for i in range(self.nrstages): self.segmentvolume[i] = coolingtowercopyfrom.segmentvolume[i]
        for i in range(self.nrstages): self.segmentvolumewater[i] = coolingtowercopyfrom.segmentvolumewater[i]
        for i in range(self.nrstages): self.segmentvolumeair[i] = coolingtowercopyfrom.segmentvolumeair[i]
        for i in range(self.nrstages): self.watersegment[i].copyfrom(coolingtowercopyfrom.watersegment[i])
        for i in range(self.nrstages): self.airsegment[i].copyfrom(coolingtowercopyfrom.airsegment[i])
        for i in range(self.nrstages): self.watersegmentflowout[i] = coolingtowercopyfrom.watersegmentflowout[i]
        for i in range(self.nrstages): self.airsegmentdryairflowout[i] = coolingtowercopyfrom.airsegmentdryairflowout[i]
        for i in range(self.nrstages): self.interfacetemperature[i] = coolingtowercopyfrom.interfacetemperature[i]
        for i in range(self.nrstages): self.interfaceabshumidity[i] = coolingtowercopyfrom.interfaceabshumidity[i]
        for i in range(self.nrstages): self.airabshumidity[i] = coolingtowercopyfrom.airabshumidity[i]
        for i in range(self.nrstages): self.massevap[i] = coolingtowercopyfrom.massevap[i]
        for i in range(self.nrstages): self.segmenttransferarea[i] = coolingtowercopyfrom.segmenttransferarea[i]
        for i in range(self.nrstages): self.segmentcontactarea[i] = coolingtowercopyfrom.segmentcontactarea[i]
        for i in range(self.nrstages): self.dTwaterdt[i] = coolingtowercopyfrom.dTwaterdt[i]
        for i in range(self.nrstages): self.dTairdt[i] = coolingtowercopyfrom.dTairdt[i]
        for i in range(self.nrstages): self.dhumidityairdt[i] = coolingtowercopyfrom.dhumidityairdt[i]

        self.outflow0temperatureoutnew = coolingtowercopyfrom.outflow0temperatureoutnew #Kelvin
        self.doutflow0temperatureoutnewdt = coolingtowercopyfrom.doutflow0temperatureoutnewdt #Kelvin/sec

        self.strm0valveop = coolingtowercopyfrom.strm0valveop
        self.strm0cv = coolingtowercopyfrom.strm0cv
        self.strm0temptau = coolingtowercopyfrom.strm0temptau
        self.strm0flowtau = coolingtowercopyfrom.strm0flowtau
        self.strm1flowcoefficient = coolingtowercopyfrom.strm1flowcoefficient
        self.strm1temptau = coolingtowercopyfrom.strm1temptau
        self.strm1flowtau = coolingtowercopyfrom.strm1flowtau

        self.strm0massflownew = coolingtowercopyfrom.strm0massflownew #kg/s
        self.dstrm0massflowdt = coolingtowercopyfrom.dstrm0massflowdt #kg/s/s
        self.strm0pressureinnew = coolingtowercopyfrom.strm0pressureinnew #Pa
        self.dstrm0pressureindt = coolingtowercopyfrom.dstrm0pressureindt #Pa/s
        self.strm0temperatureoutnew = coolingtowercopyfrom.strm0temperatureoutnew #Kelvin
        self.dstrm0temperatureoutnewdt = coolingtowercopyfrom.dstrm0temperatureoutnewdt #Kelvin

        #Stream 2 flow
        self.strm1massflownew = coolingtowercopyfrom.strm1massflownew #kg/s
        self.dstrm1massflowdt = coolingtowercopyfrom.dstrm1massflowdt #kg/s
        self.strm1pressureoutnew = coolingtowercopyfrom.strm1pressureoutnew #Pa
        self.dstrm1pressureoutdt = coolingtowercopyfrom.dstrm1pressureoutdt #Pa/s
        self.strm1temperatureoutnew = coolingtowercopyfrom.strm1temperatureoutnew #Kelvin
        self.dstrm1temperatureoutnewdt = coolingtowercopyfrom.dstrm1temperatureoutnewdt #Kelvin


    def selectedproperty(self, selection):
        if (selection >= self.nrcontrolpropinherited):
            diff = selection - self.nrcontrolpropinherited
            if diff == 0:
                return self.on
            elif diff == 1:
                return self.fanspeed
            elif diff == 2:
                return self.fanpower
            elif diff == 3:
                return self.watervolumefraction
            elif diff == 4:
                return self.masstransfercoefair
            elif diff == 5:
                return self.heattransfercoefwater
            elif diff == 6:
                return self.heattransfercoefair
            else:
                return None
        else: return super(coolingtower, self).selectedproperty(selection)


    def calcwetbulbtemp(self):
        Ta = globe.AmbientTemperature #local double
        RH = globe.RelativeHumidity #local double
        self.wetbulbtemperature = Ta * math.atan(0.151977 * math.pow(RH + 8.313659, 0.5)) + math.atan(Ta + RH) -  \
                math.atan(RH - 1.676331) + 0.00391838 * math.pow(RH, 1.5) * math.atan(0.023101 * RH) - 4.686035
        self.wetbulbtemperature = 290 #TEST


    def calcwatervapourpressure(self, temperature): #From the Antoine equation
        temp = utilities.kelvin2celcius(temperature) #local double
        return globe.ConvertmmHgtoPa * math.pow(10, globe.AAntoineWater - globe.BAntoineWater / \
            (globe.CAntoineWater + temp))


    def calcwatervapourpressurefromrelativehumidty(self, relativehumidity, temperature):
            #//Water vap pressure in Pa, from rel.humidity as a percentage
            #//and from the temperature in Kelvin
        vapourpressureatsaturation = self.calcwatervapourpressuresaturation(temperature) #local float
        return relativehumidity/100.0 * vapourpressureatsaturation


    def calcwatervapourpressuresaturation(self, temperature): #//From the Buck equation
        temp = utilities.kelvin2celcius(temperature) #local float
        return globe.BuckC1 * math.exp((globe.BuckC2 - temp / globe.BuckC3) * (temp / (globe.BuckC4 + temp)))


    def calcabshumidity(self, watervappressure):  #//Specific Humidity from Peries 8th edition
        return 0.622 * watervappressure / (globe.Ps - watervappressure) #//kg/kg


    def calcairheattransfercoef1(self): #//This is if we want to use the Lewis factor, 
                                            #which we might actually not want to use.
        self.heattransfercoefair = globe.CTLewisFactor * self.masstransfercoefair * \
                            globe.CTCpAir / CTDefaultSegmentContactArea


    def calcairheattransfercoef2(self): #//This is from McCabe's chapther on humidification processes and operations.
        self.heattransfercoefair = globe.CTLewisFactor * self.masstransfercoefair * globe.CTCpAir


    def updatefrompropertydialogue(self): #//When property dialogue is read, some properties need to be updated.
        self.calcairheattransfercoef2()
        #//if (linkedsprayvalve != null) 
        #//{ 
        #//    linkedsprayvalve.op.v = on.v; 
        #//}


    def ddt(self, simi, scaleslope):   #//Differential equations.  scaleslope is for RukgaKutta4
        self.fanpowerstatespacex1 = self.fanpower.v
        self.ddtfanpowerstatespacex1 = self.fanpowerstatespacex2
        #//ddtfanpowerstatespacex2 = -9 * fanpowerstatespacex1 - 2 * fanpowerstatespacex2 + 9 * newfanpower
        self.ddtfanpowerstatespacex2 = -globe.Rotatinga0 * self.fanpowerstatespacex1 - \
                globe.Rotatinga1 * self.fanpowerstatespacex2 + globe.Rotatingb0 * self.newfanpower

        self.dstrm0pressureindt = -1 / self.strm0flowtau * self.inflow[0].mat.P.v + 1 / self.strm0flowtau * self.strm0pressureinnew
        self.dstrm1pressureoutdt = -1 / self.strm1flowtau * self.outflow[1].mat.P.v + 1 / self.strm1flowtau * self.strm1pressureoutnew

        incomingwaterflow = 0.0 #local float
        incomingairflow = 0.0 #local float
        incomingT = 0.0 #local float
        incominghumidity = 0.0 #local float
        for i in range(self.nrstages): #//segments in tower are numbered from zero at the bottom of the 
                                                #tower, to nrstages - 1 at the top.
            if (i == self.nrstages - 1):
                incomingwaterflow = self.inflow[0].massflow.v
            else:
                incomingwaterflow = self.watersegmentflowout[i + 1]
            self.watersegmentflowout[i] = incomingwaterflow - self.massevap[i]

            if (i == 0):
                incominghumidity = self.calcabshumidity(self.calcwatervapourpressurefromrelativehumidty( \
                    self.inflow[1].mat.relativehumidity.v, self.inflow[1].mat.T.v))
            else:
                incominghumidity = (self.airabshumidity[i - 1] + scaleslope*self.dhumidityairdt[i - 1][0])

            if (i == 0):
                incomingairflow = self.inflow[1].massflow.v/(1 + incominghumidity) 
            else:
                incomingairflow = self.airsegmentdryairflowout[i - 1]
            self.airsegmentdryairflowout[i] = incomingairflow
            #//airsegmentflowout[i] = incomingairflow + massevap[i]; Since we are only interested in dry air flow, which will not change, in the tower
                                                                        #//there is no need for this line anymore.

            if (i == self.nrstages - 1):
                incomingT = self.inflow[0].mat.T.v
            else: 
                incomingT = (self.watersegment[i + 1].T.v + scaleslope*self.dTwaterdt[i + 1][0])
            self.dTwaterdt[i][0] = 1 / (self.watersegment[i].density.v*self.segmentvolumewater[i]) * \
                    (incomingwaterflow * incomingT - self.watersegmentflowout[i] * (self.watersegment[i].T.v + \
                    scaleslope * self.dTwaterdt[i][0])) - self.heattransfercoefwater.v * self.segmentcontactarea[i] * \
                    ((self.watersegment[i].T.v + scaleslope * self.dTwaterdt[i][0]) - self.interfacetemperature[i]) / \
                    (self.watersegment[i].totalCp/self.watersegment[i].massofonemole * self.watersegment[i].density.v * \
                    self.segmentvolumewater[i])

            if (i == 0):
                incomingT = self.inflow[1].mat.T.v
            else: 
                incomingT = (self.airsegment[i - 1].T.v + scaleslope*self.dTairdt[i - 1][0])
            self.dTairdt[i][0] = 1 / (self.airsegment[i].density.v*self.segmentvolumeair[i]) * \
                    (incomingairflow*incomingT - self.airsegmentdryairflowout[i]*(self.airsegment[i].T.v + \
                    scaleslope*self.dTairdt[i][0])) - self.heattransfercoefair.v * self.segmentcontactarea[i] * \
                    ((self.airsegment[i].T.v + scaleslope * self.dTairdt[i][0]) - self.interfacetemperature[i]) / \
                    (self.airsegment[i].totalCp/self.airsegment[i].massofonemole * self.airsegment[i].density.v * \
                    self.segmentvolumeair[i])
                
            self.dhumidityairdt[i][0] = (incomingairflow*incominghumidity + self.massevap[i] - 
                    (self.airabshumidity[i] + scaleslope*self.dhumidityairdt[i][0])* \
                    self.airsegmentdryairflowout[i])/(self.airsegment[i].density.v * self.segmentvolumeair[i])
                    #//(Total water mass in, minus total water mass out) / (total mass air in segment)


    def update(self, simi, historise):
        self.calcairheattransfercoef2() #//Assuming now that the heat transfer coef for air is linked to the mass transfer coeff.

        if (self.linkedsprayvalve != None):
            pass
            #//linkedsprayvalve.op.v = (on.v >= 0.5) ? 1:0;
                
        if (self.on.v < 0.5): 
            hybridfanspeed = globe.CTFanShutdownSpeed 
        else: 
            hybridfanspeed = self.fanspeed.v
        self.inflow[1].massflow.v = globe.CTMassFlowStrm1T0 * hybridfanspeed / globe.CTFanSpeedT0  #//This line is commented out when CT fitting is done.
        self.deltapressure = globe.CTDefaultFanDP * math.pow(hybridfanspeed / globe.CTFanSpeedT0, 2)
        self.newfanpower = globe.CTFanPowerT0 * math.pow(hybridfanspeed / globe.CTFanSpeedT0, 3)

        strm0pressureinold = self.strm0pressureinnew

        self.strm0pressureinnew = self.outflow[0].mat.P.v + \
            math.pow(self.inflow[0].massflow.v / (self.strm0cv * (self.strm0valveop + globe.Epsilon)), 2) * (self.inflow[0].mat.density.v)
        if (self.strm0pressureinnew / (strm0pressureinold + globe.Epsilon) > globe.CTPMaxFactorIncreaseperSampleT): #//Dynamic protection:
            #//if pressure changes too fast the diff. equations cannot solve.
            self.strm0pressureinnew = strm0pressureinold * globe.CTPMaxFactorIncreaseperSampleT

        self.strm1pressureoutnew = self.inflow[1].mat.P.v + self.deltapressure
        #//strm1pressureoutnew = inflow[1].mat.P.v -
        #//    Math.Pow(inflow[1].massflow.v / strm1flowcoefficient, 2) * (inflow[1].mat.density.v + global.Epsilon);

        self.massfluxwater = self.inflow[0].massflow.v / (globe.CTTotalInterfaceArea * self.watervolumefraction.v) #//The volume flow of water.
        self.massfluxair = self.inflow[1].massflow.v / (globe.CTTotalInterfaceArea *self.CTAirVolumeFraction) #//The volume flow of air.

        #//calcairheattransfercoef(); #//Update the air heat transfer coeff in case the water mass transfer coeff has changed.           

        for i in range(self.nrstages): #//Static equations that can be solved without integration.
            self.interfacetemperature[i] = -((self.masstransfercoefair.v * globe.DeltaHWater * (self.interfaceabshumidity[i] - self.airabshumidity[i]) - 
                    self.heattransfercoefwater.v*self.watersegment[i].T.v - self.heattransfercoefair.v*self.airsegment[i].T.v)/
                    (self.heattransfercoefair.v + self.heattransfercoefwater.v))
            self.interfaceabshumidity[i] = self.calcabshumidity(self.calcwatervapourpressuresaturation(self.interfacetemperature[i]))

            self.massevap[i] = self.masstransfercoefair.v * self.segmentcontactarea[i] * (self.interfaceabshumidity[i] - self.airabshumidity[i])
            #//watersegment[i].Cp[0] = watersegment[i].composition[0].m.calcCp(watersegment[i].T.v);
            #//airsegment[i].Cp[0] = airsegment[i].composition[0].m.calcCp(airsegment[i].T.v);
            
        self.ddt(simi, 0)
        for i in range(self.nrstages):
            self.dTwaterdt[i][1] = self.dTwaterdt[i][0]
            self.dTairdt[i][1] = self.dTairdt[i][0]
            self.dhumidityairdt[i][1] = self.dhumidityairdt[i][0]

        self.ddt(simi, self.h/2)
        for i in range(self.nrstages):
            self.dTwaterdt[i][2] = self.dTwaterdt[i][0]
            self.dTairdt[i][2] = self.dTairdt[i][0]
            self.dhumidityairdt[i][2] = self.dhumidityairdt[i][0]

        self.ddt(simi, self.h / 2)
        for i in range(self.nrstages):
            self.dTwaterdt[i][3] = self.dTwaterdt[i][0]
            self.dTairdt[i][3] = self.dTairdt[i][0]
            self.dhumidityairdt[i][3] = self.dhumidityairdt[i][0]

        self.ddt(simi, self.h)
        for i in range(self.nrstages):
            self.dTwaterdt[i][4] = self.dTwaterdt[i][0]
            self.dTairdt[i][4] = self.dTairdt[i][0]
            self.dhumidityairdt[i][4] = self.dhumidityairdt[i][0]

        for i in range(self.nrstages):
            self.watersegment[i].T.v += self.h / 6 * (self.dTwaterdt[i][1] + 2 * self.dTwaterdt[i][2] + 2 * self.dTwaterdt[i][3] + self.dTwaterdt[i][4])
            self.airsegment[i].T.v += self.h / 6 * (self.dTairdt[i][1] + 2 * self.dTairdt[i][2] + 2 * self.dTairdt[i][3] + self.dTairdt[i][4])
            self.airabshumidity[i] += self.h / 6 * (self.dhumidityairdt[i][1] + 2 * self.dhumidityairdt[i][2] + 2 * self.dhumidityairdt[i][3] + self.dhumidityairdt[i][4])

        self.fanpowerstatespacex1 += self.ddtfanpowerstatespacex1 * globe.SampleT
        self.fanpowerstatespacex2 += self.ddtfanpowerstatespacex2 * globe.SampleT

        self.fanpower.v = self.fanpowerstatespacex1
        if (self.fanpower.v < 0): self.fanpower.v = 0
            
        self.outflow[0].mat.T.v = self.watersegment[0].T.v
        self.outflow[1].mat.T.v = self.airsegment[self.nrstages - 1].T.v

        self.outflow[0].mat.copycompositiontothismat(self.inflow[0].mat)
        self.outflow[1].mat.copycompositiontothismat(self.inflow[1].mat)

        self.inflow[0].mat.P.v += self.dstrm0pressureindt * globe.SampleT
        #//outflow[0].mat.P.v = global.Ps; #//standard pressure since it is open to the atmosphere.
        self.outflow[0].massflow.v = self.watersegmentflowout[0]
        self.outflow[0].mat.density.v = self.watersegment[0].density.v

        self.outflow[1].mat.P.v += self.dstrm1pressureoutdt * globe.SampleT
        self.outflow[1].massflow.v = self.airsegmentdryairflowout[self.nrstages - 1]*(1 + self.airabshumidity[self.nrstages - 1])
        self.outflow[1].mat.density.v = self.airsegment[self.nrstages - 1].density.v

        if (self.outflow[0].mat.T.v < 0): self.outflow[0].mat.T.v = 0

        if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
            index = int(simi / globe.SimVectorUpdatePeriod)
            for i in range(self.nrstages):
                self.interfaceabshumiditysimvector[i][index] = self.interfaceabshumidity[i]
                self.airabshumiditysimvector[i][index] = self.airabshumidity[i]
                if (self.watersegment[i].T.simvector != None):
                    self.watersegment[i].T.simvector[index] = self.watersegment[i].T.v
                if (self.interfacetemperaturesimvector[i] != None):
                    self.interfacetemperaturesimvector[i][index] = self.interfacetemperature[i]

            if (self.fanpower.simvector != None):
                self.fanpower.simvector[index] = self.fanpower.v
            if (self.fanspeed.simvector != None):
                self.fanspeed.simvector[index] = hybridfanspeed
            if (self.on.simvector != None):
                self.on.simvector[index] = self.on.v
            if (self.masstransfercoefair.simvector != None):
                self.masstransfercoefair.simvector[index] = self.masstransfercoefair.v
            if (self.heattransfercoefwater.simvector != None):
                self.heattransfercoefwater.simvector[index] = self.heattransfercoefwater.v


    def setproperties(self, asim, aroot):   #public override void setproperties(simulation asim)
        diag = coolingtowerproperties(self, asim, aroot)


    def showtrenddetail(self):
        if not self.detailtrended:
            self.detailtrended = True
            self.allocatememory()
        else:
            self.detailtrended = False
            self.deallocatememory()


    def allocatememory(self):
        if self.fanpower.simvector == None or len(self.fanpower.simvector) != globe.SimVectorLength:
            self.fanpower.simvector = [0.0]*globe.SimVectorLength

        if self.fanspeed.simvector == None or len(self.fanspeed.simvector) != globe.SimVectorLength:
            self.fanspeed.simvector = [0.0]*globe.SimVectorLength

        for i in range(self.nrstages):
            if (self.watersegment[i].T.simvector == None or 
                len(self.watersegment[i].T.simvector) != globe.SimVectorLength):
                self.watersegment[i].T.simvector = [0.0]*globe.SimVectorLength

            if (self.interfacetemperaturesimvector[i] == None or 
                len(self.interfacetemperaturesimvector[i]) != globe.SimVectorLength):
                self.interfacetemperaturesimvector[i] = [0.0]*globe.SimVectorLength


    def deallocatememory(self):
        self.fanpower.simvector = None
        self.fanspeed.simvector = None

        for i in range(self.nrstages):
            self.watersegment[i].T.simvector = None
            self.interfacetemperaturesimvector[i] = None


    def dodetailtrend(self, plt):
        if self.detailtrended:
            figurenr = 0
            x = globe.SimTimeVector
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.interfaceabshumiditysimvector[0])
            axarr[0].set_title('interface humidity[0] kg/kg : ' + self.name)
            axarr[1].plot(x, self.interfaceabshumiditysimvector[4])
            axarr[1].set_title('interface humidity[4] kg/kg : ' + self.name)
            axarr[2].plot(x, self.interfaceabshumiditysimvector[9])
            axarr[2].set_title('interface humidity[9] kg/kg : ' + self.name)

            figurenr += 1
            plt.figure(figurenr)
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.airabshumiditysimvector[0])
            axarr[0].set_title('airabshumidity[0] kg/kg : ' + self.name)
            axarr[1].plot(x, self.airabshumiditysimvector[4])
            axarr[1].set_title('airabshumidity[4] kg/kg : ' + self.name)
            axarr[2].plot(x, self.airabshumiditysimvector[9])
            axarr[2].set_title('airabshumidity[9] kg/kg : ' + self.name)

            figurenr += 1
            plt.figure(figurenr)
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.watersegment[0].T.simvector)
            axarr[0].set_title('watersegment[0].T Kelvin : ' + self.name)
            axarr[1].plot(x, self.watersegment[4].T.simvector)
            axarr[1].set_title('watersegment[4].T Kelvin : ' + self.name)
            axarr[2].plot(x, self.watersegment[9].T.simvector)
            axarr[2].set_title('watersegment[9].T Kelvin : ' + self.name)

            figurenr += 1
            plt.figure(figurenr)
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.interfacetemperaturesimvector[0])
            axarr[0].set_title('interfacetemperaturesimvector[0] Kelvin : ' + self.name)
            axarr[1].plot(x, self.interfacetemperaturesimvector[4])
            axarr[1].set_title('interfacetemperaturesimvector[4] Kelvin : ' + self.name)
            axarr[2].plot(x, self.interfacetemperaturesimvector[9])
            axarr[2].set_title('interfacetemperaturesimvector[9] Kelvin : ' + self.name)

            figurenr += 1
            plt.figure(figurenr)
            f, axarr = plt.subplots(2, sharex=True)
            axarr[0].plot(x, self.fanpower.simvector)
            axarr[0].set_title('Fan Power Consumption (W) : ' + self.name)
            axarr[1].plot(x, self.fanspeed.simvector)
            axarr[1].set_title('Fan Speed (rps) : ' + self.name)


    def mouseover(self, x, y):
        return (x >= (self.location.x - 0.5 * globe.CTHESWidth) and x <= (self.location.x + 0.5 * globe.CTHESWidth) \
                and y >= (self.location.y - 0.5 * globe.CTHESHeight) and y <= (self.location.y + 0.5 * globe.CTHESHeight))


    def updateinoutpointlocations(self):
        #//Update in and out point locations;
        self.inpoint[0].x = self.location.x - 0.5 * globe.CTSWidth + globe.CTHESInPointsFraction[0] * globe.CTSWidth
        self.inpoint[0].y = self.location.y - 0.5 * globe.CTSHeight - globe.InOutPointWidth
        self.inpoint[1].x = self.location.x - 0.5 * globe.CTSWidth + globe.CTHESInPointsFraction[1] * globe.CTSWidth
        self.inpoint[1].y = self.location.y + 0.5 * globe.CTSHeight + globe.InOutPointWidth
        self.outpoint[0].x = self.location.x - 0.5 * globe.CTSWidth + globe.CTHESOutPointsFraction[0] * globe.CTSWidth
        self.outpoint[0].y = self.location.y + 0.5 * globe.CTSHeight + globe.InOutPointWidth
        self.outpoint[1].x = self.location.x - 0.5 * globe.CTSWidth + globe.CTHESOutPointsFraction[1] * globe.CTSWidth
        self.outpoint[1].y = self.location.y - 0.5 * globe.CTSHeight - globe.InOutPointWidth
        super(coolingtower, self).updateinoutpointlocations()


    def draw(self, canvas): #//public virtual void draw(Graphics G)
        self.updateinoutpointlocations()

        #//Draw main tank
        #GraphicsPath tankmain
        #Pen plotPen
        #float width = 1

        #tankmain = new GraphicsPath()
        #plotPen = new Pen(Color.Black, width)

        point0 = point(globe.OriginX + int(globe.GScale*(self.location.x - 0.5*globe.CTWidthDraw)), \
                    globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.CTHeightDraw)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.location.x - 0.5*globe.CTWidthDraw)), \
                    globe.OriginY + int(globe.GScale*(self.location.y - 0.5*globe.CTHeightDraw)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.location.x + 0.5*globe.CTWidthDraw)), \
                    globe.OriginY + int(globe.GScale*(self.location.y - 0.5*globe.CTHeightDraw)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.location.x + 0.5*globe.CTWidthDraw)), \
                    globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.CTHeightDraw)))
        
        polygon = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)

        #Point[] myArray = new Point[] 
         #   {new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - 0.5*global.CTWidthDraw)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.CTHeightDraw))), 
        #    new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - 0.5*global.CTWidthDraw)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y - 0.5*global.CTHeightDraw))), 
        #    new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + 0.5*global.CTWidthDraw)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y - 0.5*global.CTHeightDraw))), 
        #    new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + 0.5*global.CTWidthDraw)),
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.CTHeightDraw)))}
        #tankmain.AddPolygon(myArray)
        #plotPen.Color = Color.Black
        #SolidBrush brush = new SolidBrush(Color.White)
        #brush.Color = (highlighted) ? Color.Orange : Color.White
        #G.FillPath(brush, tankmain)
        #G.DrawPath(plotPen, tankmain)

        if (self.highlighted == True):
            canvas.itemconfig(polygon, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(polygon, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(polygon, fill='grey')

        #//Draw inpoint
        super(coolingtower, self).draw(canvas)




