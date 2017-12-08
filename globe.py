from enum import Enum, unique
import component as component
import molecule as molecule
import numpy as np
import math

#global enums ---------------------------------------------------------------------------------------------------------


@unique
class baseclasstypeenum(Enum):
    UnitOp = 1
    Stream = 2
    Block = 3


@unique
class calculationmethod(Enum):
    DetermineFlow = 1
    DeterminePressure = 2


@unique
class components(Enum):
    Naphtha = 0
    Air = 1


@unique
class datasourceforvar(Enum):
    Simulation = 1
    Exceldata = 2


@unique
class drawingmode(Enum):
    Nothing = 1
    Streams = 2
    Signals = 3
    GasPipes = 4
    LiquidPipes = 5


@unique
class materialphase(Enum):
    Solid = 1
    Liquid = 2
    Gas = 3


@unique
class nmpcalgorithm(Enum):
    UnconstrainedLineSearch = 1
    InteriorPoint1 = 2
    ActiveSet1 = 3
    GeneticAlgorithm1 = 4
    ParticleSwarmOptimisation1 = 5


@unique
class objecttypes(Enum):
    FTReactor = 1
    GasPipe = 2
    LiquidPipe = 3
    Pump = 4
    Tank = 5
    Valve = 6
    Tee = 7
    Mixer = 8
    Stream = 9
    PIDController = 10
    HX = 11
    HeatExchangerSimple = 12
    SteamGenerator = 13
    Flange = 14
    NMPC = 15
    CoolingTower = 16
    CoolingTowerSimple = 17
    CoolingTowerHeatExchangerSimple = 18
    istillationColumn = 19
    Signal = 20
    Selector = 21
    ControlMVSignalSplitter = 22






#Functions for globe.py ------------------------------------------------------------------------------------------------

def calcSampleT(): #return double
    return TimerInterval / 1000.0 * SpeedUpFactor #; // seconds - at this point SampleT 


def calcSimIterations(): #return int
    if (SampleT == 0): delta = 0.01
    else: delta = 0 #local var
    return int(SimTime / float(SampleT + delta)) #; //Nr of iterations of the simulation.


def calcSimVectorLength(): #return int
    if (SampleT == 0): delta = 0.01 #local var
    else: delta = 0
    return int(SimTime / float(SimVectorUpdateT + delta)) #; //Nr of iterations of the simulation.


def initsimtimevector():
    simtimevector = [0.0]*SimVectorLength
    simtimevector[0] = 0
    for i in range(1,len(simtimevector)):
        simtimevector[i] = simtimevector[i - 1] + SimVectorUpdateT
    return simtimevector


#Scientific constants -----------------------SOME OF THESE WILL LATER BE ABLE TO BE MOVED TO THE FLUID PACKAGE-----------------------------------------------------------------------------
g = 9.81 #; //m/s^2
R = 8.314 #; // J/Kelvin/molecule
Ps = 100000.0 #; //Pa
Ts = 273.15 # //Calvin
#//Water constants
WaterDensity = 1000.0 # //kg/m^3
DeltaHWater = 2257.0*1000.0 #//Joule / kg
#//Air constants
AirDensity = 1.225 #; //kg/m^3

#Timing constants 
TimerInterval = 1 #; // micro seconds
SpeedUpFactor = 200.0 #; //50, CT and normal sim: 200; //factor  Heat exchangers: 30000
SampleT = calcSampleT() #; //Function returns a value since then reader can see which function it is.
SimVectorUpdateT = 1.0 #; //CT: 1.0; //seconds; HX: 30s; normal sim with cooling tower: 1s.
SimVectorUpdatePeriod = int(round(SimVectorUpdateT / SampleT)) #; //Nr. samples between saving in vect.
TrendUpdateT = 1.0 #; //seconds.  The simulation period of updating trends in simulation.  
                                                 #//; HX: 30s; normal sim with cooling tower: 1s.
TrendUpdateIterPeriod = int(round(TrendUpdateT / SampleT)) #; //Nr. of samples between update trend.
SimTime = 3600.0*1 #; // Normal full model: 3600.0*4 ; CT alone:  64830; //seconds 3600*1;//3600*24;  135: ES004 53340 ; for 172EP004: 34440;for CT fitting: 12 hours/3hours.
SimIterations = calcSimIterations() #; //Nr of iterations of the simulation.
SimVectorLength = calcSimVectorLength() #;
PlantDataSampleT = 30.0 #; //30 seconds for CT;  The sample frequency of the IP.21 data used for fitting.
SimTimeVector = initsimtimevector()


#Calculation constants
Epsilon = 0.00000001 #//small number that is added to a denominator in order to divide by it safely.
ConvergeDiffFrac = 0.001 #//Fraction difference or less that will be treated as convergance.


#Screen constants 
GScale = 1600.0 / 100.0 #//pixels per m
OriginX = 0 #//pixels
OriginY = 0 #//pixels
DefaultLocationX = 0
DefaultLocationY = 0
MinDistanceFromPoint = 0.5 #//m : Minimum Distance from each point for it to be selected
MinDistanceFromGasPipe = 0.5 #//m : Minimum distance from each gas pipe for it to be selected
DetailTrendHighlightColour = 'blue' #colour to be used to highlight baseprocessclasses that will be detaile trended.


#Simulation-wide constants
RelativeHumidity = 80.0 #//%.  Average RH for Doha through the year.  Might need to make this an instantaneous figure later
                                                    #    on.  wwww.qatar.climatemps.com/humidity.php
AmbientTemperature = 25.0 + 273.0 #K.  To be converted to degC for Stull equation.  This is the average daily mean
                                                            #through out the year.  To be changed later based on when the simulation is run.
                                                            #Currently from en.wikipedia.org/wiki/Doha#Climate
HeCircuitFlowT0 = 85.0 #kg/s
SGPGasInlet = 65.0 * 100000.0 #Pa
SGPGasOutlet = 58.5 * 100000.0 #Pa
PBPGasInlet = 6.9e6 #Pa
PBPGasOutlet = 6.5e6 #Pa
PBTGasInlet = 259.1 + 273.0 #Kelvin.
PBTGasOutlet = 700.0 + 273.0 #Kelvin.


