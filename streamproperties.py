from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities

#The main stream compositions that will be facilitated on the stream properties diag:
streamcompositions = {'Water' : 1, 'Air' : 2}
flowinputtypes = {'Mass flow' : 1, 'Standard flow' : 2}  #The flow input types that can be set


class streamproperties(Dialog):
    def __init__(self, astream, asim, aroot):
        self.thestream = astream
        self.thesim = asim
        
        super(streamproperties, self).__init__(aroot)

        self.refreshdialogue()
        #if (thevalve.inflow[0] != null) { listView1.Items.Add(thevalve.inflow[0].nr.ToString()); }
        #if (thevalve.outflow[0] != null) { listView2.Items.Add(thevalve.outflow[0].nr.ToString()); }


    def body(self, master):
        self.title('Properties for stream number: ' + str(self.thestream.nr))

        tk.Label(master, text='Name').grid(row=0, sticky=tk.W)
        tk.Label(master, text='Pressure').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Temperature').grid(row=2, sticky=tk.W)
        tk.Label(master, text='Humidity (Relative)').grid(row=3, sticky=tk.W)
        tk.Label(master, text='Volume').grid(row=4, sticky=tk.W)
        tk.Label(master, text='f (vapour fraction)').grid(row=5, sticky=tk.W)
        tk.Label(master, text='Density').grid(row=6, sticky=tk.W)
        tk.Label(master, text='Mass of 1 mol').grid(row=7, sticky=tk.W)
        tk.Label(master, text='Actual volume flow').grid(row=8, sticky=tk.W)
        tk.Label(master, text='Standard volume flow').grid(row=9, sticky=tk.W)
        tk.Label(master, text='Mass flow').grid(row=10, sticky=tk.W)
        tk.Label(master, text='Molar flow').grid(row=11, sticky=tk.W)
        tk.Label(master, text='Heat capacity').grid(row=12, sticky=tk.W)
        tk.Label(master, text='Direction').grid(row=13, sticky=tk.W)
        tk.Label(master, text='Distance').grid(row=14, sticky=tk.W)

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
        self.e8text = tk.StringVar()
        self.e8 = tk.Entry(master, textvariable=self.e8text)
        self.e9text = tk.StringVar()
        self.e9 = tk.Entry(master, textvariable=self.e9text)
        self.e10text = tk.StringVar()
        self.e10 = tk.Entry(master, textvariable=self.e10text)
        self.e11text = tk.StringVar()
        self.e11 = tk.Entry(master, textvariable=self.e11text)
        self.e12text = tk.StringVar()
        self.e12 = tk.Entry(master, textvariable=self.e12text)
        self.e13text = tk.StringVar()
        self.e13 = tk.Entry(master, textvariable=self.e13text)
        self.e14text = tk.StringVar()
        self.e14 = tk.Entry(master, textvariable=self.e14text)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)
        self.e5.grid(row=5, column=1)
        self.e6.grid(row=6, column=1)
        self.e7.grid(row=7, column=1)
        self.e8.grid(row=8, column=1)
        self.e9.grid(row=9, column=1)
        self.e10.grid(row=10, column=1)
        self.e11.grid(row=11, column=1)
        self.e12.grid(row=12, column=1)
        self.e13.grid(row=13, column=1)
        self.e14.grid(row=14, column=1)

        tk.Label(master, text='Barg').grid(row=1, column=3, sticky=tk.W)
        tk.Label(master, text='DegC').grid(row=2, column=3, sticky=tk.W)
        tk.Label(master, text='%').grid(row=3, column=3, sticky=tk.W)
        tk.Label(master, text='m^3').grid(row=4, column=3, sticky=tk.W)
        tk.Label(master, text='fraction').grid(row=5, column=3, sticky=tk.W)
        tk.Label(master, text='kg/m^3').grid(row=6, column=3, sticky=tk.W)
        tk.Label(master, text='kg/mol').grid(row=7, column=3, sticky=tk.W)
        tk.Label(master, text='m^3/h').grid(row=8, column=3, sticky=tk.W)
        tk.Label(master, text='Nm^3/h').grid(row=9, column=3, sticky=tk.W)
        tk.Label(master, text='kg/h').grid(row=10, column=3, sticky=tk.W)
        tk.Label(master, text='moles/s').grid(row=11, column=3, sticky=tk.W)
        tk.Label(master, text='J/(mol K)').grid(row=12, column=3, sticky=tk.W)
        tk.Label(master, text='Radians').grid(row=13, column=3, sticky=tk.W)
        tk.Label(master, text='m').grid(row=14, column=3, sticky=tk.W)

        self.radiobuttoncompositionValue = tk.IntVar()
        self.radiobuttoncompositionValue.set(1)
        tk.Radiobutton(self.theframe,
                    text = 'Water',
                    variable = self.radiobuttoncompositionValue,
                    value = streamcompositions['Water']).grid(padx = 3, pady = 2,
                                    row = 1, column = 5,
                                    sticky = tk.NW
                                    )
        tk.Radiobutton(self.theframe,
                    text = "Air",
                    variable = self.radiobuttoncompositionValue,
                    value = streamcompositions['Air']).grid(padx = 3, pady = 2,
                                    row = 2, column = 5,
                                    sticky = tk.NW
                                    )

        self.radiobuttonflowinputValue = tk.IntVar()
        self.radiobuttonflowinputValue.set(1)
        tk.Radiobutton(self.theframe,
                    text = 'Mass flow',
                    variable = self.radiobuttonflowinputValue,
                    value = flowinputtypes['Mass flow']).grid(padx = 3, pady = 2,
                                    row = 4, column = 5,
                                    sticky = tk.NW
                                    )
        tk.Radiobutton(self.theframe,
                    text = "Standard flow",
                    variable = self.radiobuttonflowinputValue,
                    value = flowinputtypes['Standard flow']).grid(padx = 3, pady = 2,
                                    row = 5, column = 5,
                                    sticky = tk.NW
                                    )

        self.flashbutton = tk.Button(self.theframe,
                             text = "NoFlash", command = self.noflashbutton)
        self.flashbutton.grid(row = 15, column = 5, pady = 2, padx = 3, sticky = tk.NW)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        #self.e0.set(self.thevalve.name)
        #self.theframe.itemconfig(self.e0, textvariable='red')
        #self.e0.insert(0, 'default text')
        self.e0text.set(self.thestream.name)
        self.e1text.set(str(utilities.pascal2barg(self.thestream.mat.P.v)))
        self.e2text.set(str(utilities.kelvin2celcius(self.thestream.mat.T.v)))
        self.e3text.set(str(self.thestream.mat.relativehumidity.v))
        self.e4text.set(str(self.thestream.mat.V.v))
        self.e5text.set(str(self.thestream.mat.f.v))
        self.e6text.set(str(self.thestream.mat.density.v))
        self.e7text.set(str(self.thestream.mat.massofonemole))
        self.e8text.set(str(utilities.fps2fph(self.thestream.actualvolumeflow.v)))
        self.e9text.set(str(utilities.fps2fph(self.thestream.standardvolumeflow.v)))
        self.e10text.set(str(utilities.fps2fph(self.thestream.massflow.v)))
        self.e11text.set(str(self.thestream.molarflow.v))
        self.e12text.set(str(self.thestream.mat.totalCp))
        self.e13text.set(str(self.thestream.direction))
        self.e14text.set(str(self.thestream.distance))

        if self.thestream.mat.composition[1].molefraction == 1.0:
            self.radiobuttoncompositionValue.set(streamcompositions['Air'])


    def validate(self):
        try:
            if self.radiobuttonflowinputValue.get() == flowinputtypes['Mass flow']:
                self.thestream.massflow.v = utilities.fph2fps(float(self.e10.get()))
            else:
                self.thestream.standardvolumeflow.v = utilities.fph2fps(float(self.e9.get()))
                #//thestream.calcmassflowfromstandardflow();
            if self.radiobuttoncompositionValue.get() == streamcompositions['Water']:
                self.thestream.mat.composition[1].molefraction = 0.0
                self.thestream.mat.composition[10].molefraction = 1.0
            else: #this is the case for Air
                self.thestream.mat.composition[1].molefraction = 1.0
                self.thestream.mat.composition[10].molefraction = 0.0

            #for (int i = 0; i < dataGridView1.Rows.Count; i++)
            #    thestream.mat.composition[i].molefraction = Convert.ToDouble(dataGridView1.Rows[i].Cells[1].Value)

            self.thestream.name = self.e0.get()
            self.thestream.mat.P.v = utilities.barg2pascal(float(self.e1.get()))
            self.thestream.mat.T.v = utilities.celcius2kelvin(float(self.e2.get()))
            self.thestream.mat.relativehumidity.v = float(self.e3.get())
            self.thestream.mat.V.v = float(self.e4.get())
            self.thestream.mat.f.v = float(self.e5.get())

        except ValueError:
            print("That's not a number!")
            return 0

        return 1


    def updatethestreamwithflash(self):
        #readthedialogue()
        #//List<component> inputcomposition = new List<component>()
        #//material.copycompositiontothiscomposition(ref inputcomposition, global.fluidpackage)

        self.thestream.mat.PTfVflash(self.thestream.mat.T.v, self.thestream.mat.V.v,
            self.thestream.mat.P.v, self.thestream.mat.f.v)
        #//thestream.update(thesim.simi)
        self.thestream.calcmolarflowfrommassflow()
        self.thestream.calcactualvolumeflowfrommassflow()
        self.thestream.calcstandardflowfrommoleflow()


    def updatethestreamwithnoflash(self): #//reads various fields manually without flashing
        #readthedialogue();
        try:
            self.thestream.mat.density.v = float(self.e6.get())
            self.thestream.mat.massofonemole = float(self.e7.get())
            self.thestream.mat.totalCp = float(self.e12.get())
        except ValueError:
            print("That's not a number!")
            return

        self.thestream.calcmolarflowfrommassflow()
        self.thestream.calcactualvolumeflowfrommassflow()
        self.thestream.calcstandardflowfrommoleflow()


    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.updatethestreamwithflash()
        self.refreshdialogue()

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()


    def update(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.updatethestreamwithflash()
        self.refreshdialogue()

        self.apply()


    def noflashbutton(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.updatethestreamwithnoflash()
        self.refreshdialogue()
