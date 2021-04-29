import sys
import pygame
import pygame.gfxdraw
import random

class Figure(): #vai ser a bolinha em si + o rastro

	def __init__(self):
		pass

class Animation(): # o que vai fazer com que a bolinha se movimente com base nas frequencias

	def __init__(self):
		pass

def create_mock(N):
	mock = {}
	steps = 100
	decibels = []

	for i in range(N):
		decibels_level = []
		for j in range(steps):
			temp = random.randint(-80, 0)
			decibels_level.append(temp)
		decibels.append(decibels_level)

	mock['N'] = N
	mock['steps'] = steps
	mock['decibels'] = decibels

	return mock

def circle_settings(N, W):
	circle = {}

	color = (255,0,0)
	max_w = (W/2) - 10
	min_w = 1
	rate = (max_w - min_w) / (N + 1)

	min_value = min_w
	centers = []
	for i in range(N):
		min_value += rate
		centers.append(min_value)

	radius = min(20, 0.4 * rate)

	circle['color'] = color
	circle['radius'] = int(radius)
	circle['centers'] = centers
	print(centers)
	for i in range(len(centers)):
		if i < len(centers)-1:
			print(centers[i+1] - centers[i])


	return circle

class Screen():

	def __init__(self, width, height):
		self.width = width
		self.height = height

class Ball():

	def __init__(self, color, center, radius):
		self.color = color
		self.center_x, self.center_y = center
		self.radius = radius

	def draw(self, screen, position_y):
		self.center_y = position_y
		return pygame.draw.circle(screen, self.color, (self.center_x, self.center_y), self.radius)

if __name__ == '__main__':
	pygame.init()

	info_object = pygame.display.Info()
	width = int(info_object.current_w/2)
	height = int(info_object.current_h/2)

	speed = [0, 1]
	black = 0, 0, 0

	screen = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()
	#screen.fill(black)

	#MOCK
	
	#N = random.randint(1, 10)
	N= 5
	print(N)
	mock = create_mock(N)
	circle = circle_settings(N, width/2)
	
	x = width / 4
	y = height / 2
	step = random.randint(0, height/2)

	balls = []
	for i in range(N):
		balls.append(Ball(circle['color'], (circle['centers'][i], y), circle['radius']))
	print('criou as bolas.')

	while 1:
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT: sys.exit()

	    if y <= 0 or y >= height/2:
	        speed[1] = -speed[1]
	    if y == step:
	    	speed[1] = -speed[1]
	    	step = random.randint(0, height/2)

	    screen.fill(black)
	    for i in range(N):
	    	balls[i].draw(screen, y)
	    y += speed[1]

	    for i in range(N):
	    	screen.blit(screen, balls[i].draw(screen, y))

	    pygame.display.flip()
	    clock.tick(200)
