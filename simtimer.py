import globe as globe
import math


class simtimer(object):
    def __init__(self, adays, ahours, aminutes, aseconds):
            #(double adays, double ahours, double aminutes, double aseconds)
        self.days = adays
        self.hours = ahours
        self.minutes = aminutes
        self.seconds = aseconds
        self.totalseconds = 0


    def reset(self):
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.totalseconds = 0


    def tick(self):
        #//Assume SampleT is in seconds
        remainder = 0.0 #local double

        self.totalseconds += globe.SampleT
        self.days = math.floor(self.totalseconds / (3600 * 24))
        remainder = self.totalseconds % (3600 * 24)
        self.hours = math.floor(remainder / (3600))
        remainder = remainder % 3600
        self.minutes = math.floor(remainder / 60)
        self.seconds = remainder % 60


    def timerstring(self):   #public String timerstring()
        return "Days: " + str(self.days) + "  Time: " + \
                str(self.hours) + ":" + str(self.minutes) + \
                ":" + str(self.seconds)


    def __eq__(self, simtimer2):
        return (self.hours == simtimer2.hours and
            self.minutes == simtimer2.minutes and self.seconds == simtimer2.seconds)


    def __ne__(self, simtimer2):
        return not (self.hours == simtimer2.hours and
            self.minutes == simtimer2.minutes and self.seconds == simtimer2.seconds)


    def __lt__(self, simtimer2):
        return (3600 * self.hours + 60 * self.minutes + self.seconds <
                3600 * simtimer2.hours + 60 * simtimer2.minutes + simtimer2.seconds)


    def __gt__(self, simtimer2):
        return (3600 * self.hours + 60 * self.minutes + self.seconds >
                3600 * simtimer2.hours + 60 * simtimer2.minutes + simtimer2.seconds)


    def __ge__(self, simtimer2):
        return (3600 * self.hours + 60 * self.minutes + self.seconds >=
                3600 * simtimer2.hours + 60 * simtimer2.minutes + simtimer2.seconds)


    def ___le__(self, simtimer2):
        return (3600 * self.hours + 60 * self.minutes + self.seconds <=
                3600 * simtimer2.hours + 60 * simtimer2.minutes + simtimer2.seconds)



    


