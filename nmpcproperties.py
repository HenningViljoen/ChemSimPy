from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities
import globe as globe


class nmpcproperties(Dialog):
    def __init__(self, anmpc, asim, aroot):
        self.selectedbaseclasspv = 0 #a bunch of local ints to follow
        self.selectedbaseclassop = 0
        self.selectedpv = 0
        self.selectedcv = 0
        self.selectedmv = 0
        self.selectedop = 0
        self.selectedboolmv = 0
        self.baseclasstypepv = globe.baseclasstypeenum.UnitOp
        self.baseclasstypeop = globe.baseclasstypeenum.UnitOp
        self.thenmpc = anmpc
        self.thesim = asim
        
        super(nmpcproperties, self).__init__(aroot)

        #self.refreshdialogue()


    def body(self, master):
        self.title('NMPC Controller Properties: ' + self.thenmpc.name)

        tk.Label(master, text='Name').grid(row=0, sticky=tk.W)
        tk.Label(master, text='N').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Initial delay').grid(row=2, sticky=tk.W)
        tk.Label(master, text='Run interval').grid(row=3, sticky=tk.W)
        tk.Label(master, text='alpha k').grid(row=4, sticky=tk.W)

        
        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text)
        self.e0.grid(row=0, column=1)
        self.e1text = tk.StringVar()
        self.e1 = tk.Entry(master, textvariable=self.e1text)
        self.e1.grid(row=1, column=1)
        self.e2text = tk.StringVar()
        self.e2 = tk.Entry(master, textvariable=self.e2text)
        self.e2.grid(row=2, column=1)
        self.e3text = tk.StringVar()
        self.e3 = tk.Entry(master, textvariable=self.e3text)
        self.e3.grid(row=3, column=1)
        self.e4text = tk.StringVar()
        self.e4 = tk.Entry(master, textvariable=self.e4text)
        self.e4.grid(row=4, column=1)

        tk.Label(master, text='Iterations').grid(row=1, column=2, sticky=tk.W)
        tk.Label(master, text='Iterations').grid(row=2, column=2, sticky=tk.W)
        tk.Label(master, text='Iterations').grid(row=3, column=2, sticky=tk.W)
        
        
        tk.Label(master, text='CV Object').grid(row=5, column=0, sticky=tk.W)
        tk.Label(master, text='CV Property').grid(row=5, column=1, sticky=tk.W)
        tk.Label(master, text='CV List').grid(row=5, column=2, sticky=tk.W)
        tk.Label(master, text='CV Target').grid(row=5, column=3, sticky=tk.W)
        tk.Label(master, text='CV Weight').grid(row=5, column=4, sticky=tk.W)
        tk.Label(master, text='CV EU low').grid(row=5, column=5, sticky=tk.W)
        tk.Label(master, text='CV EU high').grid(row=5, column=6, sticky=tk.W)
        tk.Label(master, text='CV target source').grid(row=5, column=7, sticky=tk.W)
        tk.Label(master, text='MV Object').grid(row=5, column=8, sticky=tk.W)
        tk.Label(master, text='MV Property').grid(row=5, column=9, sticky=tk.W)
        tk.Label(master, text='MV List (cont)').grid(row=5, column=10, sticky=tk.W)
        tk.Label(master, text='MV Min').grid(row=5, column=11, sticky=tk.W)
        tk.Label(master, text='MV Max').grid(row=5, column=12, sticky=tk.W)

        self.listbox0 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox0.grid(row=6, column=0)
        self.listbox1 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox1.grid(row=6, column=1)
        self.listbox2 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox2.grid(row=6, column=2)
        self.listbox3 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox3.grid(row=6, column=3)
        self.listbox4 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox4.grid(row=6, column=4)
        self.listbox5 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox5.grid(row=6, column=5)
        self.listbox6 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox6.grid(row=6, column=6)
        self.listbox7 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox7.grid(row=6, column=7)
        self.listbox8 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox8.grid(row=6, column=8)
        self.listbox9 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox9.grid(row=6, column=9)
        self.listbox10 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox10.grid(row=6, column=10)
        self.listbox11 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox11.grid(row=6, column=11)
        self.listbox12 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB)
        self.listbox12.grid(row=6, column=12)

        self.addcvbutton = tk.Button(self.theframe,
                             text = 'Add CV', command = self.addcvbuttonevent)
        self.addcvbutton.grid(row = 7, column = 2, pady = 2, padx = 3, sticky = tk.NW)

        self.deletecvbutton = tk.Button(self.theframe,
                             text = 'Delete CV', command = self.deletecvbuttonevent)
        self.deletecvbutton.grid(row = 7, column = 3, pady = 2, padx = 3, sticky = tk.NW)

        self.selectfilebutton = tk.Button(self.theframe,
                             text = 'File CV target', command = self.selectfilebuttonevent)
        self.selectfilebutton.grid(row = 7, column = 4, pady = 2, padx = 3, sticky = tk.NW)

        tk.Label(master, text='Current value').grid(row=8, column=1, sticky=tk.W)
        tk.Label(master, text='Min').grid(row=9, column=1, sticky=tk.W)
        tk.Label(master, text='Max').grid(row=10, column=1, sticky=tk.W)

        self.e5text = tk.StringVar()
        self.e5 = tk.Entry(master, textvariable=self.e5text)
        self.e5.grid(row=8, column=2)
        self.e6text = tk.StringVar()
        self.e6 = tk.Entry(master, textvariable=self.e6text)
        self.e6.grid(row=9, column=2)
        self.e7text = tk.StringVar()
        self.e7 = tk.Entry(master, textvariable=self.e7text)
        self.e7.grid(row=10, column=2)

        tk.Label(master, text='Target value').grid(row=8, column=3, sticky=tk.W)
        tk.Label(master, text='Weight').grid(row=9, column=3, sticky=tk.W)
        tk.Label(master, text='Min').grid(row=10, column=3, sticky=tk.W)
        tk.Label(master, text='Max').grid(row=11, column=3, sticky=tk.W)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        #self.e0.set(self.thevalve.name)
        #self.theframe.itemconfig(self.e0, textvariable='red')
        #self.e0.insert(0, 'default text')
        self.e0text.set(str(self.thetee.nout))

        self.mixerlist = []
        self.listbox.delete(0, tk.END)
        linkedmixerindex = -1
        j = 0 #int local
        for i in range(len(self.thesim.unitops)):
            if (self.thesim.unitops[i].objecttype == globe.objecttypes.Mixer):
                self.mixerlist.append(self.thesim.unitops[i])
                self.listbox.insert(tk.END, self.thesim.unitops[i].name)
                if self.thetee.linkedmixer == self.thesim.unitops[i]:
                    self.listbox.activate(j)
                    linkedmixerindex = j
                j += 1

        if linkedmixerindex >= 0: self.e1text.set(str(linkedmixerindex))


    def validate(self):
        try:
            anout = int(self.e0.get()) #local int
            if (self.thetee.nout != anout):
                self.thetee.nout = anout
                self.thetee.initoutpoint()
                self.thetee.initinflow()
                self.thetee.initoutflow()
                self.thetee.initk()
                self.thetee.initbranchflows()
                self.thetee.initbranchdp()

            selectedindextuple = self.listbox.curselection()
            if len(selectedindextuple) > 0:
                selectedi = selectedindextuple[0]
                self.thetee.linkedmixer = self.mixerlist[selectedi]

        except ValueError:
            print("That's not a number!")
            return 0

        self.refreshdialogue()
        return 1


    def addcvbuttonevent(self, event=None):
        pass


    def deletecvbuttonevent(self, event=None):
        pass


    def selectfilebuttonevent(self, event=None):
        pass

