from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities
import globe as globe


machinestatus = {'On' : 1, 'Off' : 2}  


class coolingtowerproperties(Dialog):
    def __init__(self, acoolingtower, asim, aroot):
        self.thecoolingtower = acoolingtower
        self.thesim = asim
        
        super(coolingtowerproperties, self).__init__(aroot)

        self.refreshdialogue()


    def body(self, master):
        self.title('Properties for cooling tower: ' + self.thecoolingtower.name)

        tk.Label(master, text='Name').grid(row=0, sticky=tk.W)
        tk.Label(master, text='Water volume fraction').grid(row=1, sticky=tk.W)
        tk.Label(master, text='CT default mass transfer coef air').grid(row=2, sticky=tk.W)
        tk.Label(master, text='CT default heat transfer coef water').grid(row=3, sticky=tk.W)
        tk.Label(master, text='CT default heat transfer coef air').grid(row=4, sticky=tk.W)
        tk.Label(master, text='Fan speed').grid(row=5, sticky=tk.W)

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

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)
        self.e5.grid(row=5, column=1)

        tk.Label(master, text='Streams in').grid(row=6, column=0, sticky=tk.W)
        self.streamsinlistbox = tk.Listbox(master)
        self.streamsinlistbox.grid(row=7, column=0)

        tk.Label(master, text='Streams out').grid(row=6, column=1, sticky=tk.W)
        self.streamsoutlistbox = tk.Listbox(master)
        self.streamsoutlistbox.grid(row=7, column=1)

        tk.Label(master, text='fraction').grid(row=1, column=2, sticky=tk.W)
        tk.Label(master, text='kg/(s*m^2)').grid(row=2, column=2, sticky=tk.W)
        tk.Label(master, text='W/(m^2*K)').grid(row=3, column=2, sticky=tk.W)
        tk.Label(master, text='W/(m^2*K)').grid(row=4, column=2, sticky=tk.W)
        tk.Label(master, text='RPS').grid(row=5, column=2, sticky=tk.W)

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

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        self.e0text.set(self.thecoolingtower.name)
        self.e1text.set(str(self.thecoolingtower.watervolumefraction.v))
        self.e2text.set(str(self.thecoolingtower.masstransfercoefair.v))
        self.e3text.set(str(self.thecoolingtower.heattransfercoefwater.v))
        self.e4text.set(str(self.thecoolingtower.heattransfercoefair.v))
        self.e5text.set(str(round(self.thecoolingtower.fanspeed.v, globe.NormalDigits)))


        self.streamsinlistbox.delete(0, tk.END)
        self.streamsinlistbox.insert(tk.END, self.thecoolingtower.inflow[0].name)
        self.streamsoutlistbox.delete(0, tk.END)
        self.streamsoutlistbox.insert(tk.END, self.thecoolingtower.outflow[0].name)

        if self.thecoolingtower.on.v < 0.5:
            self.radiobuttonmachinestatus.set(machinestatus['Off'])


    def validate(self):
        try:
            self.thecoolingtower.name = self.e0.get()
            self.thecoolingtower.watervolumefraction.v = float(self.e1.get())
            self.thecoolingtower.masstransfercoefair.v = float(self.e2.get())
            self.thecoolingtower.heattransfercoefwater.v = float(self.e3.get())
            self.thecoolingtower.heattransfercoefair.v = float(self.e4.get())
            self.thecoolingtower.fanspeed.v = float(self.e5.get())

            if self.radiobuttonmachinestatus.get() == machinestatus['On']:
                self.thecoolingtower.on.v = 1
            else:
                self.thecoolingtower.on.v = 0

        except ValueError:
            print("That's not a number!")
            return 0

        self.thecoolingtower.updatefrompropertydialogue()
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







