

class molecule(object):
    def __init__(self, anabreviation, aname, amolarmass, adynamicviscosity, \
        adensity, aTc = 500, aPc = 50*100000, \
            aomega = 0.3, aCpA = -4.224, aCpB = 0.3063, \
            aCpC = -1.586e-04, aCpD = 3.215e-08):
        #//Propane is the default Cp coefficients that have been inserted here.  
        # The Cp arguments here are heat capacity coefficients for the molecule.

        self.abreviation = anabreviation #string
        self.name = aname #string
        self.molarmass = amolarmass #//kg / mole
        self.dynamicviscosity = adynamicviscosity #//Pa·s  We need the dynamic viscosity here since it is used to 
                    #calculate the Renoulds number in liquid flow applications.  Later temperature dependance 
                    # will be added.  Standard conditions for now.
        self.density = adensity; #//kg/m3.  Also used in Re nr calc.  Later temp dependance will be added.  
                                #Standard conditions for now.  public double defaultmolefraction; 
                                # fraction of this molecule that is the default fraction for each stream.
        self.Tc = aTc #Kelvin; Critical temperature.
        self.Pc = aPc #Pascal; Critical pressure.
        self.omega = aomega #unitless; Acentric factor.
        self.CpA = aCpA; #//coeficient in equation to calculate Cp is a function of T
        self.CpB = aCpB; #//coeficient in equation to calculate Cp is a function of T
        self.CpC = aCpC; #//coeficient in equation to calculate Cp is a function of T
        self.CpD = aCpD; #//coeficient in equation to calculate Cp is a function of T


    def calcCp(self, T): #given the Temperature, calculate the Cp for the molecule.
        return self.CpA + self.CpB * T + self.CpC * T**2.0 + self.CpD * T**3.0
