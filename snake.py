from p5 import *
import numpy as np

from food import Food
from settings import Settings
class Snake:
    def __init__(self, settings, foodObj):
        self.x = settings.windowSize / 2
        self.y = settings.windowSize / 2
        self.xSpeed = settings.scale
        self.ySpeed = 0
        self.scale = settings.scale
        self.settings: Settings = settings
        self.food: Food = foodObj
        self.total = 2
        self.tail = [(self.x-self.settings.scale, self.y),(self.x-(self.settings.scale*2), self.y)]
        self.alive = True
        self.fitness = 0
        self.lifetime = 0
        self.hasBestBrain = False
        self.movesRemaining = 100

    def update(self):
        if(self.alive):
            #update tail
            for i in range(len(self.tail)-1):
                self.tail[i] = self.tail[i+1]
            if(self.total - 1 == len(self.tail)):
                self.tail.append((self.x, self.y))
            else:
                self.tail[self.total - 1] = (self.x, self.y)
            
            #update self
            self.x += self.xSpeed
            self.y += self.ySpeed
            self.x = constrain(self.x, 0, self.settings.windowSize-self.settings.scale)
            self.y = constrain(self.y, 0, self.settings.windowSize-self.settings.scale)
            self.lifetime += 1

            #class methods
            self.movesRemaining -= 1
            self.checkForDeath()
            self.eatFood()
            self.show()

    def show(self):
        if(self.hasBestBrain):
            fill(255)
            square((self.x, self.y), self.settings.scale)
            for i in range(len(self.tail)):
                square(self.tail[i], self.settings.scale)


    def dir(self, x, y):
        x *= self.scale
        y *= self.scale
        if abs(self.xSpeed) == abs(x):
            self.xSpeed = self.xSpeed
        elif abs(self.ySpeed) == abs(y):
            self.ySpeed = self.ySpeed
        else:
            self.xSpeed = x
            self.ySpeed = y

    def eatFood(self):
        d = dist((self.x, self.y), (self.food.x, self.food.y))  
        if(d == 0):
            self.total+=1
            self.movesRemaining += 100
            self.food.eaten = True
            if(self.total > self.settings.globalBestTotal):
                self.settings.globalBestTotal = self.total

    def checkForDeath(self):
        self.calcFitness()

        if(self.movesRemaining < 0):
            self.alive = False
            self.settings.numberOfSnakesAlive -= 1
            self.settings.totalFitness += self.fitness
            if(self.fitness > 0):
                print("Fitness:", self.fitness, "out of moves", self.movesRemaining)
        else:
            for i in range(len(self.tail)):
                d = dist((self.x, self.y), (self.tail[i]))
                if d == 0:
                    self.alive = False
                    self.settings.numberOfSnakesAlive -= 1
                    self.settings.totalFitness += self.fitness
                    if(self.fitness > 0):
                        print("Fitness:", self.fitness, "snake crashed it's face")
    
    def calcFitness(self):
        if(self.total < 10):
            self.fitness = (self.lifetime * self.lifetime) * np.power(2, self.total)
        else:
            self.fitness = ((self.lifetime * self.lifetime) * np.power(2, 10)) * (self.total-9)
        
    def resetSnake(self):
        self.xSpeed = self.settings.scale
        self.ySpeed = 0
        self.x = self.settings.windowSize/2
        self.y = self.settings.windowSize/2
        self.total = 2
        self.tail = [(self.x-self.settings.scale, self.y),(self.x-(2*self.settings.scale), self.y)]
        self.alive = True
        self.fitness = 0
        self.lifetime = 0
        self.movesRemaining = 100
        self.food.spawnAtInitialLocation()
