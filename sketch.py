from p5 import *
from snake import Snake
from food import Food
from settings import Settings
from inputs import Inputs
from NeuralNetwork import NeuralNetwork
from population import Population





settings = Settings()
#create Popluation object with settings

P = Population(settings)
def setup():
    size(settings.windowSize, settings.windowSize)
    no_stroke()
    background(0)
    #setup population
    P.setup()
    

def draw():
    background(0)
    #run population
    P.run()




def key_pressed(event):
    if(key == 'W'):
        S.dir(0, -1)
    if(key == 'S'):
        S.dir(0, 1)
    if(key == 'A'):
        S.dir(-1, 0)        
    if(key == 'D'):
        S.dir(1, 0)

run(frame_rate = settings.framerate)