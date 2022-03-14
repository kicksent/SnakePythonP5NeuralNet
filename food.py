import numpy as np
from p5 import *
class Food:
    
    def __init__(self, settings):
        np.random.seed(2022)
        self.settings = settings
        self.spawnLocations = []
        self.spawnIndex = 0
        self.generateRandomFoodList()
        self.x = 15 * self.settings.scale
        self.y = 15 * self.settings.scale
        self.eaten = False
        self.isFoodForBestSnake = False

    def update(self):
        if(self.eaten == False):
            self.show()
        else:   
            self.spawnAtRandomLocation()

    def spawnAtRandomLocation(self):
        self.x = self.spawnLocations[self.spawnIndex][0]
        self.y = self.spawnLocations[self.spawnIndex][1]
        # self.x = np.random.randint(self.settings.gridUnits) * self.settings.scale
        # self.y = np.random.randint(self.settings.gridUnits) * self.settings.scale
        self.spawnIndex += 1
        self.eaten = False

    def spawnAtInitialLocation(self):
        self.x = self.spawnLocations[0][0]
        self.y = self.spawnLocations[0][1]
        self.eaten = False
    
    def show(self):
        if(self.isFoodForBestSnake):
            fill(100, 0, 100)
            square((self.x, self.y), self.settings.scale)

    def generateRandomFoodList(self):
        for i in range(1,100):
            self.spawnLocations.append([np.random.randint(self.settings.gridUnits) * self.settings.scale, np.random.randint(self.settings.gridUnits) * self.settings.scale])