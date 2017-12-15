import tkinter as tk
from random import randint
import simulation as simulation
import valve as valve
from heatexchangersimple import heatexchangersimple
from tank import tank
from tee import tee
from mixer import mixer
from pump import pump
from coolingtower import coolingtower
from nmpc import nmpc
import globe as globe
import point as point
import stream as stream
import utilities as utilities
from streamproperties import streamproperties
from tkinter import filedialog
import dill

import matplotlib
matplotlib.use("TkAgg")  #This is needed otherwise the app crashes: https://github.com/MTG/sms-tools/issues/36
from matplotlib import pyplot as plt
#import matplotlib.pyplot as plt
#  http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
#  http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
#  http://zetcode.com/gui/tkinter/drawing/

#global data structures for this module --------------------------------------------------------------------------------

#unitops that can be used on the pfd.
pfdunitops = {'Edit' : 1, 'Stream' : 2, 'Valve' : 3, 'HXSimple' : 4, 'Tank' : 5, 'Tee' : 6, 'Mixer' : 7, 'Pump' : 8, \
    'CT' : 9, 'NMPC' : 10}

#class definition ------------------------------------------------------------------------------------------------------

class application(tk.Frame):
     
    def __init__(self, master):
        super().__init__(master)

        self.sim = simulation.simulation()
        self.dmode = globe.drawingmode.Nothing

        self.radiobuttonValue = tk.IntVar()
        self.radiobuttonValue.set(1)
        self.toolsThickness = 2
        self.rgb = "#%02x%02x%02x" % (255, 255, 255)
         
        self.pack()
        self.createWidgets()
        print('Launching ChemSim app...')
 
         
    def createWidgets(self):
        tk_rgb = "#%02x%02x%02x" % (128, 192, 200)        
         
        self.leftFrame = tk.Frame(self, bg = tk_rgb)
        self.leftFrame.pack(side = tk.LEFT, fill = tk.Y)
         
        self.label = tk.Label(self.leftFrame, text = "Time: ")
        self.label.grid(row = 0, column = 0, sticky = tk.NW, pady = 2, padx = 3)
         
        tk.Radiobutton(self.leftFrame,
                    text = 'Edit',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Edit']).grid(padx = 3, pady = 2,
                                    row = 6, column = 0,
                                    sticky = tk.NW
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = "Stream",
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Stream']).grid(padx = 3, pady = 2,
                                    row = 7, column = 0,
                                    sticky = tk.NW
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'Valve',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Valve']).grid(padx = 3, pady = 2,
                                    row = 8, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'HXSimple',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['HXSimple']).grid(padx = 3, pady = 2,
                                    row = 9, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'Tank',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Tank']).grid(padx = 3, pady = 2,
                                    row = 10, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'Tee',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Tee']).grid(padx = 3, pady = 2,
                                    row = 11, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'Mixer',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Mixer']).grid(padx = 3, pady = 2,
                                    row = 12, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'Pump',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['Pump']).grid(padx = 3, pady = 2,
                                    row = 13, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'CT',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['CT']).grid(padx = 3, pady = 2,
                                    row =14, column = 0,
                                    sticky = tk.NW,
                                    )
        tk.Radiobutton(self.leftFrame,
                    text = 'NMPC',
                    variable = self.radiobuttonValue,
                    value = pfdunitops['NMPC']).grid(padx = 3, pady = 2,
                                    row =15, column = 0,
                                    sticky = tk.NW,
                                    )
        
                     
        self.buttonsimfast = tk.Button(self.leftFrame, text = "SimFast",
                                      command = self.simfast)
        self.buttonsimfast.grid(padx = 3, pady = 2,
                                    row = 16, column = 0,
                                    sticky = tk.NW)

        self.buttonsave = tk.Button(self.leftFrame, text = "Save",
                                      command = self.save)
        self.buttonsave.grid(padx = 3, pady = 2,
                                    row = 17, column = 0,
                                    sticky = tk.NW)

        self.buttonopen = tk.Button(self.leftFrame, text = "Open",
                                      command = self.open)
        self.buttonopen.grid(padx = 3, pady = 2,
                                    row=18, column = 0,
                                    sticky = tk.NW)
