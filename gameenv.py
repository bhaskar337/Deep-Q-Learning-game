import pygame,sys
import random
import time
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600


TITLE = 'GAME'

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BALL_COLOR = (196, 211, 208)
POWERUPOBS_COLOR = (0, 200, 0)
POWERUPOBS_COLOR2 = (200, 0, 0)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('monospace', 26)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

OBSTACLE_WIDTH = 75
TIME_INTERVAL = 5
background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

class Obstacle:
    def __init__(self,color):
        # start Y position of obstacle
        self.OBSTACLE_GAP = random.choice([150, 200, 250])
        self.posY = -OBSTACLE_WIDTH
        self.color = color
        # End X position of obstacle part 1
        self.gapX = random.choice([0, 50, 100, 150, 200, 250])


# PRESS SPACE TO CHANGE DIRECTION
class Game:
    def __init__(self, FPS=None):
        self.FPS = FPS
        self.BALL_SIZE = 15
        self.WALL_COLOR = (167, 241, 232)
        self.speedX = 5
        self.speedY = 3
        self.accelerationX = 0.04
        self.accelerationY = 0.2
        self.small = None
        self.terminalVelociy = 7
        # interval at which new obstacle is generated
        self.interval = 80
        self.intervalFloat = 80
        self.count = self.interval
        self.score = 0
        self.collisionson = True
        self.collisionstime = None

        self.isPowerUp = False

    # re-initializes the game
    def reset(self):
        self.done = False
        self.score = 0

        # initial positions
        self.posX = int(WINDOW_WIDTH / 2)
        self.posY = WINDOW_HEIGHT - 100

        # d irection: 0 = left and 1 = right
        self.direction = 0
        self.obstacles = []

    # draws the player's ball
    def _drawBall(self, color=WHITE):
        pygame.draw.circle(screen, color, (int(self.posX), int(self.posY)), self.BALL_SIZE)
        # screen.blit(ball_image, (self.posX, self.posY))

    # draws all the obstacles
    def _drawObstacles(self):
        for i in self.obstacles:
            rect = pygame.Rect(i.gapX + i.OBSTACLE_GAP, i.posY, WINDOW_WIDTH, OBSTACLE_WIDTH) 
            pygame.draw.rect(screen, i.color, rect, 4) 

    # call this function each step to view the game
    def render(self):
        pygame.display.flip()
        # screen.fill(BLACK)
        
        if self.FPS:
            clock.tick(self.FPS)
        if self.small != None and time.time() - self.small >= TIME_INTERVAL:
            self.BALL_SIZE = 15
        if not self.collisionson and time.time() - self.collisionstime >= TIME_INTERVAL:
            self.collisionson = True
            self.WALL_COLOR = (167, 241, 232)
            for i in self.obstacles:
                    i.color = self.WALL_COLOR
        screen.blit(background_image, (0, 0))
        self._drawBall(BALL_COLOR)
        self._drawObstacles()
        textsurface = myfont.render("Score: "+str(self.score), False, (0, 0, 0))
        screen.blit(textsurface,(260,0))
        if not self.collisionson:
            textsurface = myfont.render("Invulnerable: "+str(round(TIME_INTERVAL - (time.time() - self.collisionstime),2)), False, (0, 0, 0))
            screen.blit(textsurface,(120,40))
        if self.BALL_SIZE == 8:
            textsurface = myfont.render("Small Size: "+str(round(TIME_INTERVAL - (time.time() - self.small),2)), False, (0, 0, 0))
            if not self.collisionson:
                screen.blit(textsurface,(120,20))
            else:
                screen.blit(textsurface,(120,40))

    # updates pos of ball and obstacles
    def _updatePos(self):

        if self.direction:
            self.posX += self.speedX
        else:
            self.posX -= self.speedX

        for i in self.obstacles:
            i.posY += self.speedY

    # detects collision with boundries and obstacles
    # to be implemented
    def _detectCollisions(self):
        if(int(self.obstacles[0].posY) < int(self.posY) and  int(self.obstacles[0].posY)+OBSTACLE_WIDTH > int(self.posY) and (int(self.posX) < int(self.obstacles[0].gapX) or int(self.posX) > int(self.obstacles[0].gapX) + self.obstacles[0].OBSTACLE_GAP)):
            return True

    def _boundaryHit(self):
        if(self.posX < 0 or self.posX > WINDOW_WIDTH):
            return True
    # adds and removes obstacles
    def _manageObstacles(self):
        if self.count >= self.interval:
            prob = random.uniform(0,1)
            if prob > 0.2:
                self.obstacles.append(Obstacle(self.WALL_COLOR))
            elif prob <=0.2 and prob > 0.1:
                self.obstacles.append(Obstacle(POWERUPOBS_COLOR2))
            else:
                self.obstacles.append(Obstacle(POWERUPOBS_COLOR))
            self.count = 0
        else:
            self.count += 1

        if self.obstacles[0].posY >= WINDOW_HEIGHT:
            obs = self.obstacles.pop(0)
            if self.speedY <= self.terminalVelociy:
                self.speedY+=self.accelerationY
                self.interval=round((self.speedY*self.interval)/(self.speedY + self.accelerationY))
            self.isPowerUp = False

        if self.obstacles[0].posY >= self.posY and not self.isPowerUp:
            if (self.obstacles[0].color == POWERUPOBS_COLOR):
                self.BALL_SIZE = 8
                self.small = time.time()
            elif (self.obstacles[0].color == POWERUPOBS_COLOR2):
                self.collisionson = False
                self.collisionstime = time.time()
                self.WALL_COLOR = BLACK
                for i in self.obstacles:
                    i.color = BLACK

            self.score+=1            
            self.isPowerUp = True


    # performs a step based on the given action
    def step(self):

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    self.direction = not self.direction
                    self.speedX+=self.accelerationX
        self._updatePos()
        self._manageObstacles()
        if self.collisionson and self._detectCollisions():
            self.done = True
            self.close()
        if self._boundaryHit():
            self.done = True
            self.close()

    # exits the game
    def close(self):
        pygame.quit()
        exit(0)


env = Game(60)
env.reset()

while(True):
    env.step()
    env.render()
