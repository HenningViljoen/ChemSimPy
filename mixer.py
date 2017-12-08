from unitop import unitop
from point import point
import globe as globe
import utilities as utilities
from mixerproperties import mixerproperties


class mixer(unitop):
    def __init__(self, anr, ax, ay, anin):
                    #public mixer(int anr, double ax, double ay, int anin)
                    #: base(anr, ax, ay, anin, 1)
        super(mixer, self).__init__(anr, ax, ay, anin, 1)
        self.initmixer()


    def mixercopyconstructor(self, baseclasscopyfrom):
        #: base(0, 0, 0, ((mixer)baseclasscopyfrom).nin, 1) //The correct nin will be configured in the unitop class
        self.initmixer()
        self.copyfrom(baseclasscopyfrom)


    def initmixer(self):
        self.objecttype = globe.objecttypes.Mixer
        self.name = 'Mixer ' + str(self.nr)
        self.mixerinitradius = globe.MixerInitRadiusDefault
        self.updateinoutpointlocations()


    def copyfrom(self, baseclasscopyfrom):
        mixercopyfrom = baseclasscopyfrom
        super(mixer, self).copyfrom(mixercopyfrom)
        mixerinitradius = mixercopyfrom.mixerinitradius
        self.nin = mixercopyfrom.nin


    def update(self, i, historise):
        self.outflow[0].massflow.v = 0.0
        self.outflow[0].actualvolumeflow.v = 0.0
        #//outflow[0].mat.P.v = 0;
        self.outflow[0].mat.T.v = 0.0
        self.outflow[0].mat.density.v = 0.0
        self.mat.copycompositiontothisobject(self.inflow[0].mat)

        for j in range(self.nin):
            self.outflow[0].massflow.v += self.inflow[j].massflow.v
        massflowtouse = [0.0]*self.nin #local var
        totalmassflowtouse = 0.0 #local var
        for j in range(self.nin):
            if self.outflow[0].massflow.v == 0:
                massflowtouse[j] = 1.0
            else:
                massflowtouse[j] = self.inflow[j].massflow.v
            #massflowtouse[j] = (outflow[0].massflow.v == 0) ? 1 : inflow[j].massflow.v
            totalmassflowtouse += massflowtouse[j]

        for j in range(self.nin):
            self.outflow[0].actualvolumeflow.v += self.inflow[j].actualvolumeflow.v
            #//outflow[0].mat.P.v += inflow[j].mat.P.v * massflowtouse[j];
            self.inflow[j].mat.P.v = self.outflow[0].mat.P.v
            self.outflow[0].mat.T.v += self.inflow[j].mat.T.v * massflowtouse[j]
            self.outflow[0].mat.density.v += self.inflow[j].mat.density.v * massflowtouse[j]

        #//outflow[0].mat.P.v /= totalmassflowtouse;
        self.outflow[0].mat.T.v /= totalmassflowtouse
        self.outflow[0].mat.density.v /= totalmassflowtouse


    def updateinoutpointlocations(self):
        #//Update in and out point locations;
        self.outpoint[0].x = self.location.x + globe.MixerLength / 2
        self.outpoint[0].y = self.location.y
        for i in range(self.nin):
            self.inpoint[i].x = self.location.x - globe.MixerLength / 2
            self.inpoint[i].y = self.location.y - (self.nin - 1) / 2.0 * globe.MixerDistanceBetweenBranches + \
                i * globe.MixerDistanceBetweenBranches
        super(mixer, self).updateinoutpointlocations()


    def setproperties(self, asim, aroot):  #public override void setproperties(root, simulation asim)
        diag = mixerproperties(self, asim, aroot)


    def mouseover(self, x, y):
        return (utilities.distance(x - self.location.x, y - self.location.y) <= self.mixerinitradius)


    def draw(self, canvas):
        self.updateinoutpointlocations()

        #GraphicsPath plot1
        #Pen plotPen
        #float width = 1

        #plot1 = new GraphicsPath()
        #plotPen = new Pen(Color.Black, width)

        point0 = point(globe.OriginX + int(globe.GScale*(self.outpoint[0].x)), 
                    globe.OriginY + int(globe.GScale*(self.outpoint[0].y - globe.MixerBranchThickness/2)))
        point1 = point(globe.OriginX + int(globe.GScale*(self.outpoint[0].x - globe.MixerLength/2)), 
                    globe.OriginY + int(globe.GScale*(self.outpoint[0].y - globe.MixerBranchThickness/2)))
        point2 = point(globe.OriginX + int(globe.GScale*(self.outpoint[0].x - globe.MixerLength/2)), 
                    globe.OriginY + int(globe.GScale*(self.outpoint[0].y + globe.MixerBranchThickness/2)))
        point3 = point(globe.OriginX + int(globe.GScale*(self.outpoint[0].x)),
                    globe.OriginY + int(globe.GScale*(self.outpoint[0].y + globe.MixerBranchThickness/2)))

        mainoutput = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y, point3.x, point3.y)

        #Point[] output = new Point[] 
        #    {new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[0].x)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(outpoint[0].y - global.MixerBranchThickness/2))), 
        #    new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[0].x - global.MixerLength/2)), 
        #            global.OriginY + Convert.ToInt32(global.GScale*(outpoint[0].y - global.MixerBranchThickness/2))), 
         #   new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[0].x - global.MixerLength/2)), 
         #           global.OriginY + Convert.ToInt32(global.GScale*(outpoint[0].y + global.MixerBranchThickness/2))), 
         #   new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[0].x)),
         #           global.OriginY + Convert.ToInt32(global.GScale*(outpoint[0].y + global.MixerBranchThickness/2)))}

        #plot1.AddPolygon(output)

        x0 = globe.OriginX + int(globe.GScale * (self.location.x - globe.MixerBranchThickness / 2))
        y0 = globe.OriginY + int(globe.GScale * (self.location.y - (self.nin - 1) / 2.0 * \
            globe.MixerDistanceBetweenBranches))
        x1 = x0 + int(globe.GScale * (globe.MixerBranchThickness))
        y1 = y0 + int(globe.GScale * ((self.nin - 1) * globe.MixerDistanceBetweenBranches))

        upright = canvas.create_rectangle(x0, y0, x1, y1)

        if self.highlighted:
            canvas.itemconfig(upright, fill='red')
        else:
            canvas.itemconfig(upright, fill='gray')

        #Rectangle upright = new Rectangle(
        #        global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.MixerBranchThickness / 2)),
        #        global.OriginY + Convert.ToInt32(global.GScale * (location.y - (nin - 1) / 2.0 * global.MixerDistanceBetweenBranches)),
        #        Convert.ToInt32(global.GScale * (global.MixerBranchThickness)),
        #        Convert.ToInt32(global.GScale * ((nin - 1) * global.MixerDistanceBetweenBranches)))
        #plot1.AddRectangle(upright);

        branches = list() #list of Rectangles
        #Rectangle[] branches = new Rectangle[nout]
        for i in range(self.nin):
            x0 = globe.OriginX + int(globe.GScale * (self.location.x - globe.MixerLength / 2))
            y0 = globe.OriginY + int(globe.GScale * (self.location.y - (self.nin - 1) / 2.0 * \
                globe.MixerDistanceBetweenBranches + i * globe.MixerDistanceBetweenBranches))
            x1 = x0 + int(globe.GScale * (globe.MixerLength / 2))
            y1 = y0 + int(globe.GScale * (globe.MixerBranchThickness))
            #branches[i] = new Rectangle(
            #        global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.TeeLength / 2)),
            #        global.OriginY + Convert.ToInt32(global.GScale * (location.y - (nout - 1) / 2.0 * global.TeeDistanceBetweenBranches +
            #        i * global.TeeDistanceBetweenBranches)),
            #        Convert.ToInt32(global.GScale * (global.TeeLength / 2)),
            #        Convert.ToInt32(global.GScale * (global.TeeBranchThickness)))
            rect = canvas.create_rectangle(x0, y0, x1, y1)
            branches.append(rect)

        #Rectangle[] branches = new Rectangle[nin]
        #for (int i = 0; i < nin; i++)
        #    branches[i] = new Rectangle(
         #           global.OriginX + Convert.ToInt32(global.GScale * (location.x - global.MixerLength / 2)),
         #           global.OriginY + Convert.ToInt32(global.GScale * (location.y - (nin - 1) / 2.0 * global.MixerDistanceBetweenBranches +
         #           i * global.MixerDistanceBetweenBranches)),
         #           Convert.ToInt32(global.GScale * (global.MixerLength / 2)),
         #           Convert.ToInt32(global.GScale * (global.MixerBranchThickness)))
         #   plot1.AddRectangle(branches[i])

        #plotPen.Color = Color.Black

        #SolidBrush brush = new SolidBrush(Color.Black)
        #if (highlighted) { brush.Color = Color.Orange; }
        #G.FillPath(brush, plot1)
        #G.DrawPath(plotPen, plot1)

        super(mixer, self).draw(canvas)