#//in and out point constants
InOutPointWidth = 0.2   #; //m
InOutPointHeight = 0.08   #; //m


#Material properties
AirMolarMass = 0.02897; #//kg/mol
CO2MolarMass = 0.018; #//kg/mol
H2OMolarMass = 0.0180153; #//kg/mol
HeMolarMass = 4.002602e-3; #//kg/mol


#Rounding constants
NormalDigits = 3 #nr of digits will be rounded to for display normally
PressureDigits = 6 #nr of digits pressure values will be rounded to for display


#application class constants --------------------------------------------------------------------------------------------
ModelFileExtension = '.csy' #.ChemSimpYthon


#baseprocessclass class default properties ------------------------------------------------------------------------------
baseprocessclassInitMass = 10.0  # //kg
baseprocessclassInitMassFlow = 0.0  # //kg/h
baseprocessclassInitPressure = 1.0 * Ps  # //Pa    210*Ps
baseprocessclassInitTemperature = Ts + 25.0  # //Kelvin.  25 degC   Ts + 170
baseprocessclassInitVolume = 1.0  # //m3


#chromosome class constants ------------------------------------------------------------------------------------------------------------------
DefaultMaxValueforMVs = 100 #//the top end of the frac/perc range of each MV.
MaxBinaryLengthChromosome = 7


#complex class constants -------------------------------------------------------------------------------------------
ZeroImaginary = 0.0001


#coolingtower class constants (CT) ---------This class is initially modelled on the Swedish paper, Marques later added-------------------------------------------------------------------------
CTRK4ArraySize = 5

CTHeight = 14.1  #/m
CTWidth = 14.4 #m
CTLength = 14.4 #m  
CTDefaultNrStages = 10  #The number of discretisations of the water, interface and air streams

CTDefaultFanDP = 211.9 #Pa.  Calculated on model Excel sheet.
CTDefaultFanTotalEfficiency = 0.866 #Fraction.  From CT datasheet.
CTFanSpeedT0 = 120.1 / 60.0 #revolutions per second; from data sheet for fan.
CTFanPowerT0 = 137000.0 #W; as per CT datasheet.
CTFanShutdownSpeed = 0.1 #rps.  Speed at shutdown to keep simulating the air that does exchange heat with the water when the fan is turned off.
        
#Below are the model paramaters for the second order power transient for the fans and pumps
RotatingPercOS = 50.0 # percentage overshoot
RotatingTsettle = 15.0 #seconds; settling time.
RotatingZeta = -math.log(RotatingPercOS/100)/(math.sqrt(math.pow(math.pi,2) + \
    math.pow(math.log(RotatingPercOS/100),2)))
#//public static double RotatingOmegaN = 4 / (RotatingZeta * RotatingTsettle)
RotatingOmegaN = -math.log(0.02 * math.sqrt(1 - math.pow(RotatingZeta, 2))) / \
    (RotatingZeta * RotatingTsettle)
#//public static double RotatingZeta = 0.4
#//public static double RotatingOmegaN = 1 / 8
        
Rotatingb0 = math.pow(RotatingOmegaN, 2)
Rotatinga0 = math.pow(RotatingOmegaN, 2)
Rotatinga1 = 2.0 * RotatingZeta * RotatingOmegaN
Rotatinga2 = 1.0

CTTotalInterfaceArea = CTWidth * CTHeight
CTTotalHorizontalArea = CTWidth * CTLength
CTTotalVolume = CTWidth * CTLength * CTHeight
CTFillVolume = 1161.0 #m^3;  as per CT data sheet.
CTDefaultSegmentVolume = CTWidth * CTLength * CTHeight / CTDefaultNrStages

CTWaterVolumeFraction = 0.1
CTPackingVolumeFraction = CTFillVolume / CTTotalVolume
CTAirVolumeFraction = 1.0 - CTWaterVolumeFraction - CTPackingVolumeFraction
        
CTDropletRadius = 0.001 #m; Assumption  0.001
CTDropletVolume = 4.0 / 3.0 * math.pi * math.pow(CTDropletRadius, 3)
        
CTDropletSurfaceArea = 4.0 * math.pi * math.pow(CTDropletRadius, 2)

CTLewisFactor = 1.0 #This is from Lewis' work.
CTCpAir = 1013.0 #J/kgK; At 400K.

CTTransferCoefCoef = 1.0 / CTDefaultSegmentVolume #Multiplier to scale all the 
CTDefaultMassTransferCoefficientAir = 0.000657 # kg/(s*m^2) 0.0001; CTTransferCoefCoef*2.71E-14; //; fitted value . 9.2688E-07
CTDefaultHeatTransferCoefficientWater = 64.395 #W/(m^2*K) . 1.0; fitted value .CTTransferCoefCoef*14.814
CTDefaultHeatTransferCoefficientAir = 0.6658  #W/(m^2*K) . 1.0; fitted value .CTTransferCoefCoef*5.729;
        
CTNIn = 2  #One flow in is water (strm1), the other is air (strm2).
CTNOut = 2

AAntoineWater = 8.07131 #Antoine equation coefficients for water vapour pressure.  This is for the equation yielding mmHg
BAntoineWater = 1730.63
CAntoineWater = 233.426
AbsHumidityConst = 2.16679 / 1000.0 #kg*K/J
ConvertmmHgtoPa = 133.3223 #Pa per mmHg

WaterSatPressC1 = -7.85951
WaterSatPressC2 = 1.844
WaterSatPressC3 = -11.786
WaterSatPressC4 = 22.68
WaterSatPressC5 = -15.96
WaterSatPressC6 = 1.801

BuckC1 = 611.21
BuckC2 = 18.678
BuckC3 = 234.5
BuckC4 = 257.14

CTTuningFactor = 0.9 #factor to throttle the amount of cooling for tuning the total model purposes (to be removed later).

CTHeightDraw = 5.0 #meter
CTWidthDraw = 5.0 #meter
CTInPointsFraction = [0.1, 0.9] #input 1: Cooling water return
CTOutPointsFraction = [0.10, 0.9] #Output 1: Cooling water supply

CTTemperatureTau = 15.0 * 60.0 ##seconds.  From Muller Craig article.

