from controlvar import controlvar
import globe as globe


class mpcvar:
    def __init__(self, avar, aname, atarget, aweight, amin = 0, amax = 0):
       #public mpcvar(controlvar avar, string aname, double atarget, double aweight, double amin = 0, double amax = 0)
        self.var = avar #controlvar
        self.name = aname #string
        self.target = controlvar(atarget) #//This will be the target in the objective function of the NMPC/MPC controller that will use this variable.
                                #The target will be a control var, since it might be a signal that changes (moving target), which might come from the 
                                #historian, or from a data file.
        self.weight = aweight #double. This will be the weight in the objective function for the NMPC/MPC controller 
                                #that will use this variable.
        self.min = amin #double. Each MV and CV will have a high and low limit.  This will be taken into account in the NMPC 
                                #algorithm as constraints.
        self.max = amax #double.


    def mpcvarcopyconstructor(self, mpcvarcopyfrom):  #public mpcvar(mpcvar mpcvarcopyfrom) 
        self.var = controlvar()
        self.var.copyfrom(mpcvarcopyfrom.var)
        self.copyfrom(mpcvarcopyfrom)


    def copyfrom(self, mpcvarcopyfrom):
        self.var = controlvar()
        self.var.copyfrom(mpcvarcopyfrom.var)
        self.name = mpcvarcopyfrom.name
        self.target = mpcvarcopyfrom.target
        self.weight = mpcvarcopyfrom.weight
        self.min = mpcvarcopyfrom.min
        self.max = mpcvarcopyfrom.max


    def fracofrange(self): #returns the fraction of range of the Engineering Unit MV or CV
        return (self.var.v - self.min) / (self.max - self.min + globe.Epsilon)


    def rangetoeu(self, frac): #public double rangetoeu(double frac)
                        #converts a fraction value for the variable to its Engineering Unit form.
        return frac * (self.max - self.min) + self.min


