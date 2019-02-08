import numpy as np
from p5 import *
class Food:
    def __init__(self, settings):
        self.settings = settings
        self.x = np.random.randint(settings.gridUnits) * self.settings.scale
        self.y = np.random.randint(settings.gridUnits) * self.settings.scale
        self.eaten = False
        self.isFoodForBestSnake = False

    def update(self):
        if(self.eaten == False):
            self.show()
        else:   
            self.spawnAtRandomLocation()

    def spawnAtRandomLocation(self):
        self.x = np.random.randint(self.settings.gridUnits) * self.settings.scale
        self.y = np.random.randint(self.settings.gridUnits) * self.settings.scale
        self.eaten = False
    
    def show(self):
        if(self.isFoodForBestSnake):
            fill(100, 0, 100)
            square((self.x, self.y), self.settings.scale)