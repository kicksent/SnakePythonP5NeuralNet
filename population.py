from snake import Snake
from food import Food
from inputs import Inputs
from NeuralNetwork import NeuralNetwork
import numpy as np
from p5 import *
from cprofiler import profile #@profile

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
    #@profile
    def run(self):
        for i in range(self.settings.numberOfSnakes):
            self.SnakeArr[i].update()
            self.FoodArr[i].update()
            self.InputArr[i].generateInputs()
            self.NNArr[i].controlSnake()
            self.snakesAlive = self.settings.numberOfSnakesAlive
            if(self.snakesAlive == 0):
                print("All Snakes Have Died")
                self.startNextGenetation();
    
    def startNextGenetation(self):
        #save best snake brain
        self.saveBestSnakeBrain()

        self.settings.numberOfSnakesAlive = self.settings.numberOfSnakes
        #create a New Neural Network that has been mutated 
        self.FoodArr = []
        self.InputArr = []
        updatedNeuralNetwork = []
        for i in range(self.settings.numberOfSnakes):
            self.FoodArr.append(Food(self.settings))
            self.InputArr.append(Inputs(self.settings, self.SnakeArr[i], self.FoodArr[i]))
        
        for i in range(self.settings.numberOfSnakes):
            updatedNeuralNetwork.append(self.selectNNFromSnakeFitness(self.NNArr[i], NeuralNetwork(self.settings, self.SnakeArr[i], self.InputArr[i])));

        for i in range(self.settings.numberOfSnakes):
            self.SnakeArr[i].resetSnake()

        self.NNArr = updatedNeuralNetwork
        self.NNArr[0].whi, self.NNArr[0].whh, self.NNArr[0].woh = self.settings.getBestBrain()
        self.SnakeArr[0].isBestSnake = True
        self.FoodArr[0].isFoodForBestSnake = True
        self.settings.totalFitness = 0
        

                
    def selectNNFromSnakeFitness(self, existingNN, newNN):
        while(True):
            for i in range(self.settings.numberOfSnakes):
                #select a value between 0 and 1
                rand = np.random.rand()
                #calculate chance for snake to be chosen
                chance = self.SnakeArr[i].fitness / self.settings.totalFitness
                #print(rand, chance)
                if(rand < chance):
                    newNN.crossover(existingNN, self.NNArr[i])
                    return(newNN.mutate())

    def saveBestSnakeBrain(self):
        max = 0
        for i in range(self.settings.numberOfSnakes):
            if(self.SnakeArr[i].fitness > self.settings.globalBestScore):
                self.settings.globalBestScore = self.SnakeArr[i].fitness
                max = i
        self.settings.setBestBrain(self.NNArr[max])
        
        return(self.NNArr[i])


