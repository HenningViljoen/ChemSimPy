import globe as globe
import utilities as utilities
import baseclass as baseclass
import controlvar as controlvar
import material as material

class baseprocessclass(baseclass.baseclass):

    def __init__(self, anr, ax, ay):
        super(baseprocessclass, self).__init__(anr, ax, ay)

        self.actualvolumeflow = controlvar.controlvar()  #controlvar; /m3/s  non-standard conditions.
        self.standardvolumeflow = controlvar.controlvar() # controlvar //m3/s  standard conditions (later to be descriminated between gases and liquids)
        self.molarflow = controlvar.controlvar()  #controlvar //molar flow per second
        self.massflow = controlvar.controlvar()  #controlvar  //kg/second
        self.hasmaterial = True #Bool.  //True if the stream/unitop/baseclass has material inside that can flow/pump or be processed.

        #//mat = new material(global.baseprocessclassInitVolume);
        #//public material(string componentname, double aTemp, double aV, double aP, double af) //second constructor
        self.mat = material.material()
        self.mat.materialconstructor2(globe.fluidpackage, globe.baseprocessclassInitTemperature, \
            globe.baseprocessclassInitVolume, \
            globe.baseprocessclassInitPressure, 0)  #material object
        self.massflow.v = globe.baseprocessclassInitMassFlow
            
        self.calcactualvolumeflowfrommassflow()
        self.calcmolarflowfrommassflow()
        self.calcstandardflowfrommoleflow()

        #//pressuresimvector = new double[global.SimIterations];

        self.controlpropthisclass = []
        self.controlpropthisclass = ["pressure", \
                                     "volume",  \
                                     "density", \
                                    "temperature", \
                                    "mass", \
                                    "n", \
                                    "actualvolumeflow", \
                                    "standardvolumeflow", \
                                    "massflow", \
                                    "molarflow"]
        self.controlproperties = self.controlproperties + self.controlpropthisclass


    def copyfrom(self, baseclasscopyfrom): #public override void copyfrom(baseclass baseclasscopyfrom)
        baseprocessclasscopyfrom =  baseclasscopyfrom #local var
        #baseprocessclass baseprocessclasscopyfrom = (baseprocessclass)baseclasscopyfrom;

        super(baseprocessclass, self).copyfrom(baseclasscopyfrom)
        #base.copyfrom(baseprocessclasscopyfrom);

        self.hasmaterial = baseprocessclasscopyfrom.hasmaterial
            #//True if the stream/unitop/baseclass has material inside that can flow/pump or be processed.

        self.mat.copyfrom(baseprocessclasscopyfrom.mat)

        self.actualvolumeflow.v = baseprocessclasscopyfrom.actualvolumeflow.v #//m3/s  non-standard conditions.
        self.standardvolumeflow.v = baseprocessclasscopyfrom.standardvolumeflow.v #//m3/s  standard conditions (later to be descriminated between gases and liquids)
        self.massflow.copyfrom(baseprocessclasscopyfrom.massflow) #//kg/second  //At this stage we use copyfrom for this one as we need to copy the excel
                                                              #//source in particular as well for the mass flow.
        self.molarflow.v = baseprocessclasscopyfrom.molarflow.v #//molar flow per second


    def selectedproperty(self, selection):
            #public override controlvar selectedproperty(int selection)
        if selection == 0:
                return self.mat.P
        elif selection == 1:
                return self.mat.V
        elif selection == 2:
                return self.mat.density
        elif selection == 3:
                return self.mat.T
        elif selection == 4:
                return self.mat.mass
        elif selection == 5:
                return self.mat.n
        elif selection == 6:
                return self.actualvolumeflow
        elif selection == 7:
                    return self.standardvolumeflow
        elif selection == 8:
                return self.massflow
        elif selection == 9:
                return self.molarflow
        else:
                return self.null




    #//public void calcmassflowfromactualvolflow()
    #//{
    #//    massflow = actualvolumeflow * density;
    #//}

    def calcactualvolumeflowfrommassflow(self):
        self.actualvolumeflow.v = self.massflow.v / (self.mat.density.v + 0.001)


    def calcstandardflowfrommoleflow(self):
        self.standardvolumeflow.v = utilities.dndt2fps(self.molarflow.v)


    def calcmolarflowfrommassflow(self):
        self.molarflow.v = 0
        self.molarflow.v = self.massflow.v / (self.mat.massofonemole + 0.001)


    #//public void calcmassflowfromstandardflow()
    #//{
    #//    molarflow = utilities.fps2dndt(standardvolumeflow);
    #//    massflow = molarflow * mat.massofonemole;
    #//} 

    def calcmassflowfrommolarflow(self):
        self.massflow.v = 0
        for i in range(len(self.mat.composition)):
            self.massflow.v += self.mat.composition[i].n / self.mat.n.v * self.molarflow.v *  \
                    self.mat.composition[i].m.molarmass


    def update(self, i, historise):   #public virtual void update(int i, bool historise) 
            #//index for where in the simvectors the update is to be stored.
        self.mat.update(i, historise)


    #//public virtual void updatepoint(int i, double x, double y)
    #//{
    #//}

    #//public virtual bool mouseover(double x, double y) //This function will indicate whether the mouse is over a particular unitop or stream at any moment in time.
    #//{
    #//    return false;
    #//}

    #//public virtual void setproperties(simulation asim) //Method that will be inherited and that will set the properties of the applicable object in a window
    #//{

    #//}

    #//public virtual void draw(Graphics G)
    #//{
    #//}

