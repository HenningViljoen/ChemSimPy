import globe as globe
from controlvar import controlvar
from point import point
from unitop import unitop
from tankproperties import tankproperties
import math


class tank(unitop):
    def __init__(self, anr, ax, ay, afracinventory = globe.TankInitFracInventory, \
        aradius = globe.TankInitRadius, aheight = globe.TankInitHeight):
                #public tank(int anr, double ax, double ay, double afracinventory, double aradius, double aheight)
                #: base(anr, ax, ay, 1, 1)
        super(tank, self).__init__(anr, ax, ay, 1, 1)
        self.inittank(afracinventory, aradius, aheight)
   

    def tankcopyconstructor(self, baseclasscopyfrom):
                #public tank(baseclass baseclasscopyfrom)
                #: base(baseclasscopyfrom.nr, baseclasscopyfrom.location.x, baseclasscopyfrom.location.y, 1, 1)
        self.inittank(globe.TankInitFracInventory, globe.TankRadiusDraw, globe.TankInitHeight)
        self.copyfrom(baseclasscopyfrom)


    def inittank(self, afracinventory, aradius, aheight):
                #public void inittank(double afracinventory, double aradius, double aheight)
        self.maxvolume = 0.0 # //m^3
        self.objecttype = globe.objecttypes.Tank
        self.name = 'Tank: ' + str(self.nr)
            
        self.massinventory = controlvar() #//kg
        self.actualvolumeinventory = controlvar() #//m3
        self.fracinventory = controlvar() #//fraction
        self.inventoryheight = controlvar() #//m
        self.pressureatbottom = controlvar() #//Pa

        #//G = aG
        self.radius = aradius
        self.height = aheight

        self.fracinventory.v = afracinventory
        self.calcmaxvolume()
        self.calcmassinventoryfromfracinventory()

        self.updateinoutpointlocations()
        self.update(0, False)

        self.controlpropthisclass = []
        self.controlpropthisclass += ["massinventory",
                                            "actualvolumeinventory",
                                            "fracinventory",
                                            "inventoryheight",
                                            "pressureatbottom"]
        self.nrcontrolpropinherited = len(self.controlproperties)
        self.controlproperties += self.controlpropthisclass


    def copyfrom(self, baseclasscopyfrom):
            #public override void copyfrom(baseclass baseclasscopyfrom)
        tankcopyfrom = baseclasscopyfrom
        super(tank, self).copyfrom(tankcopyfrom)
        #base.copyfrom(tankcopyfrom)

        self.maxvolume = tankcopyfrom.maxvolume #//m^3
        self.radius = tankcopyfrom.radius
        self.height = tankcopyfrom.height
        self.massinventory.copyfrom(tankcopyfrom.massinventory) #//kg
        self.actualvolumeinventory.copyfrom(tankcopyfrom.actualvolumeinventory) #//m3
        self.fracinventory.copyfrom(tankcopyfrom.fracinventory) #//fraction
        self.inventoryheight.copyfrom(tankcopyfrom.inventoryheight) #//m
        self.pressureatbottom.copyfrom(tankcopyfrom.pressureatbottom) #//Pa


    def selectedproperty(self, selection):
            #public override controlvar selectedproperty(int selection)
        if (selection >= self.nrcontrolpropinherited):
            diff = selection - self.nrcontrolpropinherited
            if diff == 0:
                return self.massinventory
            elif diff == 1:
                return self.actualvolumeinventory
            elif diff == 2:
                return self.fracinventory
            elif diff == 3:
                return self.inventoryheight
            elif diff == 4:
                return self.pressureatbottom
            else:
                return None
        else:
            return super(tank, self).selectedproperty(selection)


    def calcmassinventoryfromfracinventory(self):
        self.actualvolumeinventory = self.fracinventory * self.maxvolume
        self.massinventory = self.actualvolumeinventory * self.mat.density


    def calcmaxvolume(self):
        self.maxvolume = math.pi * math.pow(self.radius, 2) * self.height


    def inventorycalcs(self):
        self.calcmaxvolume()
        self.actualvolumeinventory = self.massinventory / self.mat.density
        self.fracinventory.v = self.actualvolumeinventory.v / (self.maxvolume + globe.Epsilon)
        self.inventoryheight = self.actualvolumeinventory / (math.pi * math.pow(self.radius, 2))


    def update(self, simi, historise): #public override void update(int simi, bool historise)
        if (self.inflow[0] != None):
            self.mat.T.v = (self.massinventory.v * self.mat.T.v + \
                self.inflow[0].massflow.v * globe.SampleT * self.inflow[0].mat.T.v) /  \
                (self.massinventory.v + self.inflow[0].massflow.v * globe.SampleT)
            self.massinventory += self.inflow[0].massflow * globe.SampleT

        if (self.outflow[0] != None):
            self.massinventory += -self.outflow[0].massflow * globe.SampleT

        self.inventorycalcs()
        self.pressureatbottom.v = self.mat.density.v * globe.g * self.height*self.fracinventory.v + globe.Ps

        if (self.outflow[0] != None):
            self.outflow[0].mat.P.v = self.pressureatbottom.v
            self.outflow[0].mat.T.v = self.mat.T.v
            
        if (self.fracinventory.v < globe.TankMinFracInventory):
            if (self.outflow[0] != None):
                self.outflow[0].hasmaterial = False
        elif (self.outflow[0] != None):
            self.outflow[0].hasmaterial = True

        if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
            index = int(simi / globe.SimVectorUpdatePeriod)
            if (self.fracinventory.simvector != None):
                self.fracinventory.simvector[index] = self.fracinventory.v
            if (self.pressureatbottom.simvector != None):
                self.pressureatbottom.simvector[index] = self.pressureatbottom.v 


    def showtrenddetail(self):
        if not self.detailtrended:
            self.detailtrended = True
            self.allocatememory()
        else:
            self.detailtrended = False
            self.deallocatememory()


    def allocatememory(self):
        if (self.fracinventory.simvector == None):
            self.fracinventory.simvector = [0.0]*globe.SimVectorLength
        if (self.mat.T.simvector == None):
            self.mat.T.simvector = [0.0]*globe.SimVectorLength
        if (self.pressureatbottom.simvector == None):
            self.pressureatbottom.simvector = [0.0]*globe.SimVectorLength


    def deallocatememory(self):
        self.fracinventory.simvector = None
        self.mat.T.simvector = None
        self.pressureatbottom.simvector = None


    def dodetailtrend(self, plt):
        if self.detailtrended:
            x = globe.SimTimeVector
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.fracinventory.simvector)
            axarr[0].set_title('Fraction inventory (kg/s) : ' + self.name)
            axarr[1].plot(x, self.mat.T.simvector)
            axarr[1].set_title('Temperature (K) : ' + self.name)
            axarr[2].plot(x, self.pressureatbottom.simvector)
            axarr[2].set_title('Pressure at the bottom (Pa) : ' + self.name)


    def mouseover(self, x, y):  #public override bool mouseover(double x, double y)
        return (x >= (self.location.x - globe.TankRadiusDraw) and x <= (self.location.x + globe.TankRadiusDraw) and \
            y >= (self.location.y - 0.5 * globe.TankHeightDraw) and y <= (self.location.y + 0.5 * globe.TankHeightDraw))


    def updateinoutpointlocations(self):
        #//Update in and out point locations
        self.inpoint[0].x = self.location.x - globe.TankRadiusDraw - globe.InOutPointWidth
        self.inpoint[0].y = self.location.y - globe.TankInitInOutletDistanceFraction / 2 * globe.TankHeightDraw
        self.outpoint[0].x = self.location.x + globe.TankRadiusDraw + globe.InOutPointWidth
        self.outpoint[0].y = self.location.y + globe.TankInitInOutletDistanceFraction / 2 * globe.TankHeightDraw


    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        diag = tankproperties(self, asim, aroot)


    def draw(self, canvas): #//public virtual void draw(Graphics G)
        self.updateinoutpointlocations()

        #//Draw main tank
        #GraphicsPath tankmain
        #Pen plotPen
        #float width = 1

        #tankmain = new GraphicsPath()
        #plotPen = new Pen(Color.Black, width)

        point0 = point(globe.OriginX + int(globe.GScale*(self.location.x - globe.TankRadiusDraw)), 
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.TankHeightDraw)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.location.x - globe.TankRadiusDraw)), 
                   globe.OriginY + int(globe.GScale*(self.location.y - 0.5*globe.TankHeightDraw)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.location.x + globe.TankRadiusDraw)), 
                globe.OriginY + int(globe.GScale*(self.location.y - 0.5*globe.TankHeightDraw)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.location.x + globe.TankRadiusDraw)),
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.TankHeightDraw)))
        
        polygon = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)

        #Point[] myArray = new Point[] 
        #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - global.TankRadiusDraw)), 
        #        global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.TankHeightDraw))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - global.TankRadiusDraw)), 
        #           global.OriginY + Convert.ToInt32(global.GScale*(location.y - 0.5*global.TankHeightDraw))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + global.TankRadiusDraw)), 
         #       global.OriginY + Convert.ToInt32(global.GScale*(location.y - 0.5*global.TankHeightDraw))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + global.TankRadiusDraw)),
         #       global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.TankHeightDraw)))}
        #tankmain.AddPolygon(myArray)

        if (self.highlighted == True):
            canvas.itemconfig(polygon, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(polygon, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(polygon, fill='grey')

        #plotPen.Color = Color.Black
        #SolidBrush brush = new SolidBrush(Color.White)
        #brush.Color = (highlighted) ? Color.Orange : Color.White
        #G.FillPath(brush, tankmain)
        #G.DrawPath(plotPen, tankmain)

        #//Draw level in the tank (might later be changed for an embedded trend)
        #GraphicsPath tanklevel

        #tanklevel = new GraphicsPath()

        levelpoint0 = point(globe.OriginX + int(globe.GScale*(self.location.x - globe.TankRadiusDraw)),
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.TankHeightDraw)))
        levelpoint1 = point(globe.OriginX + int(globe.GScale*(self.location.x - globe.TankRadiusDraw)),
                   globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.TankHeightDraw -
                   self.fracinventory.v*globe.TankHeightDraw)))
        levelpoint2 = point(globe.OriginX + int(globe.GScale*(self.location.x + globe.TankRadiusDraw)),
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.TankHeightDraw -
                self.fracinventory.v*globe.TankHeightDraw)))
        levelpoint3 = point(globe.OriginX + int(globe.GScale*(self.location.x + globe.TankRadiusDraw)),
                globe.OriginY + int(globe.GScale*(self.location.y + 0.5*globe.TankHeightDraw)))
        
        tanklevel = canvas.create_polygon(levelpoint0.x, levelpoint0.y, levelpoint1.x, levelpoint1.y,
            levelpoint2.x, levelpoint2.y, levelpoint3.x, levelpoint3.y)

        #Point[] tanklevelarray = new Point[] 
        #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - global.TankRadiusDraw)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.TankHeightDraw))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x - global.TankRadiusDraw)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.TankHeightDraw - fracinventory.v*global.TankHeightDraw))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + global.TankRadiusDraw)), 
         #           global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.TankHeightDraw - fracinventory.v*global.TankHeightDraw))), 
        #new Point(global.OriginX + Convert.ToInt32(global.GScale*(location.x + global.TankRadiusDraw)),
        #            global.OriginY + Convert.ToInt32(global.GScale*(location.y + 0.5*global.TankHeightDraw)))}
        #tanklevel.AddPolygon(tanklevelarray)
        #plotPen.Color = Color.Black
        #brush.Color = (highlighted) ? Color.Blue : Color.Green
        #G.FillPath(brush, tanklevel)
        #G.DrawPath(plotPen, tanklevel)

        if (self.highlighted == True):
            canvas.itemconfig(tanklevel, fill='red')
        elif self.detailtrended:
            canvas.itemconfig(tanklevel, fill=globe.DetailTrendHighlightColour)
        else:
            canvas.itemconfig(tanklevel, fill='sky blue')

        #//Draw inpoint
        super(tank, self).draw(canvas)


