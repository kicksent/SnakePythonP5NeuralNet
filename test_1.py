import pytest
import copy
import random

# Classes for testing
from snake import Snake
from food import Food
from settings import Settings
from inputs import Inputs
from NeuralNetwork import NeuralNetwork
from population import Population


''' testing for population.py '''


settings = Settings()
P = Population(settings)
P.setup()


def test_crossover():
    parent1 = P.NNArr[0]
    parent2 = P.NNArr[1]
    childNN = NeuralNetwork(settings, P.InputArr[2])
    childNN = childNN.crossover(parent1, parent2)

    p1arr = P.NNArr[0].woh_to_arr()
    p2arr = P.NNArr[1].woh_to_arr()
    childarr = childNN.woh_to_arr()

    for i in range(len(childarr)):
        if(childarr[i] != p2arr[i] and childarr[i] != p1arr[i]):
            assert False
        elif(childarr[i] == p2arr[i] and childarr[i] == p1arr[i]):
            assert False
    assert True


def test_clone():
    # create an instance of NN
    NN = NeuralNetwork(settings, P.InputArr[0])
    # set temp to same instance
    tempNN = NN
    # attempt to clone
    NN = NN.clone()
    # compare
    if NN == tempNN:
        assert False
    assert True

def test_startNextGeneration():
    # set some snake fitnesses for test
    for i in range(len(P.SnakeArr)):
        P.SnakeArr[i].fitness = random.randint(1,5000)



    tmpNNArr = copy.deepcopy(P.NNArr)
    P.startNextGeneration()
    for i in range(0, len(P.NNArr)):
        if(tmpNNArr[i] == P.NNArr[i]):
            assert False
        for j in range(len(tmpNNArr[i].whi)):
            # This test can fail with a very low probability, 
            # however at this time this method seems the most useful 
            # for checking whether I am looking at the same object before 
            # and after the natural selection method is called on the population object
            if tmpNNArr[i].whi[j][j] == P.NNArr[i].whi[j][j]:
                print(tmpNNArr[i].whi[j][j], P.NNArr[i].whi[j][j], "i: {} j: {}".format(i, j))
                assert False
    
    # further testing for unique objects
    for i in range(0, len(P.NNArr)):
        for j in range(0, len(P.NNArr)):
            if(P.NNArr[i] == tmpNNArr[i]):
                assert False

    assert True

def test_startNextGeneration_multiple():
    test_startNextGeneration()
    test_startNextGeneration()
    test_startNextGeneration()
    
    


    
    