#Strm1 is normally the warm stream, and Strm2 the cold stream.  So for the CT strm1 will then be the water that is coming in, and strm2 the air.
CTDefaultU = 497.0 #from datasheet    330 * 1000000 / 3600; //W/(m^2*K);  Taken from the Muller/Craig article and converted to SI units.
CTDefaultA = 287.0 #m^2 ; From the Muller/Craig article this figure would have been 100.

CTMassFlowStrm0T0 = 6169960.0 / 3600.0 #kg/s , based on Flows to Equipment sheet.
CTMolFlowStrm0T0 = CTMassFlowStrm0T0 / H2OMolarMass #MOLAR MASS here is for the water flow then back from the plant.
        
CTMassFlowStrm1T0 = 2340671.0/3600.0 #kg/s , from fitted data per cooling tower.
CTMolFlowStrm1T0 = CTMassFlowStrm1T0 / AirMolarMass #MOLAR MASS TO BE CHANGED HERE TO BE GENERIC
    
CTPStrm0Inlet = 2.0 * Ps + Ps #Pa  2.0 barg
CTPStrm0Outlet = Ps
CTPStrm1Inlet = Ps
CTPStrm1Outlet = CTPStrm1Inlet - 0.1 * Ps #THE FAN MODEL WILL NEED TO BE ADDED HERE LATER TO MAKE THIS MORE ACCURATE.

CTTStrm0Inlet = 273.0 + 45.0 #Kelvin (water)
CTTStrm0Outlet = 273.0 + 35.0 #Kelvin (water)
CTTStrm1Inlet = AmbientTemperature #Kelvin (air)
CTTStrm1Outlet = 273.0 + 39.6 #Kelvin (air)

CTTInterfaceT0 = 0.5 * (CTTStrm0Inlet + CTTStrm1Inlet)

CTStrm0ValveOpeningDefault = 1.0 #fraction
CTStrm0Cv = CTMassFlowStrm0T0/CTStrm0ValveOpeningDefault / math.sqrt((CTPStrm0Inlet - CTPStrm0Outlet) / WaterDensity)

CTPMaxFactorIncreaseperSampleT = 2.0

CTStrm1FlowCoefficient = CTMassFlowStrm1T0 / math.sqrt((CTPStrm1Inlet - CTPStrm1Outlet) / AirDensity)
CTStrm0TempTau = CTTemperatureTau #seconds.  
CTStrm1TempTau = CTTemperatureTau #seconds.  
CTStrm0FlowTau = 60.0 #seconds.  Based on Muller-Craig.
CTStrm1FlowTau = 60.0 #seconds.  Based on Muller-Craig.


#//coolingtowerheatexchangersimple class constants (CTHES) -------------------------------------------------------------------------------------
CTHESNIn = 2  #//One flow in is water (strm1), the other is air (strm2).
CTHESNOut = 2
CTHESHeight = 5.0 #meter
CTHESWidth = 5.0 #meter
CTHESInPointsFraction = [0.1, 0.9] #input 1: Cooling water return
CTHESOutPointsFraction = [0.10, 0.9] #Output 1: Cooling water supply


#//coolingtowersimple class constants (CTS) ---------------------------------------------------------------------------------------------------
CTSHeight = 5.0 #meter
CTSWidth = 5.0 #meter


#//heatexchanger class constants -----------------------------------------------------------------------------------------
HEThermalPower = 5*1000000.0 #//W  200.0 * 1000000   - > 200 MW.
HeatExchangerNIn = 2
HeatExchangerNOut = 2
HeatExchangerInPointsFraction = [0.05, 0.95] #//input 1: Hot Gas feed, Input 2: Water
HeatExchangerOutPointsFraction = [0.05, 0.95] #//Output 1: Cooled Gas, Output 2: Steam.
HeatExchangerRadius = 1.0 #//m
HeatExchangerWidth = 6.0 #//m
        

NStrm2Coils = 455
HENSegments = 3
HENNodes = HENSegments + 1 #//The nodes are the boundaries, and the segements are what is between the nodes.

#//This is based on the Modelling design Excel file and Areva design.
        

HETStrm1Inlet = 188.0 + 273.0  #//699.9 + 273 #//K
HETStrm1Outlet = 45.0 + 273.0 #//244.7 + 273   #//245 + 273; #//K
HETStrm2Inlet = 35.0 + 273.0 #//35 + 273;//170.0 + 273 #//K
HETStrm2Outlet = 45.0 + 273.0 #//325 + 273;//530 + 273 #//K

HEPStrm1Inlet = 10.3*100000.0 #//65 * 100000 #//Pa
HEPStrm1Outlet = HEPStrm1Inlet - 0.97 * 100000.0 #;//58.5 * 100000 #//Pa
HEPStrm2Inlet = 1*100000  #;//210 * 100000  # //Pa
HEPStrm2Outlet = HEPStrm2Inlet - 0.46*100000.0  #;//HEPStrm2Inlet - 20 * 100000 #//Pa

HEPStrm1Delta = (HEPStrm1Inlet - HEPStrm1Outlet) / (HENSegments) #//Not NSegments plus 1 since 
#//outflow[0] is now going to 
#//just be an extension of the final
#//segment
HEPStrm2Delta = (HEPStrm2Inlet - HEPStrm2Outlet) / (HENSegments)

HETStrm1T0 = [HETStrm1Outlet, 0.5 * (HETStrm1Outlet + HETStrm1Inlet), HETStrm1Inlet]
HETStrm2T0 = [HETStrm2Inlet, 0.5 * (HETStrm2Inlet + HETStrm2Outlet), HETStrm2Outlet]
HEPStrm1T0 = [HEPStrm1Outlet, HEPStrm1Inlet - 2*HEPStrm1Delta, HEPStrm1Inlet - HEPStrm1Delta]
HEPStrm2T0 = [HEPStrm2Inlet - HEPStrm2Delta, HEPStrm2Inlet - 2*HEPStrm2Delta, HEPStrm2Inlet - 3*HEPStrm2Delta]

HEMassFlowStrm1T0 = 99600.0 / 3600.0 / NStrm2Coils #//kg/s Per tube.
HEMassFlowArrayStrm1T0 = [HEMassFlowStrm1T0, HEMassFlowStrm1T0, HEMassFlowStrm1T0, HEMassFlowStrm1T0] #//kg/s  From AREVA design.
MolFlowStrm1T0 = HEMassFlowStrm1T0 / CO2MolarMass #//MOLAR MASS TO BE CHANGED HERE TO BE GENERIC

