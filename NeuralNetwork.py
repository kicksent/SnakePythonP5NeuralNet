
import numpy as np
np.set_printoptions(linewidth = 200, precision = 10)
from scipy.special import expit

import numba
from numba import jit

from cprofiler import profile
from p5 import *

import copy


class NeuralNetwork:
    def __init__(self, settings, inputs):
        self.settings = settings
        self.num_input = settings.neutalNetworkDimensions["input"];
        self.num_hidden = settings.neutalNetworkDimensions["hidden"];
        self.num_output = settings.neutalNetworkDimensions["output"];
        #self.in_neurons = [];
        #generate random starting weights for snake
        #np.array([np.random.uniform(-1,1) for i in range(8)]).reshape(2,4)
        self.whi = np.array([np.random.uniform(-1,1) for i in range(self.num_hidden*(self.num_input+1))]).reshape(self.num_hidden, self.num_input+1)
        #self.whi = np.random.rand(self.num_hidden, self.num_input + 1)
        self.whh = np.array([np.random.uniform(-1,1) for i in range(self.num_hidden*(self.num_hidden+1))]).reshape(self.num_hidden, self.num_hidden+1)
        #self.whh = np.random.rand(self.num_hidden, self.num_hidden + 1)
        self.woh = np.array([np.random.uniform(-1,1) for i in range(self.num_output*(self.num_hidden+1))]).reshape(self.num_output, self.num_hidden+1)
        #self.woh = np.random.rand(self.num_output, self.num_hidden + 1)
        self.dir_array = ["left", "right", "up", "down"];
        self.outputArray = []
        self.inputs = inputs
        self.isBestBrain = False

    
    def controlSnake(self, snake):
        self.output(self.inputs.inputVector)
        self.updateTurnDirection(snake)

    
    def sigmoid(self,x):
        # for i in range(len(x)):
        #     x[i] = (1 / 1+ np.exp(-x[i]))
        # return(x)
        return(1 / (1+ np.exp(-x)))

    
    #calculate output by feeding forward through neural network
    def output(self,inp):
        res1 = self.feedForward(self.whi, inp)
        res2 = self.feedForward(self.whh, res1)
        res3 = self.feedForward(self.woh, res2)
        self.outputArray = res3
        #print(self.outputArray)

    
    def feedForward(self, matrix, arr):
        tempArr = np.append(arr, [1.0])
        tempArr = np.matrix(tempArr).T
        res = matrix * tempArr
        res = self.sigmoid(res)
        res = np.array(res).flatten()
        return(res)


    def updateTurnDirection(self, snake):
        max = 0
        maxIndex = 0
        for i in range(len(self.outputArray)):
            if(self.outputArray[i] > max):
                max = self.outputArray[i]
                maxIndex = i

        if maxIndex == 0:
            #left
            snake.dir(-1, 0)
        elif maxIndex == 1:
            #right
            snake.dir(1, 0)
        elif maxIndex == 2:
            #up
            snake.dir(0, -1)
        elif maxIndex == 3:
            #down
            snake.dir(0, 1)
    
    def mutate(self):
        for i in range(self.whi.shape[0]):
            for j in range(self.whi.shape[1]):
                if(np.random.random() < self.settings.mutationRate):
                    self.whi[i,j] += np.random.random()/5
                    self.whi[i,j] = constrain(self.whi[i,j], -1, 1)
        for i in range(self.whh.shape[0]):
            for j in range(self.whh.shape[1]):
                if(np.random.random() < self.settings.mutationRate):
                    self.whh[i,j] += np.random.random()/5
                    self.whh[i,j] = constrain(self.whh[i,j], -1, 1)
        for i in range(self.woh.shape[0]):
            for j in range(self.woh.shape[1]):
                if(np.random.random() < self.settings.mutationRate):
                    self.woh[i,j] += np.random.random()/5
                    self.woh[i,j] = constrain(self.woh[i,j], -1, 1)
        return(self)
        


    def crossover(self, parent1, parent2): 
        randC = np.random.randint(self.whi.shape[0])
        randR = np.random.randint(self.whi.shape[1])
        for i in range(self.whi.shape[0]):
            for j in range(self.whi.shape[1]):
                if i < randR or ( i == randR and j <= randC):
                    self.whi[i,j] = parent1.whi[i,j]
                else:
                    self.whi[i,j] = parent2.whi[i,j]
        randC = np.random.randint(self.whi.shape[0])
        randR = np.random.randint(self.whi.shape[1])        
        for i in range(self.whh.shape[0]):
            for j in range(self.whh.shape[1]):
                if i < randR or ( i == randR and j <= randC):
                    self.whh[i,j] = parent1.whh[i,j]
                else:
                    self.whh[i,j] = parent2.whh[i,j]
        randC = np.random.randint(self.whi.shape[0])
        randR = np.random.randint(self.whi.shape[1])   
        for i in range(self.woh.shape[0]):
            for j in range(self.woh.shape[1]):
                if i < randR or ( i == randR and j <= randC):
                    self.woh[i,j] = parent1.woh[i,j]
                else:
                    self.woh[i,j] = parent2.woh[i,j]
        return(self)
            
    #used for testing
    def woh_to_arr(self):
        arr = []
        for i in range(self.num_output):
            for j in range(self.num_hidden+1):
                arr.append(self.woh[i][j])
        return(arr)


    def clone(self):
        copy.deepcopy(self)


