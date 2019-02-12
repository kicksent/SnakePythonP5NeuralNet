
import numpy as np

class Settings():
    #settings shared between snakes
    def __init__(self):
        self.scale = 20
        self.windowSize = 800
        self.xyMaxValue = self.windowSize - self.scale
        self.gridUnits = self.windowSize / self.scale
        self.framerate = 100
        self.neutalNetworkDimensions = {"input" : 24, "hidden" : 16, "output" : 4}
        
        '''  '''
        self.debug = False
        self.profiling = True

        ''' Settings for snakes '''
        self.generation = 0
        self.numberOfSnakes = 2000
        self.numberOfSnakesAlive = self.numberOfSnakes
        self.totalFitness = 0
        self.mutationRate = .01
        self.globalBestScore = 0
        

        ''' for saving brain '''
        self.whi = None
        self.whh = None
        self.woh = None
        
    def setBestBrain(self, NN):
        #print(NN.whi.dtype)
        self.whi = NN.whi
        self.whh = NN.whh
        self.woh = NN.woh

    def printBestBrain(self):
        print(self.whi, self.whh, self.woh)
        #return(self.whi, self.whh, self.woh)


        