HEMassFlowStrm2T0 = 477000.0 / 3600.0 / NStrm2Coils #//kg/s  Needs to be slighly higher
MolFlowStrm2T0 = HEMassFlowStrm2T0 / H2OMolarMass #//MOLAR MASS TO BE CHANGED HERE TO BE GENERIC

#//heatexchanger class : Metal differential equation constants in particular
HEM = 0.1  #//2.42305008 #//kg/m; The mass of steam tube per unit length.  From Excel sheet where the properties

#//heatexchanger class : pressure drop / energy drop due to friction constants
#///public static double HEAddFriction = 10.0;
HEStrm1AddFriction = 0.1 #//1
HEStrm2AddFriction = 1.0 #//1,   10.0;
HEStrm1DeltaPK = [1.0, (HEPStrm1T0[1] - HEPStrm1T0[0]) / math.pow(MolFlowStrm1T0, 2.0), 
                                                    (HEPStrm1T0[2] - HEPStrm1T0[1]) / math.pow(MolFlowStrm1T0, 2.0), 
                                                    (HEPStrm1Inlet - HEPStrm1T0[2]) / math.pow(MolFlowStrm1T0, 2.0)]

HEStrm2DeltaPK = [(HEPStrm2Inlet - HEPStrm2T0[0]) / math.pow(MolFlowStrm2T0, 2.0), 
                                                    (HEPStrm2T0[0] - HEPStrm2T0[1]) / math.pow(MolFlowStrm2T0, 2.0), 
                                                    (HEPStrm2T0[1] - HEPStrm2T0[2]) / math.pow(MolFlowStrm2T0, 2.0),
                                                    1.0]
#//public static double[] HEStrm2DeltaPK = HEPStrm2Delta / Math.Pow(MolFlowStrm2T0, 2.0);
        
#//heatexchanger class : heat exchange constants
HEHeatExchangeSurfaceArea = 329.0 #//m2
HEOutsideDiameterTube = 19.05 / 1000.0 #//m
HETubeWallThickness = 2.11 / 1000.0 #//m
HEInsideDiameterTube = HEOutsideDiameterTube - 2.0 * HETubeWallThickness #//m
HENrPassesThroughShell = 2.0
HETubeCircOutside = math.pi * HEOutsideDiameterTube  #//m; Tube Circumferance on the outside.  
HETubeCircInside = math.pi * HEInsideDiameterTube  #//m; Tube Circumferance on the inside.  
HETubeCircAve = 0.5 * (HETubeCircOutside + HETubeCircInside)
HEAveLengthPerTube = 6.1   #//6.1 //102.6490726; #//m; Lenth per tube in AREVA design as per sheet.
HEAveLengthPerSegment = HEAveLengthPerTube / HENSegments
HEAStrm2 = math.pi * math.pow(HEInsideDiameterTube / 2.0, 2.0) #//m2; Cross sectional area of the pipes for the steam/water
HEStrm2TubeVolume = HEAStrm2* HEAveLengthPerTube   #//0.042648188; #//m^3
HEStrm2SegmentVolume = HEStrm2TubeVolume / HENSegments   # //m^3
HEShellVolume = 1.040 * 6.096 - HEStrm2TubeVolume * NStrm2Coils
HEStrm1TubeVolume = HEShellVolume / NStrm2Coils  # //3.641659803 #//m^3
HEAStrm1 = HEStrm1TubeVolume / HEAveLengthPerTube  #//m2;  From Excel sheet from AREVA design.
HEEffGasTubeCircInside = 2.0 * math.sqrt(HEAStrm1 / math.pi) * math.pi #//2 * math.sqrt(HEAStrm1 / math.pi) * math.pi;
HEStrm1SegmentVolume = HEStrm1TubeVolume / HENSegments #//m^3
HERi = 0.0001  #//0.001;  #// K∙s³/kg = K m^2 / W .  Thermal conductivity's reciprocal times thickness of wall.
        
#//public static double HEAg = 0.035476792;  //m2;  From Excel sheet from AREVA design.
HEInPointsFraction = [0.05, 0.95] #//input 1: Hot Gas feed, Input 2: Water
HEOutPointsFraction = [0.05, 0.95] #//Output 1: Cooled Gas, Output 2: Steam.
#//public static double HETubeDiameter = 0.023; //m; Diameter of the tubes in the steam generator.  From Excel sheet
#//public static double HEAs = math.pi * Math.Pow(HETubeDiameter / 2.0, 2.0); //m2; Cross sectional area of the pipes for the steam/water

#//thermal resistivity of the metal times the tube thickness.
#//This kgm and Ri, needs to be backed up with some more science.  Why is it so 
#//dificult to get these values and to fix things up properly?
HECsi = 0.1  #//0.8;  //Dimensionless. These values need to be backed up with some more research.  Why is it so difficult to 
#//get proper values for these?
HECgi = 0.1 #//0.8;  //Dimensionless. These values need to be backed up with some more research.  Why is it so difficult to 
#//get proper values for these? 
HEHeatTransferArea = HETubeCircAve * HEAveLengthPerTube / HENSegments
HEKgm = [(HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
            (HEThermalPower*1.0 / NStrm2Coils) - HERi*0.5) /
            math.pow(HEMassFlowStrm1T0,-HECgi),
            (HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
            (HEThermalPower*1.0 / NStrm2Coils) - HERi*0.5) /
            math.pow(HEMassFlowStrm1T0,-HECgi),
            (HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
            (HEThermalPower*1.0 / NStrm2Coils) - HERi*0.5) /
            math.pow(HEMassFlowStrm1T0,-HECgi)]
HEKms = [(HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
            (HEThermalPower*1.0 / NStrm2Coils) - HERi*0.5) /
            math.pow(HEMassFlowStrm2T0,-HECsi),
            (HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
            (HEThermalPower*1.0 / NStrm2Coils) - HERi*0.5) /
            math.pow(HEMassFlowStrm2T0,-HECsi),
            (HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
            (HEThermalPower*1.0 / NStrm2Coils) - HERi*0.5) /
            math.pow(HEMassFlowStrm2T0,-HECsi)]
