import random
import sys


class particle:
    def __init__(self, nrmvs, amaxvalueformv): #public particle(int nrmvs, Random rand, double amaxvalueformv)
        self.currentmvs = list() #List<double>() #Manipulated Variables in the particle - current.
        self.bestmvs = list() #List<double>() #Manipulated Variables in the particle - best solution in history of current objective.
        self.currentspeed = list() #List<double>(); #peed of each particles along each MV dimension.
        self.maxvalueformv = amaxvalueformv
        for i in range(nrmvs):
            self.currentmvs.append(0.0)
            self.bestmvs.append(0.0)
            self.currentspeed.append(0.0)
        self.currentfitness = sys.float_info.max
        self.bestfitness = sys.float_info.max
        self.initrandom()


    def initrandom(self):
        for i in range(len(self.currentmvs)):
            #//currentmvs[i] = rand.Next(0, global.DefaultMaxValueforMVs + 1);
            self.currentmvs[i] = random.random() * self.maxvalueformv
            #//bestmvs[i] = rand.Next(0, global.DefaultMaxValueforMVs + 1);


    def copyfrom(self, particlecopyfrom):  #public void copyfrom(particle particlecopyfrom)
        for i in range(len(self.currentmvs)):
            self.currentmvs[i] = particlecopyfrom.currentmvs[i]
            self.bestmvs[i] = particlecopyfrom.bestmvs[i]

