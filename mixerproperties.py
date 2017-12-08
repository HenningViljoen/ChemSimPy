from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities
import globe as globe


class mixerproperties(Dialog):
    def __init__(self, amixer, asim, aroot):
        self.themixer = amixer
        self.thesim = asim
        self.mixerlist = list()   #new List<unitop>();
        
        super(mixerproperties, self).__init__(aroot)

        self.refreshdialogue()


    def body(self, master):
        self.title('Mixer properties: ' + self.themixer.name)

        tk.Label(master, text='Nr inputs').grid(row=0, sticky=tk.W)

        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text)
        
        self.e0.grid(row=0, column=1)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        self.e0text.set(str(self.themixer.nin))


    def validate(self):
        try:
            anin = int(self.e0.get()) #local int
            if (self.themixer.nin != anin):
                self.themixer.nin = anin
                self.themixer.initinpoint()
                self.themixer.initinflow()

        except ValueError:
            print("That's not a number!")
            return 0

        return 1

