
import numpy as np
np.set_printoptions(linewidth = 200, precision = 10)
from scipy.special import expit
import numba
from numba import jit
from cprofiler import profile

class NeuralNetwork:
    def __init__(self, settings, snake, inputs):
        self.settings = settings
        self.num_input = settings.neutalNetworkDimensions["input"];
        self.num_hidden = settings.neutalNetworkDimensions["hidden"];
        self.num_output = settings.neutalNetworkDimensions["output"];
        self.snake = snake
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

    
    def controlSnake(self):
        self.output(self.inputs.inputVector)
        self.updateTurnDirection()

    
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


    def updateTurnDirection(self):
        max = 0
        maxIndex = 0
        for i in range(len(self.outputArray)):
            if(self.outputArray[i] > max):
                max = self.outputArray[i]
                maxIndex = i

        if maxIndex == 0:
            #left
            self.snake.dir(-1, 0)
        elif maxIndex == 1:
            #right
            self.snake.dir(1, 0)
        elif maxIndex == 2:
            #up
            self.snake.dir(0, -1)
        elif maxIndex == 3:
            #down
            self.snake.dir(0, 1)
    
    def mutate(self):
        for i in range(self.whi.shape[0]):
            for j in range(self.whi.shape[1]):
                if(np.random.random() < self.settings.mutationRate):
                    self.whi[i,j] += np.random.random()/5
        for i in range(self.whh.shape[0]):
            for j in range(self.whh.shape[1]):
                if(np.random.random() < self.settings.mutationRate):
                    self.whh[i,j] += np.random.random()/5
        for i in range(self.woh.shape[0]):
            for j in range(self.woh.shape[1]):
                if(np.random.random() < self.settings.mutationRate):
                    self.woh[i,j] += np.random.random()/5
        return(self)


    def crossover(self, oldSnake, partner):
        rand = np.random.rand()
        randC = np.random.randint(self.whi.shape[0])
        randR = np.random.randint(self.whi.shape[1])
        for i in range(self.whi.shape[0]):
            for j in range(self.whi.shape[1]):
                if(rand <= .5):
                    if i < randR or ( i == randR and j <= randC):
                        self.whi[i,j] = partner.whi[i,j]
                    else:
                        self.whi[i,j] = oldSnake.whi[i,j]
                else:
                    if i < randR or ( i == randR and j <= randC):
                        self.whi[i,j] = oldSnake.whi[i,j]
                    else:
                        self.whi[i,j] = partner.whi[i,j]
        rand = np.random.rand()
        randC = np.random.randint(self.whh.shape[0])
        randR = np.random.randint(self.whh.shape[1])
        for i in range(self.whh.shape[0]):
            for j in range(self.whh.shape[1]):
                if(rand <= .5):
                    if i < randR or ( i == randR and j <= randC):
                        self.whh[i,j] = partner.whh[i,j]
                    else:
                        self.whi[i,j] = oldSnake.whi[i,j]
                else:
                    if i < randR or ( i == randR and j <= randC):
                        self.whi[i,j] = oldSnake.whi[i,j]
                    else:
                        self.whh[i,j] = partner.whh[i,j]

        randC = np.random.randint(self.woh.shape[0])
        randR = np.random.randint(self.woh.shape[1])
        for i in range(self.woh.shape[0]):
            for j in range(self.woh.shape[1]):
                if(rand <= .5):
                    if i < randR or ( i == randR and j <= randC):
                        self.woh[i,j] = partner.woh[i,j]
                    else:
                        self.whi[i,j] = oldSnake.whi[i,j]
                else:
                    if i < randR or ( i == randR and j <= randC):
                        self.whi[i,j] = oldSnake.whi[i,j]
                    else:
                        self.woh[i,j] = partner.woh[i,j]





