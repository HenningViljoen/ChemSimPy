from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities
import globe as globe


class teeproperties(Dialog):
    def __init__(self, atee, asim, aroot):
        self.thetee = atee
        self.thesim = asim
        self.mixerlist = list()   #new List<unitop>();
        
        super(teeproperties, self).__init__(aroot)

        self.refreshdialogue()


    def body(self, master):
        self.title('Tee properties: ' + self.thetee.name)

        tk.Label(master, text='Nr outputs').grid(row=0, sticky=tk.W)
        tk.Label(master, text='Mixer linked').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Linked mixer index').grid(row=2, sticky=tk.W)

        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text)
        
        self.e0.grid(row=0, column=1)
        
        self.listbox = tk.Listbox(master)
        self.listbox.grid(row=1, column=1)

        self.e1text = tk.StringVar()
        self.e1 = tk.Entry(master, textvariable=self.e1text)
        
        self.e1.grid(row=2, column=1)

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




