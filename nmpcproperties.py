from tkSimpleDialog import Dialog
from mpcvar import mpcvar
from controlvar import controlvar
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

        self.refreshdialogue()


    def body(self, master):
        self.title('NMPC Controller Properties: ' + self.thenmpc.name)

        tk.Label(master, text='Name').grid(row=0, sticky=tk.W)
        tk.Label(master, text='N').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Initial delay').grid(row=2, sticky=tk.W)
        tk.Label(master, text='Run interval').grid(row=3, sticky=tk.W)
        tk.Label(master, text='alpha k').grid(row=4, sticky=tk.W)

        
        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text, width=globe.MeanWidthNMPCGUIEntry)
        self.e0.grid(row=0, column=1)
        self.e1text = tk.StringVar()
        self.e1 = tk.Entry(master, textvariable=self.e1text, width=globe.MeanWidthNMPCGUIEntry)
        self.e1.grid(row=1, column=1)
        self.e2text = tk.StringVar()
        self.e2 = tk.Entry(master, textvariable=self.e2text, width=globe.MeanWidthNMPCGUIEntry)
        self.e2.grid(row=2, column=1)
        self.e3text = tk.StringVar()
        self.e3 = tk.Entry(master, textvariable=self.e3text, width=globe.MeanWidthNMPCGUIEntry)
        self.e3.grid(row=3, column=1)
        self.e4text = tk.StringVar()
        self.e4 = tk.Entry(master, textvariable=self.e4text, width=globe.MeanWidthNMPCGUIEntry)
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
        tk.Label(master, text='MV List (c)').grid(row=5, column=10, sticky=tk.W)
        tk.Label(master, text='MV Min').grid(row=5, column=11, sticky=tk.W)
        tk.Label(master, text='MV Max').grid(row=5, column=12, sticky=tk.W)

        self.listbox0 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox0.grid(row=6, column=0)
        self.listbox0.bind('<<ListboxSelect>>', self.listbox0select)
        self.listbox1 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox1.grid(row=6, column=1)
        self.listbox1.bind('<<ListboxSelect>>', self.listbox1select)
        self.listbox2 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox2.grid(row=6, column=2)
        self.listbox2.bind('<<ListboxSelect>>', self.listbox2select)
        self.listbox3 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox3.grid(row=6, column=3)
        self.listbox4 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox4.grid(row=6, column=4)
        self.listbox5 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox5.grid(row=6, column=5)
        self.listbox6 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox6.grid(row=6, column=6)
        self.listbox7 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox7.grid(row=6, column=7)
        self.listbox8 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox8.grid(row=6, column=8)
        self.listbox8.bind('<<ListboxSelect>>', self.listbox8select)
        self.listbox9 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox9.grid(row=6, column=9)
        self.listbox10 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox10.grid(row=6, column=10)
        self.listbox10.bind('<<ListboxSelect>>', self.listbox10select)
        self.listbox11 = tk.Listbox(master, width=5, exportselection=False)
        self.listbox11.grid(row=6, column=11)
        self.listbox12 = tk.Listbox(master, width=5, exportselection=False)
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
        self.e5 = tk.Entry(master, textvariable=self.e5text, width=globe.MeanWidthNMPCGUIEntry)
        self.e5.grid(row=8, column=2)
        self.e6text = tk.StringVar()
        self.e6 = tk.Entry(master, textvariable=self.e6text, width=globe.MeanWidthNMPCGUIEntry)
        self.e6.grid(row=9, column=2)
        self.e7text = tk.StringVar()
        self.e7 = tk.Entry(master, textvariable=self.e7text, width=globe.MeanWidthNMPCGUIEntry)
        self.e7.grid(row=10, column=2)

        tk.Label(master, text='Target value').grid(row=8, column=3, sticky=tk.W)
        tk.Label(master, text='Weight').grid(row=9, column=3, sticky=tk.W)
        tk.Label(master, text='Min').grid(row=10, column=3, sticky=tk.W)
        tk.Label(master, text='Max').grid(row=11, column=3, sticky=tk.W)

        self.e8text = tk.StringVar()
        self.e8 = tk.Entry(master, textvariable=self.e8text, width=globe.MeanWidthNMPCGUIEntry)
        self.e8.grid(row=8, column=4)
        self.e9text = tk.StringVar()
        self.e9 = tk.Entry(master, textvariable=self.e9text, width=globe.MeanWidthNMPCGUIEntry)
        self.e9.grid(row=9, column=4)
        self.e10text = tk.StringVar()
        self.e10 = tk.Entry(master, textvariable=self.e10text, width=globe.MeanWidthNMPCGUIEntry)
        self.e10.grid(row=10, column=4)
        self.e11text = tk.StringVar()
        self.e11 = tk.Entry(master, textvariable=self.e11text, width=globe.MeanWidthNMPCGUIEntry)
        self.e11.grid(row=11, column=4)

        self.addmvcontbutton = tk.Button(self.theframe,
                             text = 'Add MV(c)', command = self.addmvcontbuttonevent)
        self.addmvcontbutton.grid(row = 7, column = 10, pady = 2, padx = 3, sticky = tk.NW)

        self.deletemvcontbutton = tk.Button(self.theframe,
                             text = 'Delete MV(c)', command = self.deletemvcontbuttonevent)
        self.deletemvcontbutton.grid(row = 7, column = 11, pady = 2, padx = 3, sticky = tk.NW)

        tk.Label(master, text='Current value').grid(row=8, column=10, sticky=tk.W)
        tk.Label(master, text='Min').grid(row=9, column=10, sticky=tk.W)
        tk.Label(master, text='Max').grid(row=10, column=10, sticky=tk.W)

        self.e12text = tk.StringVar()
        self.e12 = tk.Entry(master, textvariable=self.e12text, width=globe.MeanWidthNMPCGUIEntry)
        self.e12.grid(row=8, column=11)
        self.e13text = tk.StringVar()
        self.e13 = tk.Entry(master, textvariable=self.e13text, width=globe.MeanWidthNMPCGUIEntry)
        self.e13.grid(row=9, column=11)
        self.e14text = tk.StringVar()
        self.e14 = tk.Entry(master, textvariable=self.e14text, width=globe.MeanWidthNMPCGUIEntry)
        self.e14.grid(row=10, column=11)

        tk.Label(master, text='MV List (h)').grid(row=11, column=10, sticky=tk.W)
        tk.Label(master, text='MV Min').grid(row=11, column=11, sticky=tk.W)
        tk.Label(master, text='MV Max').grid(row=11, column=12, sticky=tk.W)

        self.listbox13 = tk.Listbox(master, width=globe.MeanWidthNMPCGUILB, exportselection=False)
        self.listbox13.grid(row=12, column=10)
        self.listbox13.bind('<<ListboxSelect>>', self.listbox13select)
        self.listbox14 = tk.Listbox(master, width=5, exportselection=False)
        self.listbox14.grid(row=12, column=11)
        self.listbox15 = tk.Listbox(master, width=5, exportselection=False)
        self.listbox15.grid(row=12, column=12)

        self.addmvhybbutton = tk.Button(self.theframe,
                             text = 'Add MV(h)', command = self.addmvhybbuttonevent)
        self.addmvhybbutton.grid(row = 13, column = 10, pady = 2, padx = 3, sticky = tk.NW)

        self.deletemvhybbutton = tk.Button(self.theframe,
                             text = 'Delete MV(h)', command = self.deletemvhybbuttonevent)
        self.deletemvhybbutton.grid(row = 13, column = 11, pady = 2, padx = 3, sticky = tk.NW)

        tk.Label(master, text='Current value').grid(row=14, column=10, sticky=tk.W)
        tk.Label(master, text='Min').grid(row=15, column=10, sticky=tk.W)
        tk.Label(master, text='Max').grid(row=16, column=10, sticky=tk.W)

        self.e15text = tk.StringVar()
        self.e15 = tk.Entry(master, textvariable=self.e15text, width=globe.MeanWidthNMPCGUIEntry)
        self.e15.grid(row=14, column=11)
        self.e16text = tk.StringVar()
        self.e16 = tk.Entry(master, textvariable=self.e16text, width=globe.MeanWidthNMPCGUIEntry)
        self.e16.grid(row=15, column=11)
        self.e17text = tk.StringVar()
        self.e17 = tk.Entry(master, textvariable=self.e17text, width=globe.MeanWidthNMPCGUIEntry)
        self.e17.grid(row=16, column=11)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        self.refreshmaindialogue()

        self.refreshbaseclasslistpv()
        self.refreshpropertylistdialoguepv()
        self.refreshcvlist()
        self.refreshbaseclasslistop()
        self.refreshpropertylistdialogueop()
        self.refreshmvlist()


    def refreshmaindialogue(self):
        self.e1text.set(str(self.thenmpc.N))
        self.e2text.set(str(self.thenmpc.initialdelay))
        self.e3text.set(str(self.thenmpc.runinterval))
        self.e4text.set(str(self.thenmpc.alphak))

        if self.baseclasstypepv == globe.baseclasstypeenum.UnitOp:
            self.e5text.set(str(self.thesim.unitops[self.selectedbaseclasspv].selectedproperty(self.selectedpv).v))
        elif self.baseclasstypepv == globe.baseclasstypeenum.Stream:
            self.e5text.set(str(self.thesim.streams[self.selectedbaseclasspv - \
                len(self.thesim.unitops)].selectedproperty(self.selectedpv).v))
        else:
            pass

        if (len(self.thenmpc.cvmaster) > 0):
            self.e8text.set(str(self.thenmpc.cvmaster[self.selectedcv].target.v))
            self.e9text.set(str(self.thenmpc.cvmaster[self.selectedcv].weight))
            self.e10text.set(str(self.thenmpc.cvmaster[self.selectedcv].min))
            self.e11text.set(str(self.thenmpc.cvmaster[self.selectedcv].max))
        else:
            self.e8text.set('')
            self.e9text.set('')
            self.e10text.set('')
            self.e11text.set('')

        if (len(self.thenmpc.mvmaster) > 0):
            self.e12text.set(str(self.thenmpc.mvmaster[self.selectedmv].var.v))
            self.e13text.set(str(self.thenmpc.mvmaster[self.selectedmv].min))
            self.e14text.set(str(self.thenmpc.mvmaster[self.selectedmv].max))
        else:
            self.e12text.set('')
            self.e13text.set('')
            self.e14text.set('')

        if (len(self.thenmpc.mvboolmaster) > 0):
            self.e15text.set(str(self.thenmpc.mvboolmaster[self.selectedboolmv].var.v))
            self.e16text.set(str(self.thenmpc.mvboolmaster[self.selectedboolmv].min))
            self.e17text.set(str(self.thenmpc.mvboolmaster[self.selectedboolmv].max))
        else:
            self.e15text.set('')
            self.e15text.set('')
            self.e15text.set('')


    def refreshbaseclasslistpv(self):
        for i in range(len(self.thesim.unitops)):
            self.listbox0.insert(tk.END, self.thesim.unitops[i].name)
        for i in range(len(self.thesim.streams)):
            self.listbox0.insert(tk.END, self.thesim.streams[i].name)


    def refreshpropertylistdialoguepv(self):
        self.listbox1.delete(0, tk.END)
        if self.baseclasstypepv == globe.baseclasstypeenum.UnitOp:
            for i in range(len(self.thesim.unitops[self.selectedbaseclasspv].controlproperties)):
                self.listbox1.insert(tk.END, self.thesim.unitops[self.selectedbaseclasspv].controlproperties[i])
        elif self.baseclasstypepv == globe.baseclasstypeenum.Stream:
            for i in range(len(self.thesim.streams[self.selectedbaseclasspv - len(self.thesim.unitops)].controlproperties)):
                self.listbox1.insert(tk.END, \
                    self.thesim.streams[self.selectedbaseclasspv - len(self.thesim.unitops)].controlproperties[i])
        else:
            pass


    def refreshcvlist(self):
        self.listbox2.delete(0, tk.END)
        self.listbox3.delete(0, tk.END)
        self.listbox4.delete(0, tk.END)
        self.listbox5.delete(0, tk.END)
        self.listbox6.delete(0, tk.END)
        self.listbox7.delete(0, tk.END)
        for i in range(len(self.thenmpc.cvmaster)):
            self.listbox2.insert(tk.END, self.thenmpc.cvmaster[i].name)
            self.listbox3.insert(tk.END, str(self.thenmpc.cvmaster[i].target.v))
            self.listbox4.insert(tk.END, str(self.thenmpc.cvmaster[i].weight))
            self.listbox5.insert(tk.END, str(self.thenmpc.cvmaster[i].min))
            self.listbox6.insert(tk.END, str(self.thenmpc.cvmaster[i].max))
            if self.thenmpc.cvmaster[i].target.datasource == globe.datasourceforvar.Simulation:
                self.listbox7.insert(tk.END, str(self.thenmpc.cvmaster[i].target.datasource))
            else:
                self.listbox7.insert(tk.END, self.thenmpc.cvmaster[i].target.excelsource.filename)
        if len(self.thenmpc.cvmaster) > 0:
            if (self.selectedcv >= len(self.thenmpc.cvmaster)):
                self.selectedcv = len(self.thenmpc.cvmaster) - 1
            self.listbox3.activate(self.selectedcv)


    def refreshbaseclasslistop(self):
        for i in range(len(self.thesim.unitops)):
            self.listbox8.insert(tk.END, self.thesim.unitops[i].name)
        for i in range(len(self.thesim.streams)):
            self.listbox8.insert(tk.END, self.thesim.streams[i].name)
        for i in range(len(self.thesim.blocks)):
            self.listbox8.insert(tk.END, self.thesim.blocks[i].name)


    def refreshpropertylistdialogueop(self):
        self.listbox9.delete(0, tk.END)
        if self.baseclasstypeop == globe.baseclasstypeenum.UnitOp:
            for i in range(len(self.thesim.unitops[self.selectedbaseclassop].controlproperties)):
                self.listbox9.insert(tk.END, self.thesim.unitops[self.selectedbaseclassop].controlproperties[i])
        elif self.baseclasstypeop == globe.baseclasstypeenum.Stream:
            for i in range(len(self.thesim.streams[self.selectedbaseclassop - len(self.thesim.unitops)].controlproperties)):
                self.listbox9.insert(tk.END, self.thesim.streams[self.selectedbaseclassop - \
                    len(self.thesim.unitops)].controlproperties[i])
        elif self.baseclasstypeop == globe.baseclasstypeenum.Block:
            for i in range(len(self.thesim.blocks[self.selectedbaseclassop - len(self.thesim.unitops) - len(self.thesim.streams)].controlproperties)):
                self.listbox9.insert(tk.END, thesim.blocks[self.selectedbaseclassop - len(self.thesim.unitops) - \
                    len(self.thesim.streams)].controlproperties[i])
        else:
            pass


    def refreshmvlist(self):
        self.listbox10.delete(0, tk.END)
        self.listbox11.delete(0, tk.END)
        self.listbox12.delete(0, tk.END)
        for i in range(len(self.thenmpc.mvmaster)):
            self.listbox10.insert(tk.END, self.thenmpc.mvmaster[i].name)
            self.listbox11.insert(tk.END, self.thenmpc.mvmaster[i].min)
            self.listbox12.insert(tk.END, self.thenmpc.mvmaster[i].max)
        if len(self.thenmpc.mvmaster) > 0:
            if self.selectedmv >= len(self.thenmpc.mvmaster):
                self.selectedmv = len(self.thenmpc.mvmaster) - 1
            self.listbox10.activate(self.selectedmv)

        self.listbox13.delete(0, tk.END)
        self.listbox14.delete(0, tk.END)
        self.listbox15.delete(0, tk.END)
        for i in range(len(self.thenmpc.mvboolmaster)):
            self.listbox13.insert(tk.END, self.thenmpc.mvboolmaster[i].name)
            self.listbox14.insert(tk.END, self.thenmpc.mvboolmaster[i].min)
            self.listbox15.insert(tk.END, self.thenmpc.mvboolmaster[i].max)
        if len(self.thenmpc.mvboolmaster) > 0:
            if self.selectedboolmv >= len(self.thenmpc.mvboolmaster):
                self.selectedboolmv = len(self.thenmpc.mvboolmaster) - 1
            self.listbox13.activate(self.selectedboolmv)


    def validate(self):
        try:
            self.thenmpc.N = int(self.e1.get())
            self.thenmpc.initialdelay = int(self.e2.get())
            self.thenmpc.runinterval = int(self.e3.get())
            self.thenmpc.alphak = float(self.e4.get())
            self.thenmpc.cvmaster[self.selectedcv].target.v = float(self.e8.get())
            if (self.thenmpc.cvmaster[self.selectedcv].target.datasource == globe.datasourceforvar.Simulation):
                for i in range(globe.SimIterations):
                    self.thenmpc.cvmaster[self.selectedcv].target.simvector[i] = \
                        self.thenmpc.cvmaster[self.selectedcv].target.v
            self.thenmpc.cvmaster[self.selectedcv].weight = float(self.e9.get())
            self.thenmpc.cvmaster[self.selectedcv].min = float(self.e10.get())
            self.thenmpc.cvmaster[self.selectedcv].max = float(self.e11.get())
            if len(self.thenmpc.mvmaster) > 0:
                self.thenmpc.mvmaster[self.selectedmv].min = float(self.e13.get())
                self.thenmpc.mvmaster[self.selectedmv].max = float(self.e14.get())
            if len(self.thenmpc.mvboolmaster) > 0:
                self.thenmpc.mvboolmaster[selectedboolmv].min = float(self.e16.get())
                self.thenmpc.mvboolmaster[selectedboolmv].max = float(self.e17.get())
            
        except ValueError:
            print("That's not a number!")
            return 0
        self.refreshcvlist()
        self.refreshmvlist()
        self.thenmpc.validatesettings()
        self.thenmpc.initjacobian()
        return 1


    def addcvbuttonevent(self, event=None):  #Click event for Add CV button
        aname = '' #local string
        self.selectedpv = self.listbox1.curselection()[0]
            
        if self.baseclasstypepv == globe.baseclasstypeenum.UnitOp:
            aname = self.thesim.unitops[self.selectedbaseclasspv].name + ": " + self.listbox1.get(self.selectedpv)
            newmpcvar = mpcvar(self.thenmpc.mastersim.unitops[self.selectedbaseclasspv].selectedproperty(self.selectedpv), \
                aname, 0.0, 1.0)
            #newmpcvar.copyfrom()
            self.thenmpc.cvmaster.append(newmpcvar)
        elif self.baseclasstypepv == globe.baseclasstypeenum.Stream:
            aname = self.thesim.streams[self.selectedbaseclasspv - len(self.thesim.unitops)].name + ": " + \
                self.listbox1.get(self.selectedpv)
            newmpcvar = mpcvar(self.thenmpc.mastersim.streams[self.selectedbaseclasspv - \
                len(self.thenmpc.sim1.unitops)].selectedproperty(self.selectedpv), aname, 0.0, 1.0)
            self.thenmpc.cvmaster.append(newmpcvar)
        else:
            pass
        self.thenmpc.cvmaster[-1].target.simvector = [0.0]*globe.SimIterations
        self.refreshcvlist()
        self.refreshmaindialogue()


    def deletecvbuttonevent(self, event=None):  #Click event handler for Delete button from CV list.
        self.selectedcv = self.listbox2.curselection()[0]
        if (self.selectedcv > -1):
            self.thenmpc.cvmaster.pop(self.selectedcv)
            self.refreshcvlist()
            self.refreshmaindialogue()


    def selectfilebuttonevent(self, event=None):
        pass


    def addmvcontbuttonevent(self, event=None): #Event handler for Click event of Add MV (continuous) button.
        streamnr = 0 #local int//The particular unitop/stream nr to be selected and loaded in mvmaster.
        theproperty = controlvar()#local controlvar #//to check if the particular MV is bool or not.
        self.selectedop = self.listbox9.curselection()[0]
        aname = '' #local string
        if self.baseclasstypeop == globe.baseclasstypeenum.UnitOp:
            #print(self.selectedbaseclassop)
            #print(self.selectedop)
            aname = self.thesim.unitops[self.selectedbaseclassop].name + ": " + self.listbox9.get(self.selectedop)
            #//thenmpc.mvsim0.Add(new mpcvar(thenmpc.sim0.unitops[selectedbaseclassop].selectedproperty(selectedop), 
            #//    aname, 0, 0));
            #//thenmpc.mvsim1.Add(new mpcvar(thenmpc.sim1.unitops[selectedbaseclassop].selectedproperty(selectedop),
            #//    aname, 0, 0));
            theproperty = self.thenmpc.mastersim.unitops[self.selectedbaseclassop].selectedproperty(self.selectedop)
            if not theproperty.isbool:
                self.thenmpc.mvmaster.append(mpcvar(self.thenmpc.mastersim.unitops[self.selectedbaseclassop].\
                    selectedproperty(self.selectedop), aname, 0, 0))
        elif self.baseclasstypeop == globe.baseclasstypeenum.Stream:
            aname = self.thesim.streams[self.selectedbaseclassop - len(self.thesim.unitops)].name + ": " + \
                        self.listbox9.get(self.selectedop)
            #//thenmpc.mvsim0.Add(new mpcvar(thenmpc.sim0.streams[selectedbaseclassop - 
            #//    thenmpc.sim0.unitops.Count].selectedproperty(selectedop), aname, 0, 0));
            #//thenmpc.mvsim1.Add(new mpcvar(thenmpc.sim1.streams[selectedbaseclassop -
            #//    thenmpc.sim1.unitops.Count].selectedproperty(selectedop), aname, 0, 0));
            streamnr = self.selectedbaseclassop - len(self.thenmpc.mastersim.unitops)
            theproperty = self.thenmpc.mastersim.streams[streamnr].selectedproperty(self.selectedop)
            if not theproperty.isbool:
                self.thenmpc.mvmaster.append(mpcvar(self.thenmpc.mastersim.streams[streamnr].\
                    selectedproperty(self.selectedop), aname, 0, 0))
        elif self.baseclasstypeop == globe.baseclasstypeenum.Block:
            aname = self.thesim.blocks[self.selectedbaseclassop - len(self.thesim.unitops) - len(self.thesim.streams)].\
                name + ": " + self.listbox9.get(self.selectedop)
            streamnr = self.selectedbaseclassop - len(self.thenmpc.mastersim.unitops) - len(self.thenmpc.mastersim.streams)
            theproperty = self.thenmpc.mastersim.blocks[streamnr].selectedproperty(self.selectedop)
            if not theproperty.isbool:
                self.thenmpc.mvmaster.append(mpcvar(self.thenmpc.mastersim.blocks[streamnr].\
                    selectedproperty(self.selectedop), aname, 0, 0))
        else:
            pass
        self.refreshmvlist()
        self.refreshmaindialogue()


    def deletemvcontbuttonevent(self, event=None):  #Click event handler for Delete MV button
        self.selectedmv = self.listbox10.curselection()[0]
        if (self.selectedmv > -1):
            #//thenmpc.mvsim0.RemoveAt(selectedmv)
            self.thenmpc.mvmaster.pop(self.selectedmv)
            self.refreshmvlist()
            self.refreshmaindialogue()


    def addmvhybbuttonevent(self, event=None): #Click event for add MV (boolean/hybrid)
        streamnr = 0 #local int #//The particular unitop/stream nr to be selected and loaded in mvmaster.
        theproperty = controlvar()#local controlvar #//to check if the particular MV is bool or not.
        aname = '' #local string
        self.selectedop = self.listbox9.curselection()[0]
        if self.baseclasstypeop == globe.baseclasstypeenum.UnitOp:
            aname = self.thesim.unitops[self.selectedbaseclassop].name + ": " + self.listbox9.get(self.selectedop)
            theproperty = self.thenmpc.mastersim.unitops[self.selectedbaseclassop].selectedproperty(self.selectedop)
            if (theproperty.isbool):
                self.thenmpc.mvboolmaster.append(mpcvar(self.thenmpc.mastersim.unitops[self.selectedbaseclassop].\
                    selectedproperty(self.selectedop), aname, 0, 0, 0, 1))
        elif self.baseclasstypeop == globe.baseclasstypeenum.Stream:
            aname = self.thesim.streams[self.selectedbaseclassop - len(self.thesim.unitops)].name + ": " + \
                        self.listbox9.get(self.selectedop)
            streamnr = self.selectedbaseclassop - len(self.thenmpc.mastersim.unitops)
            theproperty = self.thenmpc.mastersim.streams[streamnr].selectedproperty(self.selectedop)
            if (theproperty.isbool):
                self.thenmpc.mvboolmaster.append(mpcvar(thenmpc.mastersim.streams[streamnr].\
                    selectedproperty(self.selectedop), aname, 0, 0, 0, 1))
        else:
            pass
        self.refreshmvlist()
        self.refreshmaindialogue()


    def deletemvhybbuttonevent(self, event=None): #click event for Delete MV (bool/hybrid) button.
        self.selectedboolmv = self.listbox13.curselection()[0]
        if (self.selectedboolmv > -1):
            self.thenmpc.mvboolmaster.pop(self.selectedboolmv)
            self.refreshmvlist()
            self.refreshmaindialogue()

    
    def listbox0select(self, event=None): #CV Object list selected index changed.
        self.selectedbaseclasspv = self.listbox0.curselection()[0]
        if self.selectedbaseclasspv < len(self.thesim.unitops):
            self.baseclasstypepv = globe.baseclasstypeenum.UnitOp
        else:
            self.baseclasstypepv = globe.baseclasstypeenum.Stream
        self.refreshpropertylistdialoguepv()


    def listbox1select(self, event=None): #SelecteedIndexChanged event handler for CV 
                                                                                #Property List.
        self.selectedpv = self.listbox1.curselection()[0]  
        self.refreshmaindialogue()


    def listbox2select(self, event=None):
        self.selectedcv = self.listbox2.curselection()[0]
        self.refreshmaindialogue()

    
    def listbox8select(self, event=None):  #//Event handler for SelectedIndexChanged event for Main Object List for OPs
        self.selectedbaseclassop = self.listbox8.curselection()[0]
        if self.selectedbaseclassop < len(self.thesim.unitops):
            self.baseclasstypeop = globe.baseclasstypeenum.UnitOp
        elif self.selectedbaseclassop < len(self.thesim.unitops) + len(self.thesim.streams):
            self.baseclasstypeop = globe.baseclasstypeenum.Stream
        else:
            self.baseclasstypeop = globe.baseclasstypeenum.Block
        self.refreshpropertylistdialogueop()


    def listbox10select(self, event=None): #Event handler for MV (continuous) List selected index changed event.
        self.selectedmv = self.listbox10.curselection()[0]
        self.refreshmaindialogue()

    
    def listbox13select(self, event=None): #event for selected index changed for mv (bool/hybrid) changed.
        self.selectedboolmv = self.listbox13.curselection()[0]
        self.refreshmaindialogue()

        
