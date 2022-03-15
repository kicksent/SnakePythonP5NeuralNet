
import numpy as np

class Settings():
    #settings shared between snakes
    def __init__(self):
        self.scale = 20
        self.windowSize = 400
        self.xyMaxValue = self.windowSize - self.scale
        self.gridUnits = self.windowSize / self.scale
        self.framerate = 100
        self.neutalNetworkDimensions = {"input" : 24, "hidden" : 16, "output" : 4}
        
        '''  '''
        self.debug = False
        self.profiling = True

        ''' Settings for snakes '''
        self.generation = 0
        self.numberOfSnakes = 1000
        self.numberOfSnakesAlive = self.numberOfSnakes
        self.totalFitness = 0
        self.mutationRate = .01
        self.globalBestScore = 0
        self.globalBestIndex = 0
        self.globalBestTotal = 0
        

        ''' for saving brain '''
        self.whi = None
        self.whh = None
        self.woh = None

        self.spawnLocations = self.__generateRandomFoodList()

    def reset(self):
        self.numberOfSnakesAlive = self.numberOfSnakes
        self.totalFitness = 0

    def __generateRandomFoodList(self):
        #make the food locations the same for all snakes
        spawnLocations = []
        for i in range(1,100):
            spawnLocations.append([np.random.randint(self.gridUnits) * self.scale, np.random.randint(self.gridUnits) * self.scale])
        return(spawnLocations)

        