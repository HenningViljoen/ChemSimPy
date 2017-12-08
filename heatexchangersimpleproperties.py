from tkSimpleDialog import Dialog
import tkinter as tk
import utilities as utilities

class heatexchangersimpleproperties(Dialog):
    def __init__(self, aheatexchangersimple, asim, aroot):
        self.theheatexchangersimple = aheatexchangersimple
        self.thesim = asim
        
        super(heatexchangersimpleproperties, self).__init__(aroot)

        self.refreshdialogue()
        #if (thevalve.inflow[0] != null) { listView1.Items.Add(thevalve.inflow[0].nr.ToString()); }
        #if (thevalve.outflow[0] != null) { listView2.Items.Add(thevalve.outflow[0].nr.ToString()); }


    def body(self, master):
        self.title('HeatexchangerSimple Properties: ' + str(self.theheatexchangersimple.nr))

        tk.Label(master, text='Name').grid(row=0, sticky=tk.W)
        tk.Label(master, text='HX U').grid(row=1, sticky=tk.W)
        tk.Label(master, text='HX A').grid(row=2, sticky=tk.W)

        self.e0text = tk.StringVar()
        self.e0 = tk.Entry(master, textvariable=self.e0text)
        self.e1text = tk.StringVar()
        self.e1 = tk.Entry(master, textvariable=self.e1text)
        self.e2text = tk.StringVar()
        self.e2 = tk.Entry(master, textvariable=self.e2text)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)

        tk.Label(master, text='W/(m^2*K)').grid(row=1, column=3, sticky=tk.W)
        tk.Label(master, text='m^2').grid(row=2, column=3, sticky=tk.W)

        tk.Label(master, text='Strm 1 flow coef').grid(row=0, column=4, sticky=tk.W)
        tk.Label(master, text='Strm 1 temp tau').grid(row=1, column=4, sticky=tk.W)
        tk.Label(master, text='Strm 1 flow tau').grid(row=2, column=4, sticky=tk.W)
        
        self.e3text = tk.StringVar()
        self.e3 = tk.Entry(master, textvariable=self.e3text)
        self.e4text = tk.StringVar()
        self.e4 = tk.Entry(master, textvariable=self.e4text)
        self.e5text = tk.StringVar()
        self.e5 = tk.Entry(master, textvariable=self.e5text)

        self.e3.grid(row=0, column=5)
        self.e4.grid(row=1, column=5)
        self.e5.grid(row=2, column=5)

        tk.Label(master, text='sec').grid(row=1, column=6, sticky=tk.W)
        tk.Label(master, text='sec').grid(row=2, column=6, sticky=tk.W)

        tk.Label(master, text='Strm 2 flow coef').grid(row=0, column=7, sticky=tk.W)
        tk.Label(master, text='Strm 2 temp tau').grid(row=1, column=7, sticky=tk.W)
        tk.Label(master, text='Strm 2 flow tau').grid(row=2, column=7, sticky=tk.W)

        self.e6text = tk.StringVar()
        self.e6 = tk.Entry(master, textvariable=self.e6text)
        self.e7text = tk.StringVar()
        self.e7 = tk.Entry(master, textvariable=self.e7text)
        self.e8text = tk.StringVar()
        self.e8 = tk.Entry(master, textvariable=self.e8text)

        self.e6.grid(row=0, column=8)
        self.e7.grid(row=1, column=8)
        self.e8.grid(row=2, column=8)

        tk.Label(master, text='sec').grid(row=1, column=9, sticky=tk.W)
        tk.Label(master, text='sec').grid(row=2, column=9, sticky=tk.W)

        return self.e0 # initial focus

    
    def refreshdialogue(self):
        #self.e0.set(self.thevalve.name)
        #self.theframe.itemconfig(self.e0, textvariable='red')
        #self.e0.insert(0, 'default text')
        self.e0text.set(self.theheatexchangersimple.name)
        self.e1text.set(str(self.theheatexchangersimple.U.v))
        self.e2text.set(str(self.theheatexchangersimple.A.v))
        self.e3text.set(str(self.theheatexchangersimple.strm1flowcoefficient))
        self.e4text.set(str(self.theheatexchangersimple.strm1temptau.v))
        self.e5text.set(str(self.theheatexchangersimple.strm1flowtau))
        self.e6text.set(str(self.theheatexchangersimple.strm2flowcoefficient.v))
        self.e7text.set(str(self.theheatexchangersimple.strm2temptau.v))
        self.e8text.set(str(self.theheatexchangersimple.strm2flowtau))


    def validate(self):
        try:
            self.theheatexchangersimple.name = self.e0.get()
            self.theheatexchangersimple.U.v = float(self.e1.get())
            self.theheatexchangersimple.A.v = float(self.e2.get())

            self.theheatexchangersimple.strm1flowcoefficient = float(self.e3.get())
            self.theheatexchangersimple.strm1temptau.v = float(self.e4.get())
            self.theheatexchangersimple.strm1flowtau = float(self.e5.get())

            self.theheatexchangersimple.strm2flowcoefficient.v = float(self.e6.get())
            self.theheatexchangersimple.strm2temptau.v = float(self.e7.get())
            self.theheatexchangersimple.strm2flowtau = float(self.e8.get())
        except ValueError:
            print("That's not an int!")
            return 0

        return 1


    #def apply(self):
    #    first = int(self.e1.get())
    #    second = int(self.e2.get())
        #print first, second # or something