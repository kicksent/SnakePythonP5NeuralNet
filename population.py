from settings import Settings
from snake import Snake
from food import Food
from inputs import Inputs
from NeuralNetwork import NeuralNetwork
import numpy as np
from p5 import *
import random
from cprofiler import profile 


class Population:
    def __init__(self, settings):
        self.settings: Settings = settings
        self.FoodArr: list[Food] = []
        self.SnakeArr: list[Snake] = []
        self.InputArr: list[Inputs] = []
        self.NNArr: list[NeuralNetwork] = []
        self.snakesAlive = settings.numberOfSnakes
        self.currentBestIndex = 0
    def setup(self):
        for i in range(self.settings.numberOfSnakes):
            self.FoodArr.append(Food(self.settings))
            self.SnakeArr.append(Snake(self.settings, self.FoodArr[i]))
            self.InputArr.append(Inputs(self.settings, self.SnakeArr[i]))
            self.NNArr.append(NeuralNetwork(self.settings, self.InputArr[i]))
        self.resetBestBrain()
        self.updateBestBrain()
    
    def resetBestBrain(self):
        for i in range(self.settings.numberOfSnakes):
            self.SnakeArr[i].hasBestBrain = False
            self.SnakeArr[i].food.isFoodForBestSnake = False
    
    
    def run(self):
        for i in range(self.settings.numberOfSnakes):
            self.updateBestBrain()
            self.SnakeArr[i].update()
            if(self.SnakeArr[i].alive == True):
                self.FoodArr[i].update()
                self.InputArr[i].generateInputs()
                self.NNArr[i].controlSnake(self.SnakeArr[i])
            self.snakesAlive = self.settings.numberOfSnakesAlive
            if(self.snakesAlive == 0):
                print("gen bests ------ index: {} score: {}".format(self.getBestSnakeBrainIndex(), self.SnakeArr[self.getBestSnakeBrainIndex()].fitness))
                print("global bests --- index: {} score: {}".format(self.settings.globalBestIndex, self.settings.globalBestScore))
                self.startNextGeneration()
            
            
    def updateBestBrain(self):
        if(self.SnakeArr[self.currentBestIndex].alive == False):
            self.SnakeArr[self.currentBestIndex].hasBestBrain = False
            self.SnakeArr[self.currentBestIndex].food.isFoodForBestSnake = False
            bestIndex = self.getBestSnakeBrainIndex()
            self.currentBestIndex = bestIndex
            self.SnakeArr[bestIndex].hasBestBrain = True
            self.SnakeArr[bestIndex].food.isFoodForBestSnake = True


    def startNextGeneration(self):
        print("starting next gen")
        #increment generation
        self.settings.generation += 1

        #do algorithm for genetics
        self.createNewBrains()

        #reset scores
        self.settings.reset()
        self.resetSnakesAndFood()

    def createNewBrains(self):
        #create a New NN from Old NN that has been mutated
        
        bestIndex = self.getBestSnakeBrainIndex()
        for i in range(self.settings.numberOfSnakes):
            
            #keep best snake or other snakes that are close!
            if(i == bestIndex):
                self.NNArr[i] = self.NNArr[i] #do nothing for now 
            else:
                #create babies and match them with snakes based on score
                self.NNArr[i] = self.naturalSelection(i)


    def resetSnakesAndFood(self):
        for i in range(self.settings.numberOfSnakes):
            # self.FoodArr[i].spawnAtRandomLocation()
            self.SnakeArr[i].resetSnake()

        
    
    def naturalSelection(self, index):
        #create a new NeuralNetwork
        childNN = NeuralNetwork(self.settings, self.InputArr[index])
        
        # select two brains from the existing pool to mate
        switch = np.random.random()
        # paranoia
        if(switch > .5):
            index = self.selectNNFromSnakeFitness()
            childNN = childNN.crossover(childNN, self.NNArr[index])
        else:
            index = self.selectNNFromSnakeFitness()
            childNN = childNN.crossover(self.NNArr[index], childNN)
        childNN = childNN.mutate()
        return(childNN)
                
    def selectNNFromSnakeFitness(self):
        # has test in test_1.py
        rand = random.randint(0, self.settings.totalFitness)
        # print("random number selected: {} totalfitness: {}".format(rand, self.settings.totalFitness))
        sum = 0 
        for i in range(self.settings.numberOfSnakes):
            sum += self.SnakeArr[i].fitness
            if(sum >= rand):
                # print("index {} was selected for breeding with fitness {} sum: {}, rand: {}".format(i, self.SnakeArr[i].fitness, sum, rand))
                return i

        raise Exception("Function should not reach here.")

    def getBestSnakeBrainIndex(self):
        #don't update the best index unless it beats the global best!
        for i in range(self.settings.numberOfSnakes):
            if(self.SnakeArr[i].fitness > self.settings.globalBestScore):
                self.settings.globalBestScore = self.SnakeArr[i].fitness
                self.settings.globalBestIndex = i
        return(self.settings.globalBestIndex)

    def getBestSnakeBrain(self):
        bestIndex = self.getBestSnakeBrainIndex()
        return(self.NNArr[bestIndex])
    

        


