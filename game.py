import pygame,sys
import random

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

BALL_SIZE = 15
TITLE = 'GAME'

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL_COLOR = (167, 241, 232)
BALL_COLOR = (196, 211, 208)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('monospace', 26)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

OBSTACLE_WIDTH = 75
OBSTACLE_GAP = 150

background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

class Obstacle:
    def __init__(self):
        # start Y position of obstacle
        self.posY = -OBSTACLE_WIDTH

        # End X position of obstacle part 1
        self.gapX = random.randint(0, WINDOW_WIDTH - OBSTACLE_GAP)


# PRESS SPACE TO CHANGE DIRECTION
class Game:
    def __init__(self, FPS=None):
        self.FPS = FPS
        self.speedX = 5
        self.speedY = 3
        self.accelerationX = 0.3
        self.accelerationY = 0.3
        # interval at which new obstacle is generated
        self.interval = 80
        self.count = self.interval
        self.score = 0
        # to avoid multi clicks

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
        pygame.draw.circle(screen, color, (int(self.posX), int(self.posY)), BALL_SIZE)
        # screen.blit(ball_image, (self.posX, self.posY))

    # draws all the obstacles
    def _drawObstacles(self, color=WHITE):
        for i in self.obstacles:
            rect = pygame.Rect(0, i.posY, i.gapX, OBSTACLE_WIDTH)
            pygame.draw.rect(screen, color, rect)

            rect = pygame.Rect(i.gapX + OBSTACLE_GAP, i.posY, WINDOW_WIDTH, OBSTACLE_WIDTH)
            pygame.draw.rect(screen, color, rect)

    # call this function each step to view the game
    def render(self):
        pygame.display.flip()
        # screen.fill(BLACK)

        if self.FPS:
            clock.tick(self.FPS)

        screen.blit(background_image, (0, 0))
        self._drawBall(BALL_COLOR)
        self._drawObstacles(WALL_COLOR)
        textsurface = myfont.render("Score: "+str(self.score), False, (0, 0, 0))
        screen.blit(textsurface,(260,0))


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
        if(int(self.obstacles[0].posY) < int(self.posY) and  int(self.obstacles[0].posY)+OBSTACLE_WIDTH > int(self.posY) and (int(self.posX) < int(self.obstacles[0].gapX) or int(self.posX) > int(self.obstacles[0].gapX) + OBSTACLE_GAP)):
            return True

    def _boundaryHit(self):
        if(self.posX < 0 or self.posX > WINDOW_WIDTH):
            return True
    # adds and removes obstacles
    def _manageObstacles(self):
        if self.count == self.interval:
            self.obstacles.append(Obstacle())
            self.count = 0
        else:
            self.count += 1

        if self.obstacles[0].posY >= WINDOW_HEIGHT:
            self.obstacles.pop(0)
            self.speedX+=self.accelerationX
            self.speedY+=self.accelerationY
            self.score+=1

    # performs a step based on the given action
    def step(self):

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    self.direction = not self.direction
        self._updatePos()
        self._manageObstacles()
        if self._detectCollisions():
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
