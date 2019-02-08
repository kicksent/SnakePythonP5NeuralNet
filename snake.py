from p5 import *
import numpy as np
class Snake:
    def __init__(self, settings, foodObj):
        self.x = 18*settings.scale
        self.y = 25*settings.scale
        self.xSpeed = settings.scale
        self.ySpeed = 0
        self.scale = settings.scale
        self.settings = settings
        self.food = foodObj
        self.total = 2
        self.tail = [(self.x-self.settings.scale, self.y),(self.x-(self.settings.scale*2), self.y)]
        self.alive = True
        self.fitness = 0
        self.lifetime = 0
        self.isBestSnake = False

    def update(self):
        if(self.alive):
            #update tail
            for i in range(len(self.tail)-1):
                self.tail[i] = self.tail[i+1]
            if(self.total-1 == len(self.tail)):
                self.tail.append((self.x, self.y))
            else:
                self.tail[self.total - 1] = (self.x, self.y)
            
            #update self
            self.x += self.xSpeed
            self.y += self.ySpeed
            self.x = constrain(self.x, 0, self.settings.windowSize-self.settings.scale)
            self.y = constrain(self.y, 0, self.settings.windowSize-self.settings.scale)
            self.lifetime += 1;

            #class methods
            self.checkForDeath()
            self.eatFood()
            self.show()

    def show(self):
        if(self.isBestSnake):
            fill(255)
            square((self.x, self.y), self.settings.scale)
            for i in range(len(self.tail)):
                square(self.tail[i], self.settings.scale)


    def dir(self, x, y):
        x *= self.scale
        y *= self.scale
        if abs(self.xSpeed) == abs(x):
            self.xSpeed = self.xSpeed;
        elif abs(self.ySpeed) == abs(y):
            self.ySpeed = self.ySpeed;
        else:
            self.xSpeed = x;
            self.ySpeed = y;

    def eatFood(self):
        d = dist((self.x, self.y), (self.food.x, self.food.y))  
        if(d == 0):
            self.total+=1
            self.food.eaten = True

    def checkForDeath(self):
        for i in range(len(self.tail)):
            d = dist((self.x, self.y), (self.tail[i]))
            if d == 0:
                self.alive = False
                self.settings.numberOfSnakesAlive -= 1
                self.calcFitness();
                self.settings.totalFitness += self.fitness
                print("Fitness:", self.fitness)
    
    def setFitness(self, fitnessValue):
        self.fitness = fitnessValue

    def calcFitness(self):
        self.fitness = np.power(self.lifetime, 2) * np.power(self.total, 3);
        
    def resetSnake(self):
        self.xSpeed = self.settings.scale
        self.ySpeed = 0
        self.x = 18*self.settings.scale
        self.y = 25*self.settings.scale
        self.total = 2
        self.tail = [(self.x-self.settings.scale, self.y),(self.x-(2*self.settings.scale), self.y)]
        self.alive = True
        self.fitness = 0
        self.lifetime = 0