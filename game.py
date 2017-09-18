import pygame
import random

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

BALL_SIZE = 15
TITLE = 'GAME'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

OBSTACLE_WIDTH = 75
OBSTACLE_GAP = 150


class Obstacle:
	def __init__(self):
		#start Y position of obstacle
		self.posY = -OBSTACLE_WIDTH
		#End X postition of obstacle part 1
		self.gapX = random.randint(0, WINDOW_WIDTH - OBSTACLE_GAP)


#PRESS SPACE TO CHANGE DIRECTION
class Game:
	def __init__(self, FPS=None):
		self.FPS = FPS
		self.speedX = 5
		self.speedY = 3

		#interval at which new obstacle is generated
		self.interval = 80
		self.count = self.interval

		#to avoid multi clicks
		self.buffer = 4


	#reinitializes the game 
	def reset(self):
		self.done = False
		self.score = 0

		#initial possitions
		self.posX = int(WINDOW_WIDTH/2)
		self.posY = WINDOW_HEIGHT - 100

		#direction: 0 = left and 1 = right
		self.direction = 0
		self.obstacles = []


	#draws the player's ball
	def _drawBall(self, color = WHITE):
		pygame.draw.circle(screen, color, (self.posX, self.posY), BALL_SIZE)


	#draws all the obstacles
	def _drawObstacles(self, color = WHITE):
		for i in self.obstacles:
			rect = pygame.Rect(0, i.posY, i.gapX, OBSTACLE_WIDTH)
			pygame.draw.rect(screen, color, rect)

			rect = pygame.Rect(i.gapX + OBSTACLE_GAP, i.posY, WINDOW_WIDTH, OBSTACLE_WIDTH)
			pygame.draw.rect(screen, color, rect)


	#call this function each step to view the game
	def render(self):
		pygame.display.flip()
		screen.fill(BLACK)
		if self.FPS:
			clock.tick(self.FPS)

		self._drawBall()
		self._drawObstacles()


	#updates pos of ball and obstacles
	def _updatePos(self):

		if self.direction:
			self.posX += self.speedX
		else:
			self.posX -= self.speedX

		for i in self.obstacles:
			i.posY += self.speedY


	#if action == 1, changes direction
	#if action == 0, continue to move in the same direction 
	def _move(self, action):

		# if action: 
		# 	self.direction = not self.direction

		#for manual input, press key SPACE
		key = pygame.key.get_pressed()
		if self.buffer == 4:
			if key[pygame.K_SPACE]:
				self.direction = not self.direction
			self.buffer = 0
		else:
			self.buffer += 1

		self._updatePos()


	#detects collision with boundries and obstacles
	#to be implemented
	def _detectCollisions(self):		
		return False
		

	#adds and removes obstacles
	def _manageObstacles(self):
		if self.count == self.interval:
			self.obstacles.append(Obstacle())
			self.count = 0
		else: 
			self.count += 1

		if self.obstacles[0].posY >= WINDOW_HEIGHT:
			self.obstacles.pop(0)


	#performs a step based on the given action
	def step(self, action):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
			    self.close()

		self._manageObstacles()

		self._move(action)

		if self._detectCollisions():
			self.done = True
			self.close()


	#exits the game
	def close(self):
		pygame.quit()
		exit(0)


env = Game(60)
env.reset()

for _ in range(1000):
	env.step(0)
	env.render()
