import baseprocessclass as baseprocessclass
import globe as globe
import point as point
import utilities as utilities
import math
from streamproperties import streamproperties

class stream(baseprocessclass.baseprocessclass):
        
    def __init__(self, anr, p0x, p0y, p1x, p1y):
         #: base(anr, (p0x + p1x) / 2, (p0y + p1y) / 2)
            #public stream(int anr, double p0x, double p0y, double p1x, double p1y)
            #: base(anr, (p0x + p1x) / 2, (p0y + p1y) / 2)
        super(stream, self).__init__(anr, (p0x + p1x) / 2, (p0y + p1y) / 2)
        self.direction = 0.0 #public double   //radians
        self.distance = 0.0 # public double  //m
        self.inbetweenpoints = list() # public List<point>   //points that are between the main in and out points, that will enable straight lines for the stream.
        self.displaypoints = list() # public point[]  //The locations of the T, P and flow properties that are being displayed for the stream.
        
        self.streaminit(p0x, p0y, p1x, p1y)


    def streamcopyconstructor(self, streamcopyfrom):  #public stream(stream streamcopyfrom)
        #: base(streamcopyfrom.nr, (streamcopyfrom.points[0].x + streamcopyfrom.points[1].x) / 2,
        #    (streamcopyfrom.points[0].y + streamcopyfrom.points[1].y) / 2)
        self.streaminit(streamcopyfrom.points[0].x, streamcopyfrom.points[0].y, streamcopyfrom.points[1].x, \
                streamcopyfrom.points[1].y)
        self.copyfrom(streamcopyfrom)


    def streaminit(self, p0x, p0y, p1x, p1y):
            #private void streaminit(double p0x, double p0y, double p1x, double p1y)
        self.objecttype = globe.objecttypes.Stream
        self.name = str(self.nr) + " " + str(self.objecttype)

        self.points = [point.point]*2
        self.points[0] = point.point(p0x, p0y)
        self.points[1] = point.point(p1x, p1y)

        self.updatedirection()
        self.inbetweenpoints = list() #new List<point>(0)
        self.displaypoints = [point.point]*globe.StreamNrPropDisplay
        for i in range(globe.StreamNrPropDisplay):
            self.displaypoints[i] = point.point(0, 0)
        self.update(0, False)


    def copyfrom(self, baseclasscopyfrom):  #public override void copyfrom(baseclass baseclasscopyfrom)
        streamcopyfrom = baseclasscopyfrom
        #stream streamcopyfrom = (stream)baseclasscopyfrom

        super(stream, self).copyfrom(streamcopyfrom)
        #base.copyfrom(streamcopyfrom)

        self.direction = streamcopyfrom.direction #//radians
        self.distance = streamcopyfrom.distance #//m


    def updatedirection(self):
        self.direction = utilities.calcdirection(self.points[1].y - self.points[0].y, self.points[1].x - self.points[0].x)
        self.distance = utilities.distance(self.points[0], self.points[1])


    def updatemassflowsource(self, afilename):  #string afilename
        pass


    def updatepoint(self, i, x, y):
        #public override void updatepoint(int i, double x, double y)
        self.points[i].x = x
        self.points[i].y = y
        self.updatedirection()


    def update(self, simi, historise):
        #public override void update(int simi, bool historise)
        if (simi > 0):
            #// the reference flow is the mass flow
            self.calcactualvolumeflowfrommassflow()
            self.calcmolarflowfrommassflow()
            self.calcstandardflowfrommoleflow() #//should run after calcdndt since molar flow to be calculated first.
            if (self.massflow.datasource == globe.datasourceforvar.Exceldata):
                if (simi >= self.massflow.excelsource.data.Length): i = self.massflow.excelsource.data.Length - 1
                else: i = simi
                self.massflow.v = self.massflow.excelsource.data[i]
            if (self.mat.T.datasource == globe.datasourceforvar.Exceldata): #//This part should actually move to material.update().
                if (simi >= self.mat.T.excelsource.data.Length): i = self.mat.T.excelsource.data.Length - 1
                else: i = simi
                self.mat.T.v = self.mat.T.excelsource.data[i]
            if (self.mat.relativehumidity.datasource == globe.datasourceforvar.Exceldata): # //This part should actually move to material.update().
                if (simi >= self.mat.relativehumidity.excelsource.data.Length):
                    i = self.mat.relativehumidity.excelsource.data.Length - 1
                else: i = simi
                self.mat.relativehumidity.v = self.mat.relativehumidity.excelsource.data[i]

        if (historise and (simi % globe.SimVectorUpdatePeriod == 0)):
            index = int(simi/globe.SimVectorUpdatePeriod)
            if (self.actualvolumeflow.simvector != None):
                self.actualvolumeflow.simvector[index] = self.actualvolumeflow.v
            if (self.standardvolumeflow.simvector != None):
                self.standardvolumeflow.simvector[index] = self.standardvolumeflow.v
            if (self.massflow.simvector != None):
                self.massflow.simvector[index] = self.massflow.v
            if (self.molarflow.simvector != None):
                self.molarflow.simvector[index] = self.molarflow.v
            #//pressuresimvector[simi] = mat.P.v;
        super(stream, self).update(simi, historise)
        #base.update(simi, historise)


    def showtrenddetail(self):
        if not self.detailtrended:
            self.detailtrended = True
            self.allocatememory()
        else:
            self.detailtrended = False
            self.deallocatememory()


    def allocatememory(self):
        if (self.mat.T.simvector == None):
            self.mat.T.simvector = [0.0]*globe.SimVectorLength
        if (self.mat.P.simvector == None):
            self.mat.P.simvector = [0.0]*globe.SimVectorLength
        if (self.actualvolumeflow.simvector == None):
            self.actualvolumeflow.simvector = [0.0]*globe.SimVectorLength
        if (self.standardvolumeflow.simvector == None):
            self.standardvolumeflow.simvector = [0.0]*globe.SimVectorLength
        if (self.massflow.simvector == None):
            self.massflow.simvector = [0.0]*globe.SimVectorLength
        if (self.molarflow.simvector == None):
            self.molarflow.simvector = [0.0]*globe.SimVectorLength


    def deallocatememory(self):
        self.mat.T.simvector = None
        self.mat.P.simvector = None
        self.actualvolumeflow.simvector = None
        self.standardvolumeflow.simvector = None
        self.massflow.simvector = None
        self.molarflow.simvector = None


    def dodetailtrend(self, plt):
        if self.detailtrended:
            x = globe.SimTimeVector
            f, axarr = plt.subplots(3, sharex=True)
            axarr[0].plot(x, self.massflow.simvector)
            axarr[0].set_title('Mass flow (kg/s) : ' + self.name)
            axarr[1].plot(x, self.mat.P.simvector)
            axarr[1].set_title('Pressure (Pa) : ' + self.name)
            axarr[2].plot(x, self.mat.T.simvector)
            axarr[2].set_title('Temperature (K) : ' + self.name)


    def mouseover(self, x, y): #public override bool mouseover(double x, double y)
        streamover = False #default bool local var
        pixelstoclosestpoint = 999999999.0 #double local var
        pixelstopoint = 0 #local var

        for i in range(2):
            pixelstopoint = utilities.distance(x - self.points[i].x, y - self.points[i].y)*globe.GScale
            if (pixelstopoint < pixelstoclosestpoint): pixelstoclosestpoint = pixelstopoint
        for i in range(len(self.inbetweenpoints)):
            pixelstopoint = utilities.distance(x - self.inbetweenpoints[i].x, y - self.inbetweenpoints[i].y)*globe.GScale
            if (pixelstopoint < pixelstoclosestpoint): pixelstoclosestpoint = pixelstopoint
        if (pixelstoclosestpoint <= globe.MinDistanceFromStream):
            streamover = True
        else:
            streamover = False
        return streamover


    def setproperties(self, asim, aroot):   #public override void setproperties(simulation asim)
        diag = streamproperties(self, asim, aroot)
        #streamproperties streamprop = new streamproperties(this, asim)
        #streamprop.Show()

    
    def drawsection(self, plot, p0, p1, addarrow): #//This method will draw one segment of the stream
                                                     #//between two of its end points, or inbetween points.  
            #private void drawsection(GraphicsPath plot, point p0, point p1, bool addarrow)
        pinterim = point.point(0.0, 0.0) #localvar
        dx = abs(p1.x - p0.x) #localvar
        dy = abs(p1.y - p0.y) #localvar
        if (dx > dy):
            pinterim.x = p0.x
            pinterim.y = p1.y
        else:
            pinterim.x = p1.x
            pinterim.y = p0.y
        linelist = list() #list of line objects that will be created that will all be changed colour together if needed.
        linelist.append(plot.create_line(globe.OriginX + int(globe.GScale * p0.x),
                          globe.OriginY + int(globe.GScale * p0.y),
                          globe.OriginX + int(globe.GScale * pinterim.x),
                          globe.OriginY + int(globe.GScale * pinterim.y)))
        linelist.append(plot.create_line(globe.OriginX + int(globe.GScale * pinterim.x),
                          globe.OriginY + int(globe.GScale * pinterim.y),
                          globe.OriginX + int(globe.GScale * p1.x),
                          globe.OriginY + int(globe.GScale * p1.y)))
        if (addarrow):
            lastdirection = utilities.calcdirection(p1.y - p0.y, p1.x - p0.x) #localvar
            linelist.append(plot.create_line(globe.OriginX + int(globe.GScale * p1.x),
                          globe.OriginY + int(globe.GScale * p1.y),
                          globe.OriginX + int(globe.GScale * (p1.x +
                                globe.StreamArrowLength * math.cos(globe.StreamArrowAngle + math.pi + lastdirection))),
                          globe.OriginY + int(globe.GScale * (p1.y +
                                globe.StreamArrowLength * math.sin(globe.StreamArrowAngle + math.pi + lastdirection)))))
            linelist.append(plot.create_line(globe.OriginX + int(globe.GScale * p1.x),
                          globe.OriginY + int(globe.GScale * p1.y),
                          globe.OriginX + int(globe.GScale * (p1.x +
                                globe.StreamArrowLength * math.cos(-globe.StreamArrowAngle + math.pi + lastdirection))),
                          globe.OriginY + int(globe.GScale * (p1.y +
                                globe.StreamArrowLength * math.sin(-globe.StreamArrowAngle + math.pi + lastdirection)))))
        for line in linelist:
            if (self.highlighted == True):
                plot.itemconfig(line, fill='red')
            elif self.detailtrended:
                plot.itemconfig(line, fill=globe.DetailTrendHighlightColour)
            else:
                plot.itemconfig(line, fill='black')


    def calcdisplaypoints(self): #//Calculate the location on the screen for the properties of the stream that is going to be displayed 
                                         #//on the stream
        longestp0 = self.points[0] #//Need to have a value accordingto compiler. point object, locar var
        longestp1 = self.points[1] #point object, locar var
        tempp0 = point.point(0.0, 0.0) #point object, locar var
        tempp1 = point.point(0.0, 0.0) #point object, locar var
        distancebetweenpoints = 0.0 #double, local var
        furthestdistancebetweenpoints = 0.0 #double, local var
        if (len(self.inbetweenpoints) == 0):
            longestp0 = self.points[0]
            longestp1 = self.points[1]
        else:
            tempp0 = self.points[0]
            tempp1 = self.inbetweenpoints[0]
            distancebetweenpoints = utilities.distance(tempp0, tempp1)
            if (distancebetweenpoints > furthestdistancebetweenpoints):
                furthestdistancebetweenpoints = distancebetweenpoints
                longestp0 = self.points[0]
                longestp1 = self.inbetweenpoints[0]
            for i in range(len(self.inbetweenpoints)):
                tempp0 = self.inbetweenpoints[i - 1]
                tempp1 = self.inbetweenpoints[i]
                distancebetweenpoints = utilities.distance(tempp0, tempp1)
                if (distancebetweenpoints > furthestdistancebetweenpoints):
                    furthestdistancebetweenpoints = distancebetweenpoints
                    longestp0 = self.inbetweenpoints[i - 1]
                    longestp1 = self.inbetweenpoints[i]
            tempp0 = self.inbetweenpoints[-1]
            tempp1 = self.points[1]
            distancebetweenpoints = utilities.distance(tempp0, tempp1)
            if (distancebetweenpoints > furthestdistancebetweenpoints):
                furthestdistancebetweenpoints = distancebetweenpoints
                longestp0 = self.inbetweenpoints[-1]
                longestp1 = self.points[1]
        if (abs(longestp1.x - longestp0.x) > abs(longestp1.y - longestp0.y)):
            deltax = longestp1.x - longestp0.x #double, local var
            for i in range(globe.StreamNrPropDisplay):
                self.displaypoints[i].x = longestp0.x + (i + 1)*deltax / (globe.StreamNrPropDisplay + 1)
                self.displaypoints[i].y = longestp1.y
        else:
            deltay = longestp1.y - longestp0.y #double local var
            for i in range(globe.StreamNrPropDisplay):
                self.displaypoints[i].x = longestp1.x
                self.displaypoints[i].y = longestp0.y + (i + 1) * deltay / (globe.StreamNrPropDisplay + 1);       


    def draw(self, G):   #G will be a canvas object now.     public override void draw(Graphics G)
        plot1 = G  #GraphicsPath
        #Pen plotpen
        #float width = 1
        #plot1 = new GraphicsPath()
        if (len(self.inbetweenpoints) > 0):
            self.drawsection(plot1, self.points[0], self.inbetweenpoints[0], False)
            for i in range(1, len(self.inbetweenpoints)):
                self.drawsection(plot1, self.inbetweenpoints[i - 1], self.inbetweenpoints[i], False)
            self.drawsection(plot1, self.inbetweenpoints[-1], self.points[1], True)
        else:
            self.drawsection(plot1, self.points[0], self.points[1], True)
        #plotpen = new Pen(Color.Black, width)
        #if (highlighted)
        #   plotpen.Color = Color.Red
        #G.DrawPath(plotpen, plot1)
        
        #//The writing of the massflow, pressure and temperature of the stream on the PFD.
        self.calcdisplaypoints()
        #GraphicsPath massflowpath = new GraphicsPath()
        #StringFormat format = StringFormat.GenericDefault
        #FontFamily family = new FontFamily("Arial")
        #int myfontStyle = (int)FontStyle.Bold
        emSize = 8 #local int
        massflowstring = str(round(utilities.fps2fph(self.massflow.v), globe.NormalDigits)) #.ToString("G5") #local string var
        massflowpoint = point.point(globe.OriginX + \
                int(globe.GScale * self.displaypoints[0].x - len(massflowstring) * emSize / 2 / 2), \
                globe.OriginY + int(globe.GScale*(self.displaypoints[0].y)))
        massflowtext = plot1.create_text(massflowpoint.x, massflowpoint.y)
        plot1.itemconfig(massflowtext, text=massflowstring, fill='blue', font=('Helvetica', str(emSize)))

        
        #massflowpath.AddString(massflowstring, family, myfontStyle, emSize, massflowpoint, format)
        #G.FillPath(Brushes.Blue, massflowpath)

        #GraphicsPath pressurepath = new GraphicsPath()
        pressurestring = str(round(utilities.pascal2barg(self.mat.P.v), globe.PressureDigits)) #.ToString("G5")
        pressurepoint = point.point(globe.OriginX +
                int(globe.GScale * self.displaypoints[1].x - len(pressurestring) * emSize / 2 / 2),
                globe.OriginY + int(globe.GScale * self.displaypoints[1].y))
        pressuretext = plot1.create_text(pressurepoint.x, pressurepoint.y)
        plot1.itemconfig(pressuretext, text=pressurestring, fill='green4', font=('Helvetica', str(emSize)))
        #pressurepath.AddString(pressurestring, family, myfontStyle, emSize, pressurepoint, format)
        #G.FillPath(Brushes.Green, pressurepath)

        #GraphicsPath temperaturepath = new GraphicsPath()
        temperaturestring = str(round(utilities.kelvin2celcius(self.mat.T.v), globe.NormalDigits)) #.ToString("G5")
        temperaturepoint = point.point(globe.OriginX + \
                int(globe.GScale * self.displaypoints[2].x - len(temperaturestring) * emSize / 2 / 2), \
                globe.OriginY + int(globe.GScale * self.displaypoints[2].y))
        temperaturetext = plot1.create_text(temperaturepoint.x, temperaturepoint.y)
        plot1.itemconfig(temperaturetext, text=temperaturestring, fill='red',  font=('Helvetica', str(emSize)))
        #temperaturepath.AddString(temperaturestring, family, myfontStyle, emSize, temperaturepoint, format)
        #G.FillPath(Brushes.Red, temperaturepath)



