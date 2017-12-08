from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities
import globe as globe

import matplotlib
matplotlib.use("TkAgg")  #This is needed otherwise the app crashes: https://github.com/MTG/sms-tools/issues/36
from matplotlib import pyplot as plt


calctarget = {'Determine flow' : 1, 'Determine pressure' : 2}
machinestatus = {'On' : 1, 'Off' : 2}  


class pumpproperties(Dialog):
    def __init__(self, apump, asim, aroot):
        self.thepump = apump
        self.thesim = asim
        
        super(pumpproperties, self).__init__(aroot)

        self.refreshdialogue()


    def body(self, master):
        self.title('Properties for pump: ' + self.thepump.name)

        tk.Label(master, text='Delta pressure').grid(row=0, sticky=tk.W)
        tk.Label(master, text='Actual volume flow').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Max delta pressure').grid(row=2, sticky=tk.W)
        tk.Label(master, text='Max volume flow').grid(row=3, sticky=tk.W)

        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text)
        self.e1text = tk.StringVar()
        self.e1 = tk.Entry(master, textvariable=self.e1text)
        self.e2text = tk.StringVar()
        self.e2 = tk.Entry(master, textvariable=self.e2text)
        self.e3text = tk.StringVar()
        self.e3 = tk.Entry(master, textvariable=self.e3text)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)

        tk.Label(master, text='Streams in').grid(row=4, column=0, sticky=tk.W)
        self.streamsinlistbox = tk.Listbox(master)
        self.streamsinlistbox.grid(row=5, column=0)

        tk.Label(master, text='Streams out').grid(row=4, column=1, sticky=tk.W)
        self.streamsoutlistbox = tk.Listbox(master)
        self.streamsoutlistbox.grid(row=5, column=1)

        tk.Label(master, text='Bara').grid(row=0, column=2, sticky=tk.W)
        tk.Label(master, text='m^3/h actual').grid(row=1, column=2, sticky=tk.W)
        tk.Label(master, text='Bara').grid(row=2, column=2, sticky=tk.W)
        tk.Label(master, text='m^3/h actual').grid(row=3, column=2, sticky=tk.W)

        tk.Label(master, text='Speed target').grid(row=0, column=3, sticky=tk.W)
        tk.Label(master, text='Speed actual dyn').grid(row=1, column=3, sticky=tk.W)
        tk.Label(master, text='Speed tau').grid(row=2, column=3, sticky=tk.W)

        self.e4text = tk.StringVar()
        self.e4 = tk.Entry(master, textvariable=self.e4text)
        self.e5text = tk.StringVar()
        self.e5 = tk.Entry(master, textvariable=self.e5text)
        self.e6text = tk.StringVar()
        self.e6 = tk.Entry(master, textvariable=self.e6text)

        self.e4.grid(row=0, column=4)
        self.e5.grid(row=1, column=4)
        self.e6.grid(row=2, column=4)

        tk.Label(master, text='RPS').grid(row=0, column=5, sticky=tk.W)
        tk.Label(master, text='RPS').grid(row=1, column=5, sticky=tk.W)
        tk.Label(master, text='Seconds').grid(row=2, column=5, sticky=tk.W)
    
        self.radiobuttoncalctarget = tk.IntVar()
        self.radiobuttoncalctarget.set(1)
        tk.Radiobutton(self.theframe,
                    text = 'Determine flow',
                    variable = self.radiobuttoncalctarget,
                    value = calctarget['Determine flow']).grid(padx = 3, pady = 2,
                                    row = 0, column = 6,
                                    sticky = tk.NW
                                    )
        tk.Radiobutton(self.theframe,
                    text = "Determine pressure",
                    variable = self.radiobuttoncalctarget,
                    value = calctarget['Determine pressure']).grid(padx = 3, pady = 2,
                                    row = 1, column = 6,
                                    sticky = tk.NW
                                    )

        self.radiobuttonmachinestatus = tk.IntVar()
        self.radiobuttonmachinestatus.set(1)
        tk.Radiobutton(self.theframe,
                    text = 'On',
                    variable = self.radiobuttonmachinestatus,
                    value = machinestatus['On']).grid(padx = 3, pady = 2,
                                    row = 0, column = 7,
                                    sticky = tk.NW
                                    )
        tk.Radiobutton(self.theframe,
                    text = "Off",
                    variable = self.radiobuttonmachinestatus,
                    value = machinestatus['Off']).grid(padx = 3, pady = 2,
                                    row = 1, column = 7,
                                    sticky = tk.NW
                                    )

        self.hydrauliccurvebutton = tk.Button(self.theframe,
                             text = "Pump hydraulic curve", command = self.pumphydrauliccurve)
        self.hydrauliccurvebutton.grid(row = 15, column = 5, pady = 2, padx = 3, sticky = tk.NW)

        self.powercurvebutton = tk.Button(self.theframe,
                             text = "Pump power curve", command = self.pumppowercurve)
        self.powercurvebutton.grid(row = 16, column = 5, pady = 2, padx = 3, sticky = tk.NW)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        self.e0text.set(str(utilities.pascal2bara(self.thepump.deltapressure.v)))
        self.e1text.set(str(utilities.fps2fph(self.thepump.actualvolumeflow.v)))
        self.e2text.set(str(utilities.pascal2bara(self.thepump.maxdeltapressure)))
        self.e3text.set(str(round(utilities.fps2fph(self.thepump.maxactualvolumeflow.v),globe.NormalDigits)))
        self.e4text.set(str(round(self.thepump.pumpspeed.v,globe.NormalDigits)))
        self.e5text.set(str(round(self.thepump.pumpspeeddynamic,globe.NormalDigits)))
        self.e6text.set(str(self.thepump.speedtau))

        self.streamsinlistbox.delete(0, tk.END)
        self.streamsinlistbox.insert(tk.END, self.thepump.inflow[0].name)
        self.streamsoutlistbox.delete(0, tk.END)
        self.streamsoutlistbox.insert(tk.END, self.thepump.outflow[0].name)

        if (self.thepump.calcmethod == globe.calculationmethod.DetermineFlow):
            self.radiobuttoncalctarget.set(calctarget['Determine flow']) #Default will be that the pump will determine the flow through it.
        else:
            self.radiobuttoncalctarget.set(calctarget['Determine pressure'])
        if self.thepump.on.v < 0.5:
            self.radiobuttonmachinestatus.set(machinestatus['Off'])


    def validate(self):
        try:
            self.thepump.maxdeltapressure = utilities.bara2pascal(float(self.e2.get()))
            self.thepump.maxactualvolumeflow.v = utilities.fph2fps(float(self.e3.get()))
            self.thepump.pumpspeed.v = float(self.e4.get())
            self.thepump.speedtau = float(self.e6.get())

            if self.radiobuttoncalctarget.get() == calctarget['Determine flow']:
                self.thepump.calcmethod = globe.calculationmethod.DetermineFlow
            else:
                self.thepump.calcmethod = globe.calculationmethod.DeterminePressure
            if self.radiobuttonmachinestatus.get() == machinestatus['On']:
                self.thepump.on.v = 1
            else:
                self.thepump.on.v = 0

        except ValueError:
            print("That's not a number!")
            return 0

        self.thepump.update(self.thesim.simi, False)
        self.refreshdialogue()
        return 1


    def pumphydrauliccurve(self, event=None):
        volumeflow = [0.0]*11
        pressure = [0.0]*11
        for i in range(11):
            volumeflow[i] = i/10.0*self.thepump.maxactualvolumeflow.v
            pressure[i] = self.thepump.calcdeltapressurequadratic(volumeflow[i])  
            #//pressure[i] = thepump.pumpcurvem*volumeflow[i] + thepump.pumpcurvec;

        plt.plot(volumeflow, pressure)
        plt.title('Pressure increase over pump (Pa) : ' + self.thepump.name)
        plt.show()



    def pumppowercurve(self, event=None):
        volumeflow = [0.0]*11
        pressure = [0.0]*11
        massflow = [0.0]*11
        power = [0.0]*11
        for i in range(11):
            volumeflow[i] = i / 10.0 * self.thepump.maxactualvolumeflow.v
            pressure[i] = self.thepump.calcdeltapressurequadratic(volumeflow[i])
            massflow[i] = volumeflow[i] * self.thepump.inflow[0].mat.density.v
            power[i] = self.thepump.calcpumppower(volumeflow[i], pressure[i])
            #//pressure[i] = thepump.pumpcurvem*volumeflow[i] + thepump.pumpcurvec

        plt.plot(volumeflow, power)
        plt.title('Pump power consumption (W) : ' + self.thepump.name)
        plt.show()