#//public static double[] HEKgm = new double[] {(HEHeatTransferArea * (0.5 * (HETStrm1T0[0] - HETStrm2T0[0])) /
#//    (HEThermalPower*1 / NStrm2Coils / HENSegments) - HERi*0.5) /
#//    Math.Exp(-HEMassFlowStrm1T0*HECgi),
#//    (HEHeatTransferArea * (0.5 * (HETStrm1T0[1] - HETStrm2T0[1])) /
#//    (HEThermalPower*1 / NStrm2Coils / HENSegments) - HERi*0.5) /
#//    Math.Exp(-HEMassFlowStrm1T0*HECgi),
#//    (HEHeatTransferArea * (0.5 * (HETStrm1T0[2] - HETStrm2T0[2])) /
#//    (HEThermalPower*1 / NStrm2Coils / HENSegments) - HERi*0.5) /
#//    Math.Exp(-HEMassFlowStrm1T0*HECgi)};
#//public static double[] HEKms = new double[] {(HEHeatTransferArea * 0.5 * (HETStrm1T0[0] - HETStrm2T0[0]) /
#//    (HEThermalPower*1 / NStrm2Coils / HENSegments) - HERi*0.5) /
#//    Math.Exp(-HEMassFlowStrm2T0*HECsi),
#//    (HEHeatTransferArea * 0.5 * (HETStrm1T0[1] - HETStrm2T0[1]) /
#//    (HEThermalPower*1 / NStrm2Coils / HENSegments) - HERi*0.5) /
#//    Math.Exp(-HEMassFlowStrm2T0*HECsi),
#//    (HEHeatTransferArea * 0.5 * (HETStrm1T0[2] - HETStrm2T0[2]) /
#//    (HEThermalPower*1 / NStrm2Coils / HENSegments) - HERi*0.5) /
#//    Math.Exp(-HEMassFlowStrm2T0*HECsi)};


#//heatexchangersimple (HES) class constants  -----------------------------------------------------------------------------
#//Strm1 is normally the warm stream, and Strm2 the cold stream 
HeatExchangerSimpleDefaultU = 500.0 #// 497 from datasheet    330 * 1000000 / 3600; //W/(m^2*K);  Taken from the Muller/Craig article and converted to SI units.
HeatExchangerSimpleDefaultA = 441.0 #// 287 m^2 ; From the Muller/Craig article this figure would have been 100.

HESMassFlowStrm1T0 = 325000.0 / 3600.0 #//kg/s , biggest CW exchanger in CW circuit.
HESMolFlowStrm1T0 = HESMassFlowStrm1T0 / CO2MolarMass #//MOLAR MASS TO BE CHANGED HERE TO BE GENERIC
HESMassFlowStrm2T0 = 1366538.0 / 3600.0 #//kg/s , for the whole strm2.
HESMolFlowStrm2T0 = HEMassFlowStrm2T0 / H2OMolarMass #//MOLAR MASS TO BE CHANGED HERE TO BE GENERIC

HESPStrm1Inlet = 3.7*Ps + Ps #//Pa
HESPStrm1Outlet = HESPStrm1Inlet - 0.5*Ps
HESPStrm2Inlet = 3.5*Ps + Ps
HESPStrm2Outlet = HESPStrm2Inlet - 2 * Ps

HESStrm1FlowCoefficient = \
    HESMassFlowStrm1T0/math.sqrt((HESPStrm1Inlet - HESPStrm1Outlet)/WaterDensity) # //SPECIFIC GRAVITY OF THE STREAM TO BE ADDED LATER TO THIS CALC 
HESStrm2FlowCoefficient = 10.21076364 #//This is fitted in the model - average one for all exchangers in model.  
HESStrm1TempTau = 6.0 * 60.0;#//seconds.  Based on Muller-Craig.
HESStrm2TempTau = 6.0 * 60.0 #//seconds.  Based on Muller-Craig.
HESStrm1FlowTau = 60.0 #//seconds.  Based on Muller-Craig.
HESStrm2FlowTau = 60.0 #//seconds.  Based on Muller-Craig.

HESNSegments = 2 #//For the simple heat exchanger, the inflow and outflow streams on the two sides will be modelled as the only
                                            #//2 segments.
HESNStrm2Coils = 1 #//heatexchangersimple class will be modelled with one big coild for strm2 only.

#//heatexchangersimple class : heat exchange constants
#//public static double HEHeatExchangeSurfaceArea = 329; //m2
#//public static double HEOutsideDiameterTube = 19.05 / 1000.0; //m
#//public static double HETubeWallThickness = 2.11 / 1000.0; //m
#//public static double HEInsideDiameterTube = HEOutsideDiameterTube - 2 * HETubeWallThickness; //m
#//public static double HENrPassesThroughShell = 2.0;
#//public static double HETubeCircOutside = math.pi * HEOutsideDiameterTube;  //m; Tube Circumferance on the outside.  
#//public static double HETubeCircInside = math.pi * HEInsideDiameterTube;  //m; Tube Circumferance on the inside.  
#//public static double HETubeCircAve = 0.5 * (HETubeCircOutside + HETubeCircInside);
#//public static double HEAveLengthPerTube = 6.1; //6.1; //102.6490726; //m; Lenth per tube in AREVA design as per sheet.
#//public static double HEAveLengthPerSegment = HEAveLengthPerTube / HENSegments;
#//public static double HEAStrm2 = math.pi * Math.Pow(HEInsideDiameterTube / 2.0, 2.0); //m2; Cross sectional area of the pipes for the steam/water
#//public static double HEStrm2TubeVolume = HEAStrm2 * HEAveLengthPerTube; //0.042648188; //m^3
HESStrm2Volume = HEStrm2TubeVolume * NStrm2Coils
HESStrm2SegmentVolume = HESStrm2Volume / HENSegments #//m^3
HESShellVolume = 1.040 * 6.096 - HESStrm2Volume
HESStrm1TubeVolume = HEShellVolume / NStrm2Coils #//3.641659803; #//m^3
#//public static double HEAStrm1 = HEStrm1TubeVolume / HEAveLengthPerTube;  //m2;  From Excel sheet from AREVA design.
#//public static double HEEffGasTubeCircInside = 2 * math.sqrt(HEAStrm1 / math.pi) * math.pi;//2 * math.sqrt(HEAStrm1 / math.pi) * math.pi;
HESStrm1SegmentVolume = HESShellVolume / HESNSegments #//m^3



