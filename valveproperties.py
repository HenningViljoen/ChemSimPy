from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities

class valveproperties(Dialog):
    def __init__(self, avalve, asim, aroot):
        self.thevalve = avalve
        self.thesim = asim
        
        super(valveproperties, self).__init__(aroot)

        self.refreshdialogue()
        #if (thevalve.inflow[0] != null) { listView1.Items.Add(thevalve.inflow[0].nr.ToString()); }
        #if (thevalve.outflow[0] != null) { listView2.Items.Add(thevalve.outflow[0].nr.ToString()); }


    def body(self, master):
        self.title('Valve Properties: ' + str(self.thevalve.nr))

        tk.Label(master, text='Name').grid(row=0, sticky=tk.W)
        tk.Label(master, text='Delta pressure').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Actual volume flow').grid(row=2, sticky=tk.W)
        tk.Label(master, text='Standard volume flow').grid(row=3, sticky=tk.W)
        tk.Label(master, text='Mass flow').grid(row=4, sticky=tk.W)
        tk.Label(master, text='Molar volume flow').grid(row=5, sticky=tk.W)
        tk.Label(master, text='Valve Cv').grid(row=6, sticky=tk.W)
        tk.Label(master, text='Valve opening').grid(row=7, sticky=tk.W)

        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text)
        self.e1text = tk.StringVar()
        self.e1 = tk.Entry(master, textvariable=self.e1text)
        self.e2text = tk.StringVar()
        self.e2 = tk.Entry(master, textvariable=self.e2text)
        self.e3text = tk.StringVar()
        self.e3 = tk.Entry(master, textvariable=self.e3text)
        self.e4text = tk.StringVar()
        self.e4 = tk.Entry(master, textvariable=self.e4text)
        self.e5text = tk.StringVar()
        self.e5 = tk.Entry(master, textvariable=self.e5text)
        self.e6text = tk.StringVar()
        self.e6 = tk.Entry(master, textvariable=self.e6text)
        self.e7text = tk.StringVar()
        self.e7 = tk.Entry(master, textvariable=self.e7text)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)
        self.e5.grid(row=5, column=1)
        self.e6.grid(row=6, column=1)
        self.e7.grid(row=7, column=1)

        tk.Label(master, text='Bara').grid(row=1, column=3, sticky=tk.W)
        tk.Label(master, text='m^3/h').grid(row=2, column=3, sticky=tk.W)
        tk.Label(master, text='Nm^3/h').grid(row=3, column=3, sticky=tk.W)
        tk.Label(master, text='kg/h').grid(row=4, column=3, sticky=tk.W)
        tk.Label(master, text='mol/s').grid(row=5, column=3, sticky=tk.W)
        tk.Label(master, text='m^3/s/(Pa^0.5)').grid(row=6, column=3, sticky=tk.W)
        tk.Label(master, text='Fraction (0 to 1)').grid(row=7, column=3, sticky=tk.W)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        #self.e0.set(self.thevalve.name)
        #self.theframe.itemconfig(self.e0, textvariable='red')
        #self.e0.insert(0, 'default text')
        self.e0text.set(self.thevalve.name)
        self.e1text.set(str(utilities.pascal2bara(self.thevalve.deltapressure.v)))
        self.e2text.set(str(utilities.fps2fph(self.thevalve.actualvolumeflow.v)))
        self.e3text.set(str(utilities.fps2fph(self.thevalve.standardvolumeflow.v)))
        self.e4text.set(str(utilities.fps2fph(self.thevalve.massflow.v)))
        self.e5text.set(str(self.thevalve.molarflow.v))
        self.e6text.set(str(self.thevalve.Cv))
        self.e7text.set(str(self.thevalve.op.v))


    def validate(self):
        try:
            self.thevalve.name = self.e0.get()
            self.thevalve.Cv = float(self.e6.get())
            self.thevalve.op.v = float(self.e7.get())
        except ValueError:
            print("That's not an int!")
            return 0

        return 1


    #def apply(self):
    #    first = int(self.e1.get())
    #    second = int(self.e2.get())
        #print first, second # or something