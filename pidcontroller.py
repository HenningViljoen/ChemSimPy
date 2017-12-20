from controlvar import controlvar
import globe as globe
import utilities as utilities
from baseclass import baseclass
from pidcontrollerproperties import pidcontrollerproperties


class pidcontroller(baseclass):
    def __init__(self, anr=0, ax=0.0, ay=0.0, aK=0.0, aI=0.0, aD=0.0, asp=0.0, aminpv=0.0, amaxpv=0.0, 
            aminop=0.0, amaxop=0.0):
        super(pidcontroller, self).__init__(anr, ax, ay)
        self.pidcontrollerinit(aK, aI, aD, asp, aminpv, amaxpv, aminop, amaxop)


    def pidcontrollercopycontructor(self, pidcontrollercopyfrom):
        self.pidcontrollerinit(pidcontrollercopyfrom.K, pidcontrollercopyfrom.I, pidcontrollercopyfrom.D, \
            pidcontrollercopyfrom.sp, pidcontrollercopyfrom.minpv, pidcontrollercopyfrom.maxpv, \
            pidcontrollercopyfrom.minop, pidcontrollercopyfrom.maxop)
        self.copyfrom(pidcontrollercopyfrom)


    def pidcontrollerinit(self, aK, aI, aD, asp, aminpv, amaxpv, aminop, amaxop):
        self.objecttype = globe.objecttypes.PIDController

        self.name = 'PID Controller: ' + str(self.nr)

        self.K = aK
        self.I = aI
        self.D = aD
        self.pvspan = 0.0 #Engineering Unit range over which the PV, Set point, will vary;
        self.opspan = 0.0 #Engineering Unit range over which the OP will vary.
        self.integral = 0.0
        self.dointegral = True #If in wind-up, will go to false.
        self.bias = 0.0
        self.sp = asp

        self.pv = controlvar()
        self.op = controlvar()

        self.err = 0.0
        self.directionenum = globe.piddirection.Direct # As controldirection.  for now this will be the value.
        self.direction = -1
        self.calcdirection() #init the direction variable correctly based on the direction enum.
        self.maxpv = amaxpv
        self.minpv = aminpv
        self.maxop = amaxop
        self.minop = aminop

        self.pvname = ''
        self.opname = ''

        self.highlighted = False
        self.calcspan()


    def copyfrom(self, baseclasscopyfrom):
        pidcontrollercopyfrom = baseclasscopyfrom

        super(pidcontroller, self).copyfrom(pidcontrollercopyfrom)

        self.K = pidcontrollercopyfrom.K
        self.I = pidcontrollercopyfrom.I
        self.D = pidcontrollercopyfrom.D
        self.bias = pidcontrollercopyfrom.bias
        self.pvspan = pidcontrollercopyfrom.pvspan #Engineering Unit range over which the PV, Set point, will vary
        self.opspan = pidcontrollercopyfrom.opspan #Engineering Unit range over which the OP will vary.
        self.integral = pidcontrollercopyfrom.integral
        self.dointegral = pidcontrollercopyfrom.dointegral #If in wind-up, will go to false.
        self.sp = pidcontrollercopyfrom.sp
        self.err = pidcontrollercopyfrom.err
        self.pv.copyfrom(pidcontrollercopyfrom.pv)
        self.op.copyfrom(pidcontrollercopyfrom.op)
        self.direction = pidcontrollercopyfrom.direction # As controldirection
        self.maxpv = pidcontrollercopyfrom.maxpv
        self.minpv = pidcontrollercopyfrom.minpv
        self.maxop = pidcontrollercopyfrom.maxop
        self.minop = pidcontrollercopyfrom.minop
        self.pvname = pidcontrollercopyfrom.pvname
        self.opname = pidcontrollercopyfrom.opname


    def calcspan(self):
        self.pvspan = self.maxpv - self.minpv
        self.opspan = self.maxop - self.minop

    
    def calcdirection(self):
        if self.directionenum == globe.piddirection.Direct:
            self.direction = -1
        elif self.directionenum == globe.piddirection.Reverse:
            self.direction = 1


    def calcerr(self):
        self.err = self.direction * (self.sp - self.pv.v) / self.pvspan


    def calcintegral(self):
        if (self.dointegral):
            self.integral += self.err * globe.SampleT


    def calcop(self):
        self.op.v = self.K * (self.err + 1 / self.I * self.integral)*self.opspan + self.bias
        if (self.op.v > self.maxop):
            self.op.v = self.maxop
            self.dointegral = False
        elif (self.op.v < self.minop):
            self.op.v = self.minop
            self.dointegral = False
        else:
            self.dointegral = True


    def init(self):
        self.calcspan()
        self.bias = 0.0

        self.calcerr()
        oldop = self.op.v #local double
        self.calcop()
        self.bias = oldop - self.op.v


    def update(self, simi, historise):
        self.calcerr()
        self.calcintegral()
        self.calcop()
    

    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        diag = pidcontrollerproperties(self, asim, aroot)

    def mouseover(self, x, y):
        return (utilities.distance(x - self.location.x, y - self.location.y) <= globe.PIDControllerInitRadius)


    def draw(self, canvas):
        #//updateinoutpointlocations();

        #GraphicsPath plot1;
        #Pen plotPen;
        #float width = 1;

        #plot1 = new GraphicsPath();
        #plotPen = new Pen(Color.Black, width);

        x0 = globe.OriginX + int(globe.GScale * (self.location.x - globe.PIDControllerInitRadius))
        y0 = globe.OriginY + int(globe.GScale * (self.location.y - globe.PIDControllerInitRadius))
        x1 = x0 + int(globe.GScale * (globe.PIDControllerInitRadius * 2))
        y1 = y0 + int(globe.GScale * (globe.PIDControllerInitRadius * 2))

        circle = canvas.create_oval(x0, y0, x1, y1)

        if self.highlighted:
            canvas.itemconfig(circle, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(circle, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(circle, fill='gray')

        #plot1.AddEllipse(global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.PIDControllerInitRadius)),
        #                    global.OriginY + Convert.ToInt32(global.GScale * (location.y - global.PIDControllerInitRadius)),
         #                   Convert.ToInt32(global.GScale * (global.PIDControllerInitRadius * 2)),
         #                   Convert.ToInt32(global.GScale * (global.PIDControllerInitRadius * 2)));

        #plotPen.Color = Color.Black;

        #SolidBrush brush = new SolidBrush(Color.White);
        #if (highlighted) { brush.Color = Color.Orange; }
        #G.FillPath(brush, plot1);
        #G.DrawPath(plotPen, plot1);

        super(pidcontroller, self).draw(canvas)

