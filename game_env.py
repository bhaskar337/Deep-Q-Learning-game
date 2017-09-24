import pygame
import random
import cv2


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
OBSTACLE_WIDTH = 75

#radius of ball
BALL_SIZE = 15

TITLE = 'GAME'

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


class Obstacle:
    def __init__(self):
        #gap between the 2 corresponding obstacles
        self.obstacle_gap = random.choice([150, 200, 250])
        # start Y position of obstacle
        self.posY =  -OBSTACLE_WIDTH
        # End X position of obstacle part 1
        self.gapX = random.choice([50, 100])


class Game:
    def __init__(self, FPS=None):
        self.FPS = FPS

        #the speed of x is accelerates when direction is not changed
        #and is reinitialized when direction is changed
        self.accelerationX = 0.2
        self.speedXInit = 3

        self.speedY = 4
        # interval at which new obstacle is generated
        self.interval = 70


    # re-initializes the game
    def reset(self):
        self.done = False
        self.score = 0

        # initial positions
        self.posX = int(WINDOW_WIDTH / 2)
        self.posY = WINDOW_HEIGHT - 100

        # d irection: 0 = left and 1 = right
        self.direction = random.choice([0,1])
        self.obstacles = []

        self.speedX = self.speedXInit
        self.count = self.interval
        self.passObstacle = False

        #pixel array of the game
        self.state = pygame.surfarray.pixels3d(pygame.display.get_surface())



    # draws the player's ball
    def _drawBall(self):
        pygame.draw.circle(screen, WHITE, (self.posX, self.posY), BALL_SIZE)


    # draws all the obstacles
    def _drawObstacles(self):
        for i in self.obstacles:
            if i.gapX != 0:
                rect = pygame.Rect(0, i.posY, i.gapX, OBSTACLE_WIDTH)
                pygame.draw.rect(screen, WHITE, rect)   
            if i.gapX + i.obstacle_gap != WINDOW_WIDTH:    
                rect = pygame.Rect(i.gapX + i.obstacle_gap, i.posY, WINDOW_WIDTH, OBSTACLE_WIDTH)
                pygame.draw.rect(screen, WHITE, rect)       

         
    #draws the game screen with given FPS
    def _render(self):
        pygame.display.flip()
        screen.fill(BLACK)
        if self.FPS:
            clock.tick(self.FPS)

        self._drawBall()
        self._drawObstacles()
       

    # updates pos of ball and obstacles
    def _updatePos(self, action):
        if action:
            self.direction = not self.direction
            self.speedX = self.speedXInit
        else:
            self.speedX += self.accelerationX

        if self.direction:
            self.posX = int(self.posX + self.speedX)
        else:
            self.posX = int(self.posX - self.speedX)

        for i in self.obstacles:
            i.posY = int(i.posY + self.speedY)


    # detects collision with boundries and obstacles
    def _detectCollisions(self):
        if ((self.obstacles[0].posY - BALL_SIZE) < self.posY < (self.obstacles[0].posY + OBSTACLE_WIDTH + BALL_SIZE)) and ((self.posX - BALL_SIZE) < self.obstacles[0].gapX  or (self.posX + BALL_SIZE) > (self.obstacles[0].gapX + self.obstacles[0].obstacle_gap)):
            return True

        if self.posX < BALL_SIZE or self.posX > WINDOW_WIDTH - BALL_SIZE:
            return True


    # adds and removes obstacles
    # returns True if 0th obstacle is passed
    def _manageObstacles(self):
        if self.count >= self.interval:
            self.obstacles.append(Obstacle())
            self.count = 0
        else:
            self.count += 1

        if self.obstacles[0].posY >= WINDOW_HEIGHT:
            obs = self.obstacles.pop(0)
            self.passObstacle = False

        elif not self.passObstacle and (self.obstacles[0].posY + OBSTACLE_WIDTH/2) > self.posY:
            self.score += 1   
            self.passObstacle = True
            return True

        return False 


    #returns reshaped 80 x 80 game state 
    def _getState(self):
        state = cv2.cvtColor(cv2.resize(self.state, (80, 80)), cv2.COLOR_BGR2GRAY)
        _, state = cv2.threshold(state, 1, 255,cv2.THRESH_BINARY)
        return state.T


    # performs a step based on the given action
    def step(self, action):


        #reward = 0.1 if alive
        #reward = 1 if cross centre of 0th obstacle
        #reward = -1 if collide with obstacle/boundry
        reward = 0.1

        #stacking up 4 game frames
        actions = [action, 0, 0, 0]
        state = []
        for i in actions: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.close()

            self._updatePos(i)

            if self._manageObstacles():
                reward = 1
           
            if self._detectCollisions():
                reward = -1
                self.done = True

            state.append(self._getState())
            self._render()

        return state, reward, self.done, self.score


    # exits the game
    def close(self):
        pygame.quit()
        exit(0)