#material class constants ---------------------------------------------------------------------------------------------------------------------
Udefault = 19500 * 100000.0 #Joule
Vdefault = 18.01528 * 100000 / 1000 / 1000 #m^3
fdefault = 0.5 #Vapour molar fraction. just a value in order to get some convergiance. 
MaterialInitPhase = materialphase.Liquid
NMaterialIterations = 10
ZNotDefined = -999999.0
epsilonadd = 0.0001; #for derivatives where the denominator is added to the variable being differentiated with respect to, and not
        #multiplied.
epsilonfrac = 1.001
Inf = 9999999999.0


#mixer class constants ------------------------------------------------------------------------------------------------------------------------
MixerLength = 1.0 #m
MixerDistanceBetweenBranches = 1.0 #m
MixerDefaultNIn = 2
MixerBranchThickness = 0.2 #m
MixerInitRadiusDefault = MixerDefaultNIn * (MixerDistanceBetweenBranches + MixerBranchThickness)


#nmpc class constants ----------------------------------------------------------------------------------------------------------------------
NMPCWidth = 2.0 #m
NMPCHeight = 2.0 #m
DefaultN = 9000 #3000; //Default Optimisation horison 80
DefaultInitialDelay = 0
DefaultRunInterval = 300 #Assuming TSample is 10 sec, so then the interval would be a multiple of 
                                                    #//that.
Defaultalphak = 1.0 #0.1; //0.1   0.001; //How much of line search delta is implemented.
DefaultNMPCAlgorithm = nmpcalgorithm.ParticleSwarmOptimisation1 #nmpcalgorithm.ParticleSwarmOptimisation1; //nmpcalgorithm.UnconstrainedLineSearch;
DefaultNMPCSigma = 0.8 #Multiplier of mubarrier for each iteration of the nmpc algorithm.
MeanWidthNMPCGUILB = 11

#Interior Point 1 - ConstrainedLineSearch algorithm constants
DefaultMuBarrier = 0.00000000000000001 #initial value / guess , for initialisation.
Defaultsvalue = 0.6 #since the constraints at this point are the valve openings in ChemSim, a fraction half will be
                                                        #the initial value of the valve openings, and thus the values will be 0.5 away from zero.
DefaultsvalueMultiplier = 0.9#//1.0;
#//public static double DefaultSigma = 0.1; //The fraction multiplied with mubarrier at the end of each iteration.
DefaulttauIP = 0.95 #Tau constant for Interior Point methods.
DefaultIPErrorTol = 0.0001 #If the max of the norm is below this figure, then the algorithm will stop, and we are close enough to a solution.
CholeskyDelta = 0.01 #small delta used in Hessian modification.
CholeskyBeta = 1000000.0 #Big value that will be used to try and cut down D matrix values if they become too large in Hessian modification.
MVMaxMovePerSampleTT0 = 0.1 #Fraction of MV range.
NMPCIPWeightPreTerm = 1.0
NMPCIPWeightTerminal = 10.0

#Genetic Algorithm 1 constants (mostly default values for variables in the nmpc class).
DefaultNrChromosomes = 12 #The total number of total solutions that will be kept in memory each iteration.
DefaultNrSurvivingChromosomes = 9 #Nr of chromosomes that will be passed to the next iteration and not replaced by new random ones.
DefaultNrPairingChromosomes = 8 #The nr of chromosomes of the total population that will be pairing and producing children.
DefaultProbabilityOfMutation = 0.1 #The probability that a child will be mutated in one bit.
DefaultNrIterations = 10 #The number of iterations until the best GA solution will be passed to the update method.
DefaultCrossOverPoint = 3 #Bit index nr (starting from zero) from right to left in the binary representation, where
                                                     #cross over and mutation will start.
        
#PSO constants
DefaultNrContinuousParticles = 20 #The total number of total solutions that will be kept in memory each iteration.
#//public static int DefaultNrParticles = 20; //The total number of total solutions that will be kept in memory each iteration.
DefaultNrBooleanParticles = DefaultNrContinuousParticles #The total number of total solutions that will be kept in memory each iteration.
PSOMVBoundaryBuffer = 10 #Distance from boundary that particles are put at random when they cross the boundary.
PSOMaxBooleanSpeed = 1.0 #Max probability paramater for sigmoid function for boolean PSO.


#pidcontroller class constants -------------------------------------------------------------------------------------------------------------
Direct = -1
Reverse = 1
PIDControllerInitRadius = 0.4; #//m
IDControllerInitK = 1.0
PIDControllerInitI = 100.0
PIDControllerInitD = 0.0
PIDControllerInitMinOP = 0.0 #Engineering units.
PIDControllerInitMaxOP = 1.0 #Engineering units.
PIDControllerInitMinPV = 0.0 #Engineering units.
PIDControllerInitMaxPV = 1.0 #Engineering units.


#pump class default properties -------------------------------------------------------------------------------------------------------------
PumpInitMaxDeltaPressure = 6.7*2*100000.0 #Pa
PumpInitMinDeltaPressure = 0.0 #Pa
PumpInitMaxActualFlow = 8700000*2/2.0 / 3600.0 / 1000.0 #m3/s  Dividing by 2 since we will now have 2 pumps in parallel.
                                                                                    #assume a density of 1000 as well.
PumpMinActualFlow = 0.01 * PumpInitMaxActualFlow #This is for when the pumps is off its curve due to too high DP.
PumpCurveYAxis = WaterDensity * g * 70.0 #/Pa.  Making this more than the data sheet for now to make sure the pump
                                                                     #can survive well at that level.
PumpCurvef1 = 8500.0/3600.0 #m3/s;  Actual flow.  From pump data sheet.
PumpCurvep1 = WaterDensity * g * 50.0 #Pa
PumpCurvef2 = 15000.0 / 3600.0 #m3/s; Actual flow.
PumpCurveSpeedT0 = 740.0 / 60.0 #rev per second.  From pump data sheet.
PumpSpeedTau = 60.0 #seconds.
        
