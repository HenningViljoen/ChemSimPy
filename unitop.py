import baseprocessclass as baseprocessclass
import stream as stream
import point as point
import globe as globe

class unitop(baseprocessclass.baseprocessclass):


    def __init__(self, anr, ax, ay, anin, anout):
        #public unitop(int anr, double ax, double ay, int anin, int anout)
        super(unitop, self).__init__(anr, ax, ay)

        self.inflow = list()  #public baseprocessclass[] 
        self.outflow = list()  #public baseprocessclass[] 
        self.inpoint = list()   # public point[]  //the points where the stream(s) are coming into the unitop
        self.outpoint = list() #public point[] //the points where the stream(s) are going out of the unitop.
        self.nin = 0 #public int 
        self.nout = 0 # //amount of streams in, and amount of streams out.

        self.initunitop(anin, anout)


    def unitopcopyconstructor(self, unitopcopyfrom):  #public unitop(unitop unitopcopyfrom)
        #: base(unitopcopyfrom.nr, unitopcopyfrom.location.x, unitopcopyfrom.location.y)
        self.initunitop(unitopcopyfrom.nin, unitopcopyfrom.nout)
        self.copyfrom(unitopcopyfrom)


    def initunitop(self, anin, anout):  #private void initunitop(int anin, int anout)
        self.nin = anin
        self.nout = anout
        self.initinflow()
        self.initoutflow()
        self.initinpoint()
        self.initoutpoint()


    def copyfrom(self, baseclasscopyfrom):
            #public override void copyfrom(baseclass baseclasscopyfrom)
        unitopcopyfrom = baseclasscopyfrom
        #unitop unitopcopyfrom = (unitop)baseclasscopyfrom;
        super(unitop, self).copyfrom(unitopcopyfrom)
        #base.copyfrom(unitopcopyfrom);

            #//public baseprocessclass[] inflow;
            #//public baseprocessclass[] outflow;
            #//public point[] inpoint;   //the points where the stream(s) are coming into the unitop
            #//public point[] outpoint; //the points where the stream(s) are going out of the unitop.
            #//public int nin, nout; //amount of streams in, and amount of streams out.

        for i in range(len(self.inflow)): self.inflow[i].copyfrom(unitopcopyfrom.inflow[i])
        for i in range(len(self.outflow)): self.outflow[i].copyfrom(unitopcopyfrom.outflow[i]) 
        for i in range(len(self.inpoint)): self.inpoint[i].copyfrom(unitopcopyfrom.inpoint[i]) 
        for i in range(len(self.outpoint)): self.outpoint[i].copyfrom(unitopcopyfrom.outpoint[i]) 
        self.nin = unitopcopyfrom.nin
        self.nout = unitopcopyfrom.nout


    def initinflow(self):
        self.inflow = [stream.stream]*self.nin
        for i in range(self.nin):
            self.inflow[i] = stream.stream(0, self.location.x, self.location.y, self.location.x, self.location.y)

            

    def initoutflow(self):
        self.outflow = [stream.stream]*self.nout
        for i in range(self.nout):
            self.outflow[i] = stream.stream(0, self.location.x, self.location.y, self.location.x, self.location.y)


    def initinpoint(self):
        self.inpoint = [point.point]*self.nin #  //To be changed by derived classes.
        for i in range(self.nin): self.inpoint[i] = point.point(self.location.x, self.location.y)  #//To be changed by derived classes.


    def initoutpoint(self):
        self.outpoint = [point.point]*self.nout #//To be changed by derived classes.
        for i in range(self.nout): self.outpoint[i] = point.point(self.location.x, self.location.y)   #//To be changed by derived classes.


    def updateinoutpointlocations(self):
        for i in range(self.nin):
            if (self.inflow[i] != None): self.inflow[i].points[1].copyfrom(self.inpoint[i])
        for i in range(self.nout):
            if (self.outflow[i] != None): self.outflow[i].points[0].copyfrom(self.outpoint[i])


    def update(self, i, historise): #public override void update(int i, bool historise)
        super(unitop, self).update(i, historise)


    def draw(self, canvas):
        pass
    #    //Draw inpoint
    #    GraphicsPath[] inpointdraw = new GraphicsPath[nin];
     #   Pen plotPen = new Pen(Color.Black, 1);
     #   SolidBrush brush = new SolidBrush(Color.White);
        for i in range(self.nin):
            point0 = point.point(globe.OriginX + int(globe.GScale*(self.inpoint[i].x)), \
                        globe.OriginY + int(globe.GScale*(self.inpoint[i].y)))    
            point1 = point.point(globe.OriginX + int(globe.GScale*(self.inpoint[i].x + globe.InOutPointWidth)), \
                        globe.OriginY + int(globe.GScale*(self.inpoint[i].y - globe.InOutPointHeight)))
            point2 = point.point(globe.OriginX + int(globe.GScale*(self.inpoint[i].x + globe.InOutPointWidth)), 
                        globe.OriginY + int(globe.GScale*(self.inpoint[i].y + globe.InOutPointHeight)))

            inputpoint = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y)

            if (self.inpoint[i].highlighted == True):
                canvas.itemconfig(inputpoint, fill='red')
            else:
                canvas.itemconfig(inputpoint, fill='black')
            #inpointdraw[i] = new GraphicsPath();

            #Point[] inpointarray = new Point[] 
            #{new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[i].x)), 
            #            global.OriginY + Convert.ToInt32(global.GScale*(inpoint[i].y))), 
            #new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[i].x + global.InOutPointWidth)), 
            #            global.OriginY + Convert.ToInt32(global.GScale*(inpoint[i].y - global.InOutPointHeight))), 
            #new Point(global.OriginX + Convert.ToInt32(global.GScale*(inpoint[i].x + global.InOutPointWidth)), 
            #            global.OriginY + Convert.ToInt32(global.GScale*(inpoint[i].y + global.InOutPointHeight)))};
            #inpointdraw[i].AddPolygon(inpointarray);
            #brush.Color = (inpoint[i].highlighted) ? Color.Orange : Color.White;
            #plotPen.Color = (inpoint[i].highlighted) ? Color.Red : Color.Black;
            #G.FillPath(brush, inpointdraw[i]);
            #G.DrawPath(plotPen, inpointdraw[i]);


      #  //Draw outpoint
     #   GraphicsPath[] outpointdraw = new GraphicsPath[nout];
        for i in range(self.nout):
            point0 = point.point(globe.OriginX + int(globe.GScale*(self.outpoint[i].x)), \
                        globe.OriginY + int(globe.GScale*(self.outpoint[i].y)))
            point1 = point.point(globe.OriginX + int(globe.GScale*(self.outpoint[i].x - globe.InOutPointWidth)), \
                        globe.OriginY + int(globe.GScale*(self.outpoint[i].y + globe.InOutPointHeight)))
            point2 = point.point(globe.OriginX + int(globe.GScale*(self.outpoint[i].x - globe.InOutPointWidth)), \
                        globe.OriginY + int(globe.GScale*(self.outpoint[i].y - globe.InOutPointHeight)))
            outputpoint = canvas.create_polygon(point0.x, point0.y, point1.x, point1.y, point2.x, point2.y)

            if (self.outpoint[i].highlighted == True):
                canvas.itemconfig(outputpoint, fill='red')
            else:
                canvas.itemconfig(outputpoint, fill='black')
      #      outpointdraw[i] = new GraphicsPath();
      #      Point[] outpointarray = new Point[] 
      #      {new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[i].x)), 
       #                 global.OriginY + Convert.ToInt32(global.GScale*(outpoint[i].y))), 
       #     new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[i].x - global.InOutPointWidth)), 
       #                 global.OriginY + Convert.ToInt32(global.GScale*(outpoint[i].y + global.InOutPointHeight))), 
       #     new Point(global.OriginX + Convert.ToInt32(global.GScale*(outpoint[i].x - global.InOutPointWidth)), 
       #                 global.OriginY + Convert.ToInt32(global.GScale*(outpoint[i].y - global.InOutPointHeight)))};
        #    outpointdraw[i].AddPolygon(outpointarray);
       #     brush.Color = (outpoint[i].highlighted) ? Color.Orange : Color.White;
       ##     plotPen.Color = (outpoint[i].highlighted) ? Color.Red : Color.Black;
       #     G.FillPath(brush, outpointdraw[i]);
       #     G.DrawPath(plotPen, outpointdraw[i]);
