

class component(object):
    def __init__(self, am = None, amolefraction = 0.0, an = 0.0):
        self.molefraction = amolefraction
        self.n = an #Amount of moles of this molecule/compound that is in this material.
        self.m = am #molecule object
        #//massfraction = amassfraction;  #mass fraction of this component of the material in a particular unitop or stream.
        #//public double molefraction;  /fraction of total moles in the material that is from this component.

    def copytothisobject(self, c): #c is a component object
        self.m = c.m; #Do not make a copy of the c.m object, just point to the address of c.m, since c.m should never change between unit ops - it is part
        # of the fluid package.
        self.molefraction = c.molefraction
        self.n = c.n
        #self.massfraction = c.massfraction
        #molefraction = c.molefraction;