#----------------------------------------------------------------------
        #self.myCanvas = tk.Canvas(self, width = 800,
        #                        height = 500, scrollregion=(0, 0, 1200, 800), relief=tk.RAISED, borderwidth=5)
        
        

        #self.myCanvas.grid(row=0, column=0)

        #self.myCanvas.pack(side = tk.RIGHT, expand=True,fill=tk.BOTH)
        #self.myCanvas.bind("<B1-Motion>", self.draw)
        #self.myCanvas.bind("<Button-1>", self.setPreviousXY)

        self.canvas=tk.Canvas(self,bg='#FFFFFF',width=1400,height=800,scrollregion=(0,0,3000,2000)) #1220, 800
        self.hbar=tk.Scrollbar(self,orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM,fill=tk.X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=tk.RIGHT,expand=True,fill=tk.BOTH)
        self.canvas.bind("<B1-Motion>", self.mousemoveleftbutton)
        self.canvas.bind('<Motion>', self.mousemove)
        self.canvas.bind("<Button-1>", self.mouseleftbutton)
        self.canvas.bind('<Double-Button-1>', self.mouserightbutton)
        self.canvas.bind('<space>',  self.mouserightbutton)
        self.canvas.bind('<Button-2>',  self.mouserightbutton)
        self.canvas.bind('<Button-3>',  self.mouserightbutton)
        self.canvas.bind('<B2-Motion>',  self.mouserightbutton)
        self.canvas.bind('<B3-Motion>',  self.mouserightbutton)
        
        

        #The right button context menu will be defined here next:
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Trend", command=self.setproperties)
        self.popup_menu.add_command(label="Trend detail", command=self.detailtrend)
        self.popup_menu.add_command(label="Properties", command=self.setproperties)
        self.popup_menu.add_command(label="Delete", command=self.deleteitems)    
         