PumpInitActualVolumeFlow = 0.0 #m3/s
PumpInitOn = 1.0 #0 for off, 1 for on
PumpInitRadius = 0.4 #m
PumpInitOutletLength = 0.5 #m
PumpInitOutletRadius = 0.05 #m


#stream class default properties -------------------------------------------------------------------------------------------------------------
SignalNrPropDisplay = 1
MinDistanceFromStream =  15.0 #//pixels  0.5; //m Minimum distance from each stream for it to be selected
StreamArrowAngle = 30.0 / 180.0 * math.pi  #; //radians
StreamArrowLength = 0.5 #//m
StreamMaxMassFlow = 100000000.0 #//kg/s (100,000 tps)
StreamMinMassFlow = -StreamMaxMassFlow
StreamNrPropDisplay = 3


#//tank class default properties ----------------------------------------------------------------------------------------------------------------
TankInitRadius = 22.0 #//12.88280927; //m; from Cooling tower sump design info.
TankInitHeight = 13.2 #//13.2; //m; //from cooling tower sump design.
TankRadiusDraw = 6.0 #//meter
TankHeightDraw = 2.0 #//meter
TankInitMaxVolume = math.pi * math.pow(TankInitRadius, 2) * TankInitHeight #//m3
TankInitFracInventory = 0.5 #//Fraction
TankInitInOutletDistanceFraction = 0.95 #//fraction from the bottom or top that the inlet or outlet of the tank will be situated.
TankMinFracInventory = 0.02 #//fraction 


#tee class constants --------------------------------------------------------------------------------------------------------------------------
TeeLength = 1.0 #m
TeeDistanceBetweenBranches = 1.0 #m
TeeDefaultNOut = 2
TeeBranchThickness = 0.2 #m
TeeInitRadiusDefault = TeeDefaultNOut * (TeeDistanceBetweenBranches + TeeBranchThickness)


#valve class constants -----------------------------------------------------------------------------------------------------------------------
ValveDefaultActualFlow = 800 / 3600.0 #//From average HX flow in unit CW circuit.
ValveDefaultDP = 1.2 * Ps
ValveDefaultOpening = 0.5 #//Default valve opening.
        
ValveEqualPercR = 40.0 #//Dimensionless constant for valve equalpercentage.
ValveDefaultCv = ValveDefaultActualFlow /   \
    (math.pow(ValveEqualPercR, ValveDefaultOpening - 1) * math.sqrt(ValveDefaultDP)) # //m^3/s/(Pa^0.5)
ValveHydraulicTau = 10.0  #//seconds.  Time constant of valve hydraulics.

ValveLength = 0.5 #//m
ValveWidth = 0.4 #//m


#fluidpackage constants -------------------------------------------------------------------------------------------------
fluidpackage = list() #list of component object
fluidpackage.append(component.component(molecule.molecule("Naphtha", "GTL Naphtha", 0.157, 0.00164, 661.4959, 273 + 495, 1.2411 * 10**7, \
                -1 - np.log10(110000 /1.2411 * (10**7)) , 150.5, 0.6, 0, 0), 0))
fluidpackage.append(component.component(molecule.molecule("Air", "Air", 0.02897, 1.983 * math.pow(10, -5), 1.225, 132.41, \
                3.72 * math.pow(10, 6), \
                0.0335,
                0.8*31.15  + 0.2*28.11, 0.8*(-0.01357)  + 0.2*(-3.7) * math.pow(10, -6), 0.8*2.68*math.pow(10,-5)  + 0.2*1.746 * math.pow(10, -5),
            0.8 * (-1.168) * math.pow(10, -8) + 0.2 * (-1.065) * math.pow(10, -8)), 0))
            #//Density: 1.977 kg/m3 (gas at 1 atm and 0 °C)
fluidpackage.append( component.component( molecule.molecule("CO2", "Carbon Dioxide", 0.018, 0.07 * 0.001, 1.977, 304.25, 7.39 * math.pow(10, 6), 0.228,
                19.8, 0.07344, -5.602E-05, 1.715E-08), 0))
                #//Density: 1.977 kg/m3 (gas at 1 atm and 0 °C)
fluidpackage.append( component.component( molecule.molecule("CO", "Carbon Monoxide", 0.02801, 0.0001662 * 0.001, 1.145), 0))
            #//Density: 1.145 kg/m3 at 25 °C, 1 atm
fluidpackage.append( component.component( molecule.molecule("H2", "Hydrogen", 0.0020158, 8.76 * math.pow(10, -6), 0.08988), 0))
            #//Density: 0.08988 g/L = 0.08988 kg/m3 (0 °C, 101.325 kPa)
fluidpackage.append( component.component( molecule.molecule("He", "Helium", HeMolarMass, 0, 0.1786, 5.1953, 5.1953E6, -0.390,
                20.8, 0, 0, 0), 0))
            #//essentially no viscosity.
fluidpackage.append( component.component( molecule.molecule("CH4", "Methane", 0.01604, 0.0001027 * 0.001, 0.6556), 0))
            #//Density: 0.6556 g L−1 = 0.6556 kg/m3
fluidpackage.append( component.component( molecule.molecule("CH4O", "Methanol", 0.03204, 5.9E-04, 791.8, 513, 80.9 * 100000, 0.556,
                21.15, 0.07092, 2.587E-05, -2.852E-08), 0))
            #//Density: 0.6556 g L−1 = 0.6556 kg/m3
fluidpackage.append( component.component( molecule.molecule("N", "Nitrogen", 0.028, 0.018 * 0.001, 1.251,126.192, 3.3958*math.pow(10,6), 0.04, 
                31.15, -0.01357, 2.68*math.pow(10,-5), -1.168*math.pow(10,-8)), 0))
            #//Density: 1.251 g/L = 1.251 kg/m3
fluidpackage.append( component.component( molecule.molecule("O2", "Oxygen", 0.016, 2.04 * math.pow(10, -5), 1.429, 154.581, 5.043 * math.pow(10, 6),
                0.022, 28.11, -3.7 * math.pow(10, -6), 1.746 * math.pow(10, -5), -1.065 * math.pow(10, -8)), 0))
