import globe as globe
import math
from controlvar import controlvar

def dndt2fps(adndt):  #public static double dndt2fps(double adndt)
    return adndt * (globe.R * globe.Ts) / globe.Ps


def calcdirection(deltay, deltax):
        #public static double calcdirection(double deltay, double deltax)
    bias = 0.0  #double local var
    if (deltax == 0): deltax = 0.0001
    if (deltax < 0):
        bias = math.pi
    else:
        bias = 0.0
    return bias + math.atan(deltay / float(deltax))


def distance(p1, p2): #public static double distance(point p1, point p2)
    if isinstance(p1, float) or isinstance (p1, int):
        deltax = p1
        deltay = p2
        return math.sqrt((deltax**2) + (deltay**2))
    else:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def fps2fph(aflowps): #argument can be float or controlvar
    if isinstance(aflowps, controlvar): return aflowps.v*3600.0
    else: return aflowps*3600.0


def fph2fps(aflowph): #argument can be float or controlvar
    if isinstance(aflowph, controlvar):
        return aflowph.v / 3600.0
    else:
        return aflowph / 3600.0


def pascal2barg(apres):  #public static double pascal2barg(double apres):
    if isinstance(apres, controlvar):
        return (apres.v - globe.Ps) / globe.Ps
    else:
        return (apres - globe.Ps) / globe.Ps


def pascal2bara(apres):
    if isinstance(apres, controlvar):
        return (apres.v) / globe.Ps
    else:
        return (apres) / globe.Ps


def barg2pascal(apres):  #argument can be float or controlvar
    if isinstance(apres, controlvar):
        return apres.v * globe.Ps + globe.Ps
    else:
        return apres * globe.Ps + globe.Ps


def bara2pascal(apres):
    if isinstance(apres, controlvar):
        return apres.v * globe.Ps
    else:
        return apres * globe.Ps


def kelvin2celcius(atempkelvin):  #public static double kelvin2celcius(double atempkelvin)
    if isinstance(atempkelvin, controlvar):
        return atempkelvin.v - 273.15
    else:
        return atempkelvin - 273.15


def celcius2kelvin(atempcelcius):  #argument can be float or controlvar
    if isinstance(atempcelcius, controlvar):
        return atempcelcius.v + 273.15
    else:
        return atempcelcius + 273.15


def sigmoid(t):
    return 1 / (1 + math.exp(-t))





