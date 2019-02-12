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
    def setup(self):
        for i in range(self.settings.numberOfSnakes):
            self.FoodArr.append(Food(self.settings))
            self.SnakeArr.append(Snake(self.settings, self.FoodArr[i]))
            self.InputArr.append(Inputs(self.settings, self.SnakeArr[i], self.FoodArr[i]))
            self.NNArr.append(NeuralNetwork(self.settings, self.SnakeArr[i], self.InputArr[i]))

    def reset(self):
        self.FoodArr = []
        self.SnakeArr = []
        self.InputArr = []
        self.NNArr = []
        self.setup()
    
    
    def run(self):
        for i in range(self.settings.numberOfSnakes):
            self.SnakeArr[i].update()
            if(self.SnakeArr[i].alive == True):
                self.FoodArr[i].update()
                self.InputArr[i].generateInputs()
                self.NNArr[i].controlSnake()
            self.snakesAlive = self.settings.numberOfSnakesAlive
            if(self.snakesAlive == 0):
                print("All Snakes Have Died")
                self.startNextGenetation();
    
    def startNextGenetation(self):
        #increment generation
        self.settings.generation += 1
        
        #save best snake brain
        self.setBestSnakeBrain()

        
        #create a New Neural Network that has been mutated 
        updatedNeuralNetwork = []
        
        for i in range(self.settings.numberOfSnakes):
            #create babies
            if(self.SnakeArr[i].isBestSnake == False):
                newNN = self.naturalSelection(NeuralNetwork(self.settings, self.SnakeArr[i], self.InputArr[i]))
                updatedNeuralNetwork.append(newNN);
            else:
                #best snake goes on unchanged
                print("KEEPING BEST SNAKE")
                updatedNeuralNetwork.append(self.NNArr[i]);

        for i in range(self.settings.numberOfSnakes):
            self.SnakeArr[i].resetSnake()

        self.NNArr = updatedNeuralNetwork
        self.settings.numberOfSnakesAlive = self.settings.numberOfSnakes
        self.settings.totalFitness = 0
        
    
    def naturalSelection(self, childNN):
        childNN = childNN.crossover(self.selectNNFromSnakeFitness(), self.selectNNFromSnakeFitness())
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
            print("Debug fitness", self.SnakeArr[i].fitness)

        raise Exception("Function should not reach here. Sum: {}, rand: {}, Fitness Sum: {} {} {} ".format(sum, rand, self.settings.totalFitness, total, total == self.settings.totalFitness))

    def setBestSnakeBrain(self):
        max = 0
        max_fitness = 0
        for i in range(self.settings.numberOfSnakes):
            if(self.SnakeArr[i].fitness > max_fitness):
                self.settings.globalBestScore = self.SnakeArr[i].fitness
                max = i
                max_fitness = self.SnakeArr[i].fitness
            else:
                self.FoodArr[i].isFoodForBestSnake = False
                self.NNArr[i].isBestBrain = False
                self.SnakeArr[i].isBestSnake = False

        self.FoodArr[max].isFoodForBestSnake = True
        self.NNArr[max].isBestBrain = True
        self.SnakeArr[max].isBestSnake = True
        


