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
    text("GENERATION: {}".format(settings.generation), (100,100), wrap_at=None)




def key_pressed(event):
    if(key == 'h'):
        settings.mutationRate /= 2  
    if(key == 'd'):
        settings.mutationRate *= 2
    

run(frame_rate = settings.framerate)