import simtimer as simtimer
import globe as globe
from coolingtower import coolingtower
from heatexchangersimple import heatexchangersimple
from mixer import mixer
from pump import pump
from tee import tee
from valve import valve
from tank import tank
from stream import stream
from pidcontroller import pidcontroller


class simulation(object):
    def __init__(self):
        #public List<unitop> unitops #//All the unit ops in the model.
        #public List<stream> streams #//All the items streams in the model.
        #public List<block> blocks #//The DCS blocks in the simulation.
        #public List<signal> signals #//All the signals in the model.
        #public List<pidcontroller> pidcontrollers #//All pidcontrollers in the model.
        #//public List<controlmvsignalsplitter> controlmvsignalsplitters
        #public List<nmpc> nmpccontrollers #//All NMPC controllers in the model.
        self.simi = 0 # int //Counting index for this class for simulation indexing for historisation and simulation.
        self.simulating = False #bool
        #public simtimer simtime
        self.initsimulation()


    def simulationcopyconstructor(self, simcopyfrom):   #simulation simcopyfrom
        self.initsimulation()
        self.copyfrom(simcopyfrom)


    def initsimulation(self):
        self.unitops = list() # new List<unitop>()
        self.streams = list() #new List<stream>()
        self.signals = list() #new List<signal>()
        self.pidcontrollers = list() #new List<pidcontroller>()
        self.blocks = list() #new List<block>()
        self.nmpccontrollers = list() #new List<nmpc>()

        self.simtime = simtimer.simtimer(0, 0, 0, 0)
        #setsimulationready()


    def copyfrom(self, simcopyfrom):
        #//MemoryStream myStream = new MemoryStream();
        #//simulation tempsim = new simulation();
        #//BinaryFormatter bf = new BinaryFormatter();
        #//bf.Serialize(myStream, simcopyfrom); 
        #//myStream.Seek(0, SeekOrigin.Begin); 
        #//tempsim = (simulation)bf.Deserialize(myStream);
        #//myStream.Close();
        #//unitops = tempsim.unitops;
        #//streams = tempsim.streams;
        #//pidcontrollers = tempsim.pidcontrollers;
        if (len(self.unitops) == 0):
            self.unitops = []
            for i in range(len(simcopyfrom.unitops)):  
                #if simcopyfrom.unitops[i].objecttype == globe.objecttypes.CoolingTowerSimple:
                #    #obj = coolingtowersimple()
                #    obj.coolingtowersimplecopyconstructor(simcopyfrom.unitops[i])
                #    self.unitops.append(obj)
                #elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.CoolingTowerHeatExchangerSimple:
                #    obj = coolingtowerheatexchangersimple()
                #    obj.coolingtowerheatexchangersimplecopyconstructor(simcopyfrom.unitops[i])
                #    self.unitops.append(obj)
                if simcopyfrom.unitops[i].objecttype == globe.objecttypes.CoolingTower:
                    obj = coolingtower(0,0,0)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                #elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.DistillationColumn:
                #    obj = distillationcolumn()
                #    obj.copyfrom(simcopyfrom.unitops[i])
                 #   self.unitops.append(obj)
                #elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.Flange:
                #    obj = flange()
                #    obj.flangecopyconstructor(simcopyfrom.unitops[i])
                #    self.unitops.append(obj)
                #elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.GasPipe:
                 #   obj = gaspipe()
                 #   obj.gaspipecopyconstructor(simcopyfrom.unitops[i])
                #    self.unitops.append(obj)
                elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.HeatExchangerSimple:
                    obj = heatexchangersimple(0,0,0)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.Mixer:
                    obj = mixer(0,0,0,simcopyfrom.unitops[i].nin)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.Pump:
                    obj = pump(0.0, 0.0, 0.0, 0.0, 0.0, \
                            0.0, 0.0, 1)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.Tee:
                    obj = tee(0.0, 0.0, 0.0, simcopyfrom.unitops[i].nout)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.Valve:
                    obj = valve(0, 0.0, 0.0)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                elif simcopyfrom.unitops[i].objecttype == globe.objecttypes.Tank:
                    obj = tank(0, 0.0, 0.0)
                    obj.copyfrom(simcopyfrom.unitops[i])
                    self.unitops.append(obj)
                else:
                    break
        else:
            for i in range(len(simcopyfrom.unitops)):
                self.unitops[i].copyfrom(simcopyfrom.unitops[i])

        if (len(self.streams) == 0):
            self.streams = []
            for i in range(len(simcopyfrom.streams)):
                obj = stream(0, 0.0, 0.0, 0.0, 0.0)
                obj.copyfrom(simcopyfrom.streams[i])
                self.streams.append(obj)
        else:
            for i in range(len(simcopyfrom.streams)):
                self.streams[i].copyfrom(simcopyfrom.streams[i])

        #if (len(self.signals) == 0):
        #    self.signals = []
        #    for i in range(len(simcopyfrom.signals)):
        #        obj = signal()
         #       obj.copyfrom(simcopyfrom.signals[i])
        #        self.signals.append(obj)
        #else:
        #    for i in range(len(simcopyfrom.signals)):
        #        self.signals[i].copyfrom(simcopyfrom.signals[i])

        if (len(self.pidcontrollers) == 0):
            self.pidcontrollers = []
            for i in range(len(simcopyfrom.pidcontrollers)):
                obj = pidcontroller()
                obj.copyfrom(simcopyfrom.pidcontrollers[i])
                self.pidcontrollers.append(obj)
        else:
            for i in range(len(simcopyfrom.pidcontrollers)):
                self.pidcontrollers[i].copyfrom(simcopyfrom.pidcontrollers[i])

        #if (len(self.blocks) == 0):
        #    self.blocks = []
        #    for i in range(len(simcopyfrom.blocks)):
         #       if simcopyfrom.blocks[i].objecttype == globe.objecttypes.ControlMVSignalSplitter:
         #           obj = controlmvsignalsplitter()
         #           obj.copyfrom(simcopyfrom.blocks[i])
         #           blocks.append(obj)
         #       else:
         #           break
        #else:
         #   for i in range(len(simcopyfrom.blocks)):
        #        self.blocks[i].copyfrom(simcopyfrom.blocks[i])

        #//public List<nmpc> nmpccontrollers; The nmpc controller(s) are not going to be copied at this point in time.
        self.simi = simcopyfrom.simi #//Counting index for this class for simulation indexing for historisation and simulation.


    def setsimulating(self, asimulating):
        self.simulating = asimulating


    def setsimulationready(self):
        self.simi = 0
        self.setsimulating(False)
        self.simtime.reset()


    def drawnetwork(self, canvas):
        canvas.delete("all") #G.Clear(Color.White);
        for i in range(len(self.unitops)): self.unitops[i].draw(canvas)
        for i in range(len(self.streams)): self.streams[i].draw(canvas)
            #for (int i = 0; i < signals.Count; i++) { signals[i].draw(G); }
        for i in range(len(self.pidcontrollers)): self.pidcontrollers[i].draw(canvas)
        if (self.blocks != None):
            for i in range(len(self.blocks)): self.blocks[i].draw(canvas)
        for i in range(len(self.nmpccontrollers)): self.nmpccontrollers[i].draw(canvas)


    def simulateplant(self, historise): #//This method is called from main simulate method, and also from the nmpc controller.
                                        #public void simulateplant(bool historise)
        for i in range(len(self.unitops)): self.unitops[i].update(self.simi, historise)
        for i in range(len(self.streams)):  self.streams[i].update(self.simi, historise)
        for i in range(len(self.signals)):  self.signals[i].update(self.simi, historise)
        for i in range(len(self.pidcontrollers)): self.pidcontrollers[i].update(self.simi, historise)
        if (self.blocks != None):
            for i in range(len(self.blocks)): self.blocks[i].update(self.simi, historise)

        
    def simulate(self, canvas, detailtrends): #public void simulate(Graphics G, List<Form> detailtrends)
        #if (nmpccontrollers == null) { nmpccontrollers = new List<nmpc>(); } #//THIS LINE SHOULD AT SOME POINT BE DELETED WHEN THE MODEL FILE HAS 
                                                                                    #//BEEN RECREATED WITH THE LATEST VERSION OF THIS CLASS.
        #if (blocks == null) { blocks = new List<block>(); }
        for i in range(len(self.nmpccontrollers)): self.nmpccontrollers[i].update(self.simi, True)
            
        self.simulateplant(True)

        #if ((detailtrends != null) && (simi % global.TrendUpdateIterPeriod == 0))
        #{
        #    for (int i = 0; i < detailtrends.Count; i++)
        #    {
        #        if (detailtrends[i] != null && detailtrends[i].Visible)
        #        {
        #            detailtrends[i].Invalidate();
        #            detailtrends[i].Update();
        #        }
        #    }
        #}
        self.simtime.tick()
        self.simi += 1


    def dodetailtrends(self, plt): #detail trends for all that was checked for it.
        for i in range(len(self.unitops)): self.unitops[i].dodetailtrend(plt)
        for i in range(len(self.streams)):  self.streams[i].dodetailtrend(plt)
        for i in range(len(self.nmpccontrollers)):  self.nmpccontrollers[i].dodetailtrend(plt)
        for i in range(len(self.signals)):  self.nmpccontrollers[i].dodetailtrend(plt)
        for i in range(len(self.pidcontrollers)): self.pidcontrollers[i].dodetailtrend(plt)
        if (self.blocks != None):
            for i in range(len(self.blocks)): self.blocks[i].dodetailtrend(plt)
        plt.show()
    