#----------------------------------------------------------------------
        
         
    def mouseleftbutton(self, event):  #event handler for mouse left button pressed.
        if (self.sim.simulating == False):
            #pointerx = event.x #local var
            #pointery = event.y #local var
            pointerx = self.canvas.canvasx(event.x)
            pointery = self.canvas.canvasy(event.y)
            xonplant = (pointerx - globe.OriginX) / globe.GScale #local var
            yonplant = (pointery - globe.OriginY) / globe.GScale #local var

            if self.radiobuttonValue.get() == pfdunitops['Valve']: self.addnewvalve(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['HXSimple']: self.addnewheatexchangersimple(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['Tank']: self.addnewtank(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['Tee']: self.addnewtee(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['Mixer']: self.addnewmixer(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['Pump']: self.addnewpump(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['CT']: self.addnewcoolingtower(xonplant, yonplant)
            elif self.radiobuttonValue.get() == pfdunitops['NMPC']: self.addnewnmpccontroller(xonplant, yonplant)
            
            elif self.radiobuttonValue.get() == pfdunitops['Stream']:
                dynamicpoint = None #point object
                if self.dmode == globe.drawingmode.Streams:     #//Already drawing one stream
                    self.dmode = globe.drawingmode.Nothing
                    for i in range(len(self.sim.unitops)):
                        for j in range(self.sim.unitops[i].nin):
                            if (self.sim.unitops[i].inpoint[j].highlighted):
                                dynamicpoint = point.point(self.sim.unitops[i].inpoint[j].x, \
                                    self.sim.unitops[i].inpoint[j].y)
                                self.sim.unitops[i].inflow[j] = self.sim.streams[-1]
                    if (dynamicpoint == None):
                        dynamicpoint = point.point(xonplant, yonplant)
                    self.sim.streams[-1].points[1].copyfrom(dynamicpoint)
                else: #//A new stream is just going to be started to be drawn now
                    self.dmode = globe.drawingmode.Streams
                    for i in range(len(self.sim.unitops)):
                        for j in range(self.sim.unitops[i].nout):
                            if (self.sim.unitops[i].outpoint[j].highlighted):
                                dynamicpoint = point.point(self.sim.unitops[i].outpoint[j].x, \
                                        self.sim.unitops[i].outpoint[j].y)
                                self.sim.streams.append(stream.stream(len(self.sim.streams), dynamicpoint.x, \
                                    dynamicpoint.y, dynamicpoint.x, dynamicpoint.y))
                                self.sim.unitops[i].outflow[j] = self.sim.streams[-1]
                    if (dynamicpoint == None):
                        dynamicpoint = point.point(xonplant, yonplant)
                        self.sim.streams.append(stream.stream(len(self.sim.streams), dynamicpoint.x, dynamicpoint.y, \
                            dynamicpoint.x, dynamicpoint.y))

            self.sim.drawnetwork(self.canvas)
        #print("now")
        #self.previousX = event.x
        #self.previousY = event.y


    def mouserightbutton(self, event):
        if (self.sim.simulating == False):
            #pointerx = event.x #local var
            #pointery = event.y #local var
            pointerx = self.canvas.canvasx(event.x)
            pointery = self.canvas.canvasy(event.y)
            xonplant = (pointerx - globe.OriginX) / globe.GScale #local var
            yonplant = (pointery - globe.OriginY) / globe.GScale #local var

            if self.radiobuttonValue.get() == pfdunitops['Stream']:
                dynamicpoint = None #point object
                if self.dmode == globe.drawingmode.Streams:      #//Already drawing one stream
                    self.sim.streams[-1].inbetweenpoints.append(point.point(xonplant, yonplant))
            elif self.radiobuttonValue.get() == pfdunitops['Edit']:
                for i in range(len(self.sim.unitops)):
                    if (self.sim.unitops[i].highlighted): self.popup(event) # { contextMenuStrip1.Show(e.X, e.Y); }
                for i in range(len(self.sim.streams)):
                    if (self.sim.streams[i].highlighted): self.popup(event)
                for i in range(len(self.sim.nmpccontrollers)):
                    if (self.sim.nmpccontrollers[i].highlighted): self.popup(event)


    def mousemoveleftbutton(self, event):
        # line 1
        if (self.sim.simulating == False):
            pointerx = self.canvas.canvasx(event.x) #4 local vars here
            pointery = self.canvas.canvasy(event.y)
            xonplant = (pointerx - globe.OriginX) / globe.GScale 
            yonplant = (pointery - globe.OriginY) / globe.GScale
            if self.radiobuttonValue.get() == pfdunitops['Edit']:
                for i in range(len(self.sim.unitops)):
                    if self.sim.unitops[i].highlighted == True:
                        self.sim.unitops[i].location.x = xonplant
                        self.sim.unitops[i].location.y = yonplant
                for i in range(len(self.sim.nmpccontrollers)):
                    if self.sim.nmpccontrollers[i].highlighted == True:
                        self.sim.nmpccontrollers[i].location.x = xonplant
                        self.sim.nmpccontrollers[i].location.y = yonplant
            self.sim.drawnetwork(self.canvas)
      
        
    def mousemove(self, event):
        if (self.sim.simulating == False):
                #if (sim.nmpccontrollers == null) { sim.nmpccontrollers = new List<nmpc>(); } //THIS LINE SHOULD AT SOME POINT BE DELETED WHEN THE MODEL FILE HAS 
                #//BEEN RECREATED WITH THE LATEST VERSION OF THIS CLASS.
            pointerx = self.canvas.canvasx(event.x) #4 local vars here
            pointery = self.canvas.canvasy(event.y)
            xonplant = (pointerx - globe.OriginX) / globe.GScale 
            yonplant = (pointery - globe.OriginY) / globe.GScale
            if self.radiobuttonValue.get() == pfdunitops['Edit']:
                for i in range(len(self.sim.unitops)):
                    if (self.sim.unitops[i].mouseover(xonplant, yonplant)):
                        self.sim.unitops[i].highlighted = True
                        #if (e.Button == System.Windows.Forms.MouseButtons.Left)
                        #{
                         #   sim.unitops[i].location.x = (pointerx - global.OriginX) / global.GScale;
                        #    sim.unitops[i].location.y = (pointery - global.OriginY) / global.GScale;
                        #}
                    else: self.sim.unitops[i].highlighted = False
                for i in range(len(self.sim.streams)):
                    if (self.sim.streams[i].mouseover((pointerx - globe.OriginX) / globe.GScale, \
                            (pointery - globe.OriginY) / globe.GScale)):
                        self.sim.streams[i].highlighted = True
                        #if (e.Button == System.Windows.Forms.MouseButtons.Left)
                        #{
                        #    point onplant = new point(xonplant,yonplant);
                        #    int pointtomove;
                        #    if (utilities.distance(sim.streams[i].points[0], onplant) < utilities.distance(sim.streams[i].points[1], onplant))
                        #    {
                        #        pointtomove = 0;
                        #    }
                        #    else
                        #    {
                        #        pointtomove = 1;
                        #    }
                        #    sim.streams[i].updatepoint(pointtomove,xonplant,yonplant);
                        #}
                    else: self.sim.streams[i].highlighted = False
                for i in range(len(self.sim.nmpccontrollers)):
                    if (self.sim.nmpccontrollers[i].mouseover(xonplant, yonplant)):
                        self.sim.nmpccontrollers[i].highlighted = True
                        #if (e.Button == System.Windows.Forms.MouseButtons.Left)
                        #{
                        #    sim.nmpccontrollers[i].location.x = (pointerx - global.OriginX) / global.GScale;
                        #    sim.nmpccontrollers[i].location.y = (pointery - global.OriginY) / global.GScale;
                        #}
                    else:
                        self.sim.nmpccontrollers[i].highlighted = False
            elif self.radiobuttonValue.get() == pfdunitops['Stream']:  # //Stream button
                for i in range(len(self.sim.unitops)):
                    for j in range(self.sim.unitops[i].nin):
                        if (utilities.distance(((pointery - globe.OriginY) / globe.GScale - self.sim.unitops[i].inpoint[j].y), \
                                ((pointerx - globe.OriginX) / globe.GScale - self.sim.unitops[i].inpoint[j].x)) <= \
                                globe.MinDistanceFromPoint):
                            self.sim.unitops[i].inpoint[j].highlighted = True
                        else:
                            self.sim.unitops[i].inpoint[j].highlighted = False
                    for j in range(self.sim.unitops[i].nout):
                        if (utilities.distance(((pointery - globe.OriginY) / globe.GScale - self.sim.unitops[i].outpoint[j].y), \
                                ((pointerx - globe.OriginX) / globe.GScale - self.sim.unitops[i].outpoint[j].x)) <= \
                                globe.MinDistanceFromPoint):
                            self.sim.unitops[i].outpoint[j].highlighted = True
                        else:
                            self.sim.unitops[i].outpoint[j].highlighted = False
                if (self.dmode == globe.drawingmode.Streams):
                    self.sim.streams[-1].updatepoint(1, xonplant, yonplant)

        self.sim.drawnetwork(self.canvas)
        #if self.radiobuttonValue.get() == 6: #Valve
         #   self.canvas.create_rectangle(event.x, event.y, event.x + 50, event.y + 20)


    def addnewvalve(self, x, y):
        self.sim.unitops.append(valve.valve(len(self.sim.unitops), x, y, globe.ValveDefaultCv, \
            globe.ValveDefaultOpening))
            #//valve(double ax, double ay, double aCv, double aop) : base(ax, ay, 1, 1)


    def addnewheatexchangersimple(self, x, y):
        self.sim.unitops.append(heatexchangersimple(len(self.sim.unitops), x, y))


    def addnewtank(self, x, y):
        self.sim.unitops.append(tank(len(self.sim.unitops), x, y, \
            globe.TankInitFracInventory, globe.TankInitRadius, globe.TankInitHeight))
        #//tank(double ax, double ay, double amaxvolume, double ainventory, double aradius, double aheight, double adensity) 


    def addnewtee(self, x, y):
        self.sim.unitops.append(tee(len(self.sim.unitops), x, y, globe.TeeDefaultNOut))
            #//tee(double ax, double ay, int anout) : base(ax, ay, 1, anout)


    def addnewmixer(self, x, y):
        self.sim.unitops.append(mixer(len(self.sim.unitops), x, y, globe.MixerDefaultNIn))
            #//mixer(double ax, double ay, int anin) : base(ax, ay, anin, 1)


    def addnewpump(self, xonplant, yonplant):
        self.sim.unitops.append(pump(len(self.sim.unitops), xonplant, yonplant, globe.PumpInitMaxDeltaPressure, \
            globe.PumpInitMinDeltaPressure, globe.PumpInitMaxActualFlow, globe.PumpInitActualVolumeFlow, globe.PumpInitOn))
        #//pump(double ax, double ay, double amaxdeltapressure, double amaxactualflow, double anactualvolumeflow, bool aon)


    def addnewcoolingtower(self, xonplant, yonplant):
        self.sim.unitops.append(coolingtower(len(self.sim.unitops), xonplant, yonplant))


    def addnewnmpccontroller(self, xonplant, yonplant):
        self.sim.nmpccontrollers.append(nmpc(len(self.sim.unitops), xonplant, yonplant, self.sim))
            #//public nmpc(int anr, double ax, double ay)


    def handlestopevent(self):
        #timer1.Enabled = false
        self.sim.setsimulating(False)


    def doreset(self):
        self.handlestopevent()
        self.sim.setsimulationready()


    def simfast(self):
        self.doreset()
        self.sim.setsimulating(True)
        #//sim.simulate(panelGraphics, detailtrends);

        #toolStripLabel1.Text = sim.simtime.timerstring();
        self.sim.drawnetwork(self.canvas)

        for i in range(globe.SimIterations):
            self.sim.simulate(self.canvas, None)
        
        #toolStripLabel1.Text = sim.simtime.timerstring();
        self.sim.drawnetwork(self.canvas)
        self.sim.simi -= 1

        #for (int i = 0; i < detailtrends.Count; i++)
        #{
        #    if (detailtrends[i] != null && detailtrends[i].Visible)
        #    {
        #        detailtrends[i].Invalidate();
        #        detailtrends[i].Update();
        #    }
        #}
        self.handlestopevent()
        self.sim.dodetailtrends(plt)


    def save(self):
        savepath = filedialog.asksaveasfilename(defaultextension=globe.ModelFileExtension)
        print(savepath)
        if savepath != None:
            print('Dilling model to disk...')
            dill.dump(self.sim, open(savepath, 'wb'))

        
    def open(self):
        openpath = filedialog.askopenfilename(defaultextension=globe.ModelFileExtension)
        print(openpath)
        if openpath != None:
            print('Dilling model from disk...')
            self.sim = dill.load(open(openpath, 'rb'))
            self.sim.drawnetwork(self.canvas)


    def popup(self, event):
        intpointerx = int(self.canvas.canvasx(event.x))
        intpointery = int(self.canvas.canvasy(event.y))
        try:
            self.popup_menu.tk_popup(intpointerx, intpointery, 0)
        finally:
            self.popup_menu.grab_release()


    def setproperties(self):
        for i in range(len(self.sim.unitops)):
            if (self.sim.unitops[i].highlighted):
                self.sim.unitops[i].setproperties(self.sim, root)

        for i in range(len(self.sim.streams)):
            if (self.sim.streams[i].highlighted):
                self.sim.streams[i].setproperties(self.sim, root)

        for i in range(len(self.sim.nmpccontrollers)):
            if (self.sim.nmpccontrollers[i].highlighted):
                self.sim.nmpccontrollers[i].setproperties(self.sim, root)


    def detailtrend(self):
        for i in range(len(self.sim.unitops)):
            if (self.sim.unitops[i].highlighted):
                self.sim.unitops[i].showtrenddetail()

        for i in range(len(self.sim.streams)):
            if (self.sim.streams[i].highlighted):
                self.sim.streams[i].showtrenddetail()

        for i in range(len(self.sim.nmpccontrollers)):
            if (self.sim.nmpccontrollers[i].highlighted):
                self.sim.nmpccontrollers[i].showtrenddetail()


    def deleteitems(self):
        idelete = -1
        for i in range(len(self.sim.unitops)):
            if self.sim.unitops[i].highlighted:
                idelete = i
        if idelete >= 0: self.sim.unitops.pop(idelete)

        idelete = -1
        for i in range(len(self.sim.streams)):
            if self.sim.streams[i].highlighted:
                idelete = i
        if idelete >= 0: self.sim.streams.pop(idelete)

        idelete = -1
        for i in range(len(self.sim.nmpccontrollers)):
            if (self.sim.nmpccontrollers[i].highlighted):
                idelete = i
        if (idelete >= 0):
            self.sim.nmpccontrollers.pop(idelete)
                

    def select_all(self):
        pass
        #
         

root = tk.Tk()
root.title("ChemSim")
app = application(root)
root.mainloop() 