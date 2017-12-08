import globe as globe

class controlvar(object):
    def __init__(self, av = 0, aisbool = False):
        self.v = av;  #//The variable in this object that will have the PV or OP to be controlled in the simulation. 
        self.isbool = aisbool  #Is this a boolean variable?  Could then be part of a hybrid system.
        self.simvector = None #list() - will be a list of when it is initialised.
        #//simvector = new double[global.SimIterations];
        self.excelsource = None #for the case that data will be drawn in from an Excel file.  exceldataset object
        self.datasource = globe.datasourceforvar.Simulation  #The source of data for the variable in the model.
        
    @staticmethod
    def controlvarcopyconstructor(self, copyfrom):  #This is the copy constructor implemented as a static method
        newobj = controlvar(copyfrom.v)
        newobj.excelsource = copyfrom.excelsource
        newobj.datasource = copyfrom.datasource
        return newobj


    def copyfrom(self, copyfrom):
        self.v = copyfrom.v
        self.excelsource = copyfrom.excelsource
        self.datasource = copyfrom.datasource


    def ToString(self, format):
        return str(self.v)


    def ToString(self):
        return str(v)

    def __sub__(self, other): #self is on the left of -
        if isinstance(other,float):
            v = self.v - other
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = self.v - other.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'

    def __rsub__(self, other): #self is on the right of -
        if isinstance(other,float):
            v = other - self.v
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = other.v - self.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'


    def __neg__(self):
        return controlvar(-self.v)


    def __lt__(self, other):
        return self.v < other  #assume other is float.


    def __gt__(self, other):
        return self.v > other  #assume other is float.


    def __truediv__(self, other): #self is on the left of /
        if isinstance(other,float):
            v = self.v/other
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = self.v/other.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'


    def __rtruediv__(self, other):  #self is on the right of /
        if isinstance(other,float):
            v = other/self.v
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = other.v/self.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'


    def __mul__(self, other):
        if isinstance(other,float):
            v = self.v*other
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = self.v*other.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'


    def __rmul__(self, other): #self is on the right of *
        if isinstance(other,float):
            v = other*self.v
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = other.v*self.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'


    def __add__(self, other):
        if isinstance(other,float):
            v = self.v + other
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = self.v + other.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'


    def __pow__(self, other):
        if isinstance(other,float):
            v = self.v**other
            return controlvar(v)
        elif isinstance(other,controlvar):
            v = self.v**other.v
            return controlvar(v)
        else:
            print('Not implemented')
            return 'Not implemented'



