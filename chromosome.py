import random
import globe as globe


class chromosome:
    def __init__(self, nrmvs): #public chromosome(int nrmvs, Random rand)
        self.mvs = list() #//Manipulated Variables in the chromosome.  For now the mvs will be numbers that are integer percentages (0 - 100) of the 
                                        #//EU range of the variables.
        for i in range(nrmvs):
            self.mvs.append(0)
        self.fitness = 0.0
        random.seed()
        self.initrandom()


    def initrandom(self):
        for i in range(len(self.mvs)):
            self.mvs[i] = random.randint(0, globe.DefaultMaxValueforMVs + 1) #  rand.Next(0, global.DefaultMaxValueforMVs + 1)


    def copyfrom(self, chromosomecopyfrom):  #public void copyfrom(chromosome chromosomecopyfrom)
        for i in range(len(self.mvs)):
            self.mvs[i] = chromosomecopyfrom.mvs[i]



