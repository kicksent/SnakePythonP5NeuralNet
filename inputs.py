import numpy as np
np.set_printoptions(linewidth = 200)
from snake import Snake
class Inputs:
    def __init__(self, settings, snake, food):
        self.settings = settings
        self.snake = snake
        self.food = food
        self.inputVector = []
    
    def update(self, snake, food):
        self.snake = snake
        self.food = food

    def generateInputs(self):
        
        inputVector = np.array([0]*24, dtype=float)
        #distances: temp[0] is food, temp[1] is tail, temp[2] is wall
        #look left
        temp = self.look([-10, 0]);
        inputVector[0] = temp[0];
        inputVector[1] = temp[1];
        inputVector[2] = temp[2];
        #look left/up  
        temp2 = self.look([-10, -10]);
        inputVector[3] = temp2[0];
        inputVector[4] = temp2[1];
        inputVector[5] = temp2[2];
        #look up
        temp3 = self.look([0, -10]);
        inputVector[6] = temp3[0];
        inputVector[7] = temp3[1];
        inputVector[8] = temp3[2];
        #look up/right
        temp4 = self.look([10, -10]);
        inputVector[9] = temp4[0];
        inputVector[10] = temp4[1];
        inputVector[11] = temp4[2];
        #look right
        temp5 = self.look([10, 0]);
        inputVector[12] = temp5[0];
        inputVector[13] = temp5[1];
        inputVector[14] = temp5[2];
        #look right/down
        temp6 = self.look([10, 10]);
        inputVector[15] = temp6[0];
        inputVector[16] = temp6[1];
        inputVector[17] = temp6[2];
        #look down
        temp7 = self.look([0, 10]);
        inputVector[18] = temp7[0];
        inputVector[19] = temp7[1];
        inputVector[20] = temp7[2];
        #look down/left
        temp8 = self.look([-10, 10]);
        inputVector[21] = temp8[0];
        inputVector[22] = temp8[1];
        inputVector[23] = temp8[2];
        self.inputVector = inputVector

    def look(self, dir): #dir is a vector
        pos = np.array([self.snake.x, self.snake.y], dtype=float)
        dir = np.array(dir, dtype=float)
        vision = np.array([0]*3, dtype=float)
        distance = 1
        pos += dir
        
        foodFound = False
        tailFound = False

        while(not(pos[0] < 0 or pos[1] < 0 or pos[0] >= self.settings.xyMaxValue or pos[1] >= self.settings.xyMaxValue)):
#        while(not(pos[0] < 0 or pos[1] < 0 or pos[0] >= self.settings.windowSize or pos[1] >= self.settings.windowSize)):
            
            #check for food
            if(not foodFound and pos[0] == self.food.x and pos[1] == self.food.y):
                vision[0] = 1
                foodFound = True
            #check for tail
            if(not tailFound and self.isOnTail(pos)):
                vision[1] = 1/distance
                tailFound = True
            #reach wall
            pos += dir
            distance += 1
        vision[2] = 1 / distance
        return(vision) 

    def isOnTail(self, pos):
        for i in range(len(self.snake.tail)):
            if(pos[0] == self.snake.tail[i][0] and pos[1] == self.snake.tail[i][1]):
                return True
        return False

#dist((),())