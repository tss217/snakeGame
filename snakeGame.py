
import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font("arial.ttf",25)

class Direction(Enum): #enumeradores
    RIGHT = 1
    LEFT =2
    UP = 3
    DOWN= 4

point = namedtuple("point","x,y") # tuplas nomeadas.
BLOCKSIZE = 20
SPEED = 20
BLACK = (0,0,0)
WHITE = (225,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)

class snakeGame:
    def __init__(self, width = 640, high = 480):
        self.width = width
        self.high = high

        #display
        self.display = pygame.display.set_mode((self.width,self.high))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock() #fps 

        #init state
        self.direction = Direction.RIGHT
        self.snakeHead = point(self.width/2,self.high/2)
        self.snake = [self.snakeHead,
                      point(self.snakeHead.x-BLOCKSIZE,self.snakeHead.y),
                      point(self.snakeHead.x-(2*BLOCKSIZE),self.snakeHead.y)]
        
        #score

        self.score = 0
        self.food = None
        self.placeFood()

    def placeFood(self):
        x = random.randint(0,(self.width-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        y = random.randint(0,(self.high-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        self.food = point(x,y)

        if self.food in self.snake:
            self.placeFood()

    def playStep(self):
        # collect the user input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move

        self.move(self.direction)
        self.snake.insert(0, self.snakeHead)

        # check if game over 
        gameOver = False

        if self.collision():
            gameOver = True
            return gameOver, self.score
                   
                   
         # place new food or just move

        if self.snakeHead == self.food:
            self.score += 1
            self.placeFood()
        else:
            self.snake.pop()

        # update ui and clock 
        self.updateUi()
        self.clock.tick(SPEED)

        # return game over and score
        return gameOver, self.score
        
        
    def collision(self):
        if self.snakeHead.x > self.width-BLOCKSIZE or self.snakeHead.x <0 or self.snakeHead.y > self.high - BLOCKSIZE or self.snakeHead.y <0 :
            return True
        if self.snakeHead in self.snake[1:]:
            return True
        
        return False

    def updateUi(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))



        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE,BLOCKSIZE))

        text = font.render("score:"+ str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()


    def move(self,direction):
        x = self.snakeHead.x
        y = self.snakeHead.y

        if direction == Direction.LEFT:
            x-= BLOCKSIZE
        elif direction == Direction.RIGHT:
            x+= BLOCKSIZE
        elif direction == Direction.UP:
            y-= BLOCKSIZE
        elif direction == Direction.DOWN:
            y+= BLOCKSIZE

        self.snakeHead = point(x,y)

if __name__ == "__main__":
    game = snakeGame()

    #gameLoop

    while True:
        gameOver, score = game.playStep()

        if gameOver == True:
            break
    
    print("final score",score)

        #break

    pygame.quit()