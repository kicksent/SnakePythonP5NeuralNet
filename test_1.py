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
    childNN.crossover(parent1, parent2)


    # test that the values in the child come from the parents
    p1arr = P.NNArr[0].woh_to_arr()
    p2arr = P.NNArr[1].woh_to_arr()
    childarr = childNN.woh_to_arr()

    #the value must be either the parent 1 or parent2 values
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

    # for i in range(len(tempNN[0])):
    #     if(tempNN[0] != NN[0]):
    #         assert(false)
    print(NN)

def test_startNextGeneration():
    # prevent side effects from test
    curMutationRate = settings.mutationRate
    settings.mutationRate = 0

    # set some snake fitnesses for test
    for i in range(len(P.SnakeArr)):
        P.SnakeArr[i].fitness = random.randint(1,5000)

    tmpNNArr = copy.deepcopy(P.NNArr)
    P.startNextGeneration()
    for i in range(0, len(P.NNArr)):
        if(tmpNNArr[i] == P.NNArr[i]):
            assert False
        for j in range(len(tmpNNArr[i].whi)):
            if tmpNNArr[i].whi[j][j] == P.NNArr[i].whi[j][j]:
                print(tmpNNArr[i].whi[j][j], P.NNArr[i].whi[j][j], "i: {} j: {}".format(i, j))
                assert False
    
    # further testing for unique objects
    for i in range(0, len(P.NNArr)):
        for j in range(0, len(P.NNArr)):
            if(P.NNArr[i] == tmpNNArr[i]):
                assert False

    assert True

    #restore previous state
    settings.mutationRate = curMutationRate

def test_startNextGeneration_multiple():
    test_startNextGeneration()
    test_startNextGeneration()
    test_startNextGeneration()


# test fitness calculator

def test_fitness():
    f = Food(settings)
    snake = Snake(settings, f)
    snake.lifetime = 9
    snake.total = 5
    snake.calcFitness()
    assert(snake.fitness == 2592)

def test_fitness2():
    f = Food(settings)
    snake = Snake(settings, f)
    snake.lifetime = 10
    snake.total = 5
    snake.calcFitness()
    assert(snake.fitness == 3200)

def test_fitness4():
    f = Food(settings)
    snake = Snake(settings, f)
    snake.lifetime = 100
    snake.total = 5
    snake.calcFitness()
    assert(snake.fitness == 320000)

def test_fitness3():
    f = Food(settings)
    snake1 = Snake(settings, f)
    snake1.lifetime = 101
    snake1.total = 6
    snake1.calcFitness()

    f = Food(settings)
    snake2 = Snake(settings, f)
    snake2.lifetime = 100
    snake2.total = 7
    snake2.calcFitness()
    assert(snake2.fitness > snake1.fitness)
