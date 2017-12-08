from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities

class tankproperties(Dialog):
    def __init__(self, atank, asim, aroot):
        self.thetank = atank
        self.thesim = asim
        
        super(tankproperties, self).__init__(aroot)

        self.refreshdialogue()
        #if (thevalve.inflow[0] != null) { listView1.Items.Add(thevalve.inflow[0].nr.ToString()); }
        #if (thevalve.outflow[0] != null) { listView2.Items.Add(thevalve.outflow[0].nr.ToString()); }


    def body(self, master):
        self.title('Tank properties: Tank ' + str(self.thetank.nr))

        tk.Label(master, text='Maximum volume').grid(row=0, sticky=tk.W)
        tk.Label(master, text='Radius').grid(row=1, sticky=tk.W)
        tk.Label(master, text='Height').grid(row=2, sticky=tk.W)
        tk.Label(master, text='Mass inventory').grid(row=3, sticky=tk.W)
        tk.Label(master, text='Actual volume inventory').grid(row=4, sticky=tk.W)
        tk.Label(master, text='Fraction inventory').grid(row=5, sticky=tk.W)
        tk.Label(master, text='Inventory height').grid(row=6, sticky=tk.W)
        tk.Label(master, text='Pressure at bottom').grid(row=7, sticky=tk.W)

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

        tk.Label(master, text='m^3').grid(row=0, column=3, sticky=tk.W)
        tk.Label(master, text='m').grid(row=1, column=3, sticky=tk.W)
        tk.Label(master, text='m').grid(row=2, column=3, sticky=tk.W)
        tk.Label(master, text='kg').grid(row=3, column=3, sticky=tk.W)
        tk.Label(master, text='m^3').grid(row=4, column=3, sticky=tk.W)
        tk.Label(master, text='Fraction').grid(row=5, column=3, sticky=tk.W)
        tk.Label(master, text='m').grid(row=6, column=3, sticky=tk.W)
        tk.Label(master, text='barg').grid(row=7, column=3, sticky=tk.W)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        #self.e0.set(self.thevalve.name)
        #self.theframe.itemconfig(self.e0, textvariable='red')
        #self.e0.insert(0, 'default text')
        self.e0text.set(str(self.thetank.maxvolume))
        self.e1text.set(str(self.thetank.radius))
        self.e2text.set(str(self.thetank.height))
        self.e3text.set(str(self.thetank.massinventory.v))
        self.e4text.set(str(self.thetank.actualvolumeinventory.v))
        self.e5text.set(str(self.thetank.fracinventory.v))
        self.e6text.set(str(self.thetank.inventoryheight.v))
        self.e7text.set(str(utilities.pascal2barg(self.thetank.pressureatbottom)))

        #textBox1.Text = thetank.maxvolume.ToString("N");
        #textBox2.Text = thetank.radius.ToString("N");
        #textBox3.Text = thetank.height.ToString("N");
        #textBox4.Text = thetank.massinventory.ToString("N");
        #textBox8.Text = thetank.actualvolumeinventory.ToString("N");
        #textBox5.Text = thetank.fracinventory.ToString("N");
        #textBox6.Text = thetank.inventoryheight.ToString("N");
        #textBox7.Text = utilities.pascal2barg(thetank.pressureatbottom).ToString("N");


    def validate(self):
        try:
            self.thetank.radius = float(self.e1.get())
            self.thetank.height = float(self.e2.get())
            self.thetank.massinventory.v = float(self.e3.get())

        except ValueError:
            print("That's not a number!")
            return 0

        self.thetank.inventorycalcs()
        return 1


    #def apply(self):
    #    first = int(self.e1.get())
    #    second = int(self.e2.get())
        #print first, second # or something