fluidpackage.append( component.component( molecule.molecule("H2O", "Water", 0.0180153, WaterDensity, 1, 647.096, 22060000, 0.344,
                7.243e01, 1.039e-2, -1.497e-6, 0), 1.0))
            #//Density: 1000 kg/m3
            #//Dynamic viscosity for water at 20 Deg C
fluidpackage.append( component.component( molecule.molecule("C2H6", "Ethane", 0.03007, 0, 1.3562 * 100), 0)); #//Just assume no viscosity for the moment.
fluidpackage.append( component.component( molecule.molecule("C3H8", "Propane", 0.03007, 0, 1.3562 * 100, 369.8, 42.5 * 100000, 0.153,
                -4.224, 0.3063, -1.586e-04, 3.215e-08), 0)) #//Just assume no viscosity for the moment.
fluidpackage.append( component.component( molecule.molecule("C4H10", "Butane", 58.12 / 1000, 0, 2.48 * 100, 425.2, 38.0 * 100000, 0.199,
                9.487, 0.3313, -1.108e-04, -2.822e-09), 0)) #//Just assume no viscosity for the moment.
fluidpackage.append( component.component( molecule.molecule("C5H12", "Pentane", 72.15 / 1000, 240 / 1000000,
                0.626 * 1000), 0))
fluidpackage.append( component.component( molecule.molecule("C6H14", "2-Methylpentane", 86.18 / 1000, 0,
                653), 0))
fluidpackage.append( component.component( molecule.molecule("C7H16", "Heptane", 100.20 / 1000, 386 / 1000000,
                679.5), 0))
fluidpackage.append( component.component( molecule.molecule("C8H18", "Octane", 114.23 / 1000, 542 / 1000000,
                0.703 * 1000), 0))
fluidpackage.append( component.component( molecule.molecule("C9H20", "Nonane", 128.26 / 1000, 0.711 / 1000, 718), 0))
fluidpackage.append( component.component( molecule.molecule("C10H22", "Decane", 142.28 / 1000, 0.920 / 1000, 730, 617.8, 21.1 * 100000), 0))
fluidpackage.append( component.component( molecule.molecule("C11H24", "Undecane", 156.30826 / 1000, 0.920 / 1000, 740.2), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C12H26", "Dodecane", 170.33 / 1000, 1.35 / 1000, 780.8), 0))
fluidpackage.append( component.component( molecule.molecule("C13H28", "Tridecane", 184.36 / 1000, 0, 756), 0)) #/#/ Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C14H30", "Tetradecane", 198.39 / 1000, 2.18 / 1000, 756), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C15H32", "Pentadecane", 212.41 / 1000, 0, 769), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C16H34", "Hexadecane", 226.44 / 1000, 3.34 / 1000, 770), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C17H36", "Heptadecane", 240.47 / 1000, 0, 777), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C18H38", "Octadecane", 254.494 / 1000, 0, 777), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C19H40", "Nonadecane", 268.5209 / 1000, 0, 786), 0)) #// Just assume zero viscosity for now.fluidpackage.Add(new component(new molecule("C20H42", "Icosane", 282.55 / 1000, 0, 786), 0)); // Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C21H44", "Heneicosane", 296.6 / 1000, 0, 792), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C22H46", "Docosane", 310.61 / 1000, 0, 778), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C23H48", "Tricosane ", 324.63 / 1000, 0, 797), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C24H50", "Tetracosane", 338.66 / 1000, 0, 797), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C25H52", "Pentacosane", 352.69 / 1000, 0, 801), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C26H54", "Hexacosane", 366.71 / 1000, 0, 778), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component(  molecule.molecule("C27H56", "Heptacosane", 380.74 / 1000, 0, 780), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C28H58", "Octacosane", 394.77 / 1000, 0, 807), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C29H60", "Nonacosane", 408.80 / 1000, 0, 808), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C30H62", "Triacontane", 422.82 / 1000, 0, 810), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C31H64", "Hentriacontane", 436.85 / 1000, 0, 781), 0)) #/#/ Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C32H66", "Dotriacontane", 450.88 / 1000, 0, 812), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C33H68", "Tritriacontane", 464.90 / 1000, 0, 811), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C34H70", "Tetratriacontane ", 478.93 / 1000, 0, 812), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C35H72", "Pentatriacontane ", 492.96 / 1000, 0, 813), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C36H74", "Hexatriacontane", 506.98 / 1000, 0, 814), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C37H76", "Heptatriacontane", 520.99 / 1000, 0, 815), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C38H78", "Octatriacontane", 535.03 / 1000, 0, 816), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C39H80", "Nonatriacontane", 549.05 / 1000, 0, 817), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C40H82", "Tetracontane", 563.08 / 1000, 0, 817), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C41H84", "Hentetracontane", 577.11 / 1000, 0, 818), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C42H86", "Dotetracontane", 591.13 / 1000, 0, 819), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C43H88", "Triatetracontane", 605.15 / 1000, 0, 820), 0)) #// Just assume zero viscosity for now.
fluidpackage.append(  component.component(  molecule.molecule("C44H90", "Tetratetracontane", 619.18 / 1000, 0, 820), 0)) #// Just assume zero viscosity for now.fluidpackage.Add(  component(new molecule("C45H92", "Pentatetracontane", 633.21 / 1000, 0, 821), 0)); // Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C46H94", "Hexatetracontane", 647.23 / 1000, 0, 822), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C47H96", "Heptatetracontane", 661.26 / 1000, 0, 822), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C48H98", "Octatetracontane", 675.29 / 1000, 0, 823), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C49H100", "Nonatetracontane", 689.32 / 1000, 0, 823), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C50H102", "Pentacontane", 703.34 / 1000, 0, 824), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C51H104", "Henpentacontane", 717.37 / 1000, 0, 824), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C52H106", "Dopentacontane", 731.39 / 1000, 0, 825), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C53H108", "Tripentacontane", 745.42 / 1000, 0, 825), 0)) #// Just assume zero viscosity for now.
fluidpackage.append( component.component( molecule.molecule("C54H110", "Tetrapentacontane", 759.45 / 1000, 0, 826), 0)) # // Just assume zero viscosity for now.






