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
        self.settings = settings
        self.FoodArr = []
        self.SnakeArr = []
        self.InputArr = []
        self.NNArr = []
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
        self.updateBestBrain()
        for i in range(self.settings.numberOfSnakes):
            self.SnakeArr[i].update()
            if(self.SnakeArr[i].alive == True):
                self.FoodArr[i].update()
                self.InputArr[i].generateInputs()
                self.NNArr[i].controlSnake(self.SnakeArr[i])
            self.snakesAlive = self.settings.numberOfSnakesAlive
            if(self.snakesAlive == 0):
                print("All Snakes Have Died")
                self.startNextGeneration()
            
            
    def updateBestBrain(self):
        if(self.SnakeArr[self.currentBestIndex].alive == False):
            for i in range(self.settings.numberOfSnakes):
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
            #create babies
            if(i == bestIndex):
                #keep best snake
                self.NNArr[i] = self.NNArr[i].clone()
            else:
                self.NNArr[i] = self.naturalSelection(i).clone()


    def resetSnakesAndFood(self):
        for i in range(self.settings.numberOfSnakes):
            # self.FoodArr[i].spawnAtRandomLocation()
            self.SnakeArr[i].resetSnake()

        
    
    def naturalSelection(self, index):
        #create a new NeuralNetwork
        childNN = NeuralNetwork(self.settings, self.InputArr[index])
        
        # select two brains from the existing pool to mate
        # childNN = childNN.crossover(self.selectNNFromSnakeFitness(), self.selectNNFromSnakeFitness())
        childNN = childNN.crossover(self.getBestSnakeBrain(), self.selectNNFromSnakeFitness())
        # childNN = childNN.crossover(self.getBestSnakeBrain(),  self.selectNNFromSnakeFitness())
        childNN = childNN.mutate()
        return(childNN)
                
    def selectNNFromSnakeFitness(self):
        rand = random.randint(0, self.settings.totalFitness)
        sum = 0
        for i in range(self.settings.numberOfSnakes):
            if(sum >= rand):
                return self.NNArr[i]
            else:
                sum += self.SnakeArr[i].fitness
        if(sum >= rand):
            return self.NNArr[i]
        #leave here, in case bug still exists
        total=0
        for i in range(self.settings.numberOfSnakes):
            total += self.SnakeArr[i].fitness
            print("Debug fitness", self.settings.numberOfSnakes,  self.SnakeArr[i].fitness)

        raise Exception("Function should not reach here. Sum: {}, rand: {}, Fitness Sum: {} {} {} ".format(sum, rand, self.settings.totalFitness, total, total == self.settings.totalFitness))

    def getBestSnakeBrainIndex(self):
        max_index = 0
        max_fitness = 0
        for i in range(self.settings.numberOfSnakes):
            if(self.SnakeArr[i].fitness > max_fitness):
                self.settings.globalBestScore = self.SnakeArr[i].fitness
                max_index = i
                max_fitness = self.SnakeArr[i].fitness
        return(max_index)

    def getBestSnakeBrain(self):
        max_index = 0
        max_fitness = 0
        for i in range(self.settings.numberOfSnakes):
            if(self.SnakeArr[i].fitness > max_fitness):
                self.settings.globalBestScore = self.SnakeArr[i].fitness
                max_index = i
                max_fitness = self.SnakeArr[i].fitness
        return(self.NNArr[max_index])
    

        


