import pygame
import random

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
pygame.font.init()
myfont = pygame.font.SysFont('monospace', 26)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


class Obstacle:
    def __init__(self):
        # start Y position of obstacle
        self.obstacle_gap = random.choice([150, 200, 250])
        self.posY =  -OBSTACLE_WIDTH
        # End X position of obstacle part 1
        self.gapX = random.choice([0, 50, 100, 150])


# PRESS SPACE TO CHANGE DIRECTION
class Game:
    def __init__(self, FPS=None):
        self.FPS = FPS

        self.accelerationX = 0.05
        self.accelerationY = 0.2
        self.terminalVelociy = 7

        # interval at which new obstacle is generated
        self.interval = 90


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

        self.speedX = 5
        self.speedY = 3

        self.count = self.interval
        self.passObstacle = False



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

         

    # call this function each step to view the game
    def render(self):
        pygame.display.flip()
        screen.fill(BLACK)
        if self.FPS:
            clock.tick(self.FPS)

        self._drawBall()
        self._drawObstacles()

        textsurface = myfont.render("Score: " + str(self.score), False, WHITE)
        screen.blit(textsurface,(240,0))
       

    # updates pos of ball and obstacles
    def _updatePos(self, action):
        if action:
            self.direction = not self.direction
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
    def _manageObstacles(self):
        if self.count >= self.interval:
            self.obstacles.append(Obstacle())
            self.count = 0
        else:
            self.count += 1

        if self.obstacles[0].posY >= WINDOW_HEIGHT:
            obs = self.obstacles.pop(0)
            if self.speedY <= self.terminalVelociy:
                self.speedY += self.accelerationY
                self.interval = int((self.speedY*self.interval)/(self.speedY + self.accelerationY))
            self.passObstacle = False

        elif not self.passObstacle and (self.obstacles[0].posY + OBSTACLE_WIDTH/2) > self.posY:
            self.score += 1   
            self.passObstacle = True
            return 1  

        return 0.1       


    # performs a step based on the given action
    def step(self, action):
        self._updatePos(action)
        reward = self._manageObstacles()
       
        if self._detectCollisions():
            reward = -1
            self.done = True

        state = pygame.surfarray.array2d(pygame.display.get_surface())
        state[state > 0] = 255

        return state, reward, self.done


    # exits the game
    def close(self):
        pygame.quit()
        exit(0)


env = Game(60)
env.reset()
done = False

while True:

    action = 0
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            env.close()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                action = 1

    state, reward, done = env.step(action)
    env.render()

    if done:
        break

