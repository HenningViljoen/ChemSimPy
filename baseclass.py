import tkinter as tk
import globe as globe
import point as point
import copy

class baseclass(object):
    def __init__(self, anr, ax, ay):
        #//public bool on; //Is the equipment/unitop/stream/controller, on, or off.
        self.nr = anr #Index of this object in the collection that it is part of.
        self.name = "" #//Name of the piece of equipment / stream that is under scope.
        #on = true;
        self.objecttype = globe.objecttypes.Valve #What kind of unit op is a particular one. Just select anyone to initialize with
        self.controlproperties = list() #list of strings
        self.controlpropthisclass = list() #list of strings
        self.nrcontrolpropinherited = 0
        self.highlighted = False
        self.detailtrended = False
        self.location = point.point(ax, ay)
        self.points = list() #point objects used for the item on the PFD.  Expressed in meters.


    def copyfrom(self, baseclasscopyfrom):
        self.nr = baseclasscopyfrom.nr
        self.name = baseclasscopyfrom.name
        #//on = baseclasscopyfrom.on;
        self.objecttype = baseclasscopyfrom.objecttype
        self.highlighted = baseclasscopyfrom.highlighted
        self.location.copyfrom(baseclasscopyfrom.location)
        self.controlproperties = copy.deepcopy(baseclasscopyfrom.controlproperties)
        self.controlpropthisclass = copy.deepcopy(baseclasscopyfrom.controlpropthisclass)
        self.nrcontrolpropinherited = baseclasscopyfrom.nrcontrolpropinherited


    def selectedproperty(self, selection):
        pass


    def update(self, i, historise): #index for where in the simvectors the update is to be stored, 
                                                            #//boolean for whether or not history should be kept for the simulation
                                                            #//at this time.
        pass
        

    def updatepoint(self, i, x, y):
        pass


    def mouseover(self, x, y): #//This function will indicate whether the mouse is over a particular unitop or stream at any moment in time.
        pass


    def setproperties(self, asim, aroot): #//Method that will be inherited and that will set the properties of the applicable object in a window
        pass


    def showtrenddetail(self): #//Virtual method that will set up the trend detail window for the 
        #//                                                     //applicable object.
        pass


    def dodetailtrend(self, plt):  #This method will be overriden and will define how the execution of the trends will be done.
        pass


    def draw(self, G):
        pass
