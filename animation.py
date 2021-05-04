import pygame
import pygame.gfxdraw
import random

def get_circle_settings(N, W, H, C):
	circle = {}

	color_rate = len(C)/N
	colors = []
	step = 0

	for i in range(N):
		colors.append(C[int(step)])
		step += color_rate
	
	color = (127,0,127)
	max_w = (W) - 10
	min_w = 10
	rate = (max_w - min_w) / (N + 1)

	radius = min(20, max(1, 0.4 * rate))

	min_value = min_w
	centers = []
	for i in range(N):
		min_value += rate
		center = (min_value, H - radius - 100)
		centers.append(center)

	circle['colors'] = colors
	circle['radius'] = int(radius)
	circle['centers'] = centers

	return circle

def get_new_centers(centers, H):
	new_centers = []
	for center in centers:
		x, y = center
		temp = tuple([x, random.uniform(max(0, y-75), min(H, y+75))])
		new_centers.append(temp)

	return new_centers

def color_matrix():
	step = 1
	colors = []
	color = (255,0,0)

	colors.append(color)
	for i in range(3):
		for j in range(255):
			if i == 0:
				new_color = tuple([color[0]-1, color[1]+1, color[2]])
			elif i == 1:
				new_color = tuple([color[0], color[1]-1, color[2]+1])
			elif i == 2:
				new_color = tuple([color[0]+1, color[1], color[2]-1])
			colors.append(new_color)
			color = new_color

	return colors

def get_color():
	R = random.randint(0, 255)
	G = random.randint(0, 255)
	B = random.randint(0, 255)

	return (R, G, B)

def normalize_decibel(decibels, H):
	n_decibels = []
	for dec in decibels:
		dec = dec * (-1)
		value = (dec/80) * H
		n_decibels.append(value)

	return n_decibels


class Ball():

	def __init__(self, color, center, radius):
		self.color = color
		self.center_x, self.center_y = center
		self.radius = radius

	def draw(self, screen, position_y):
		self.center_y = position_y
		return pygame.draw.circle(screen, self.color, (self.center_x, self.center_y), self.radius)


if __name__ == '__main__':
	N = 50

	pygame.init()

	info = pygame.display.Info()
	win = pygame.display.set_mode((int(info.current_w), int(info.current_h)))
	pygame.display.set_caption("Nome da Música")

	#Detalhes da bola
	colors = color_matrix()
	circle_settings = get_circle_settings(N, int(info.current_w), int(info.current_h), colors)
	y = info.current_h - circle_settings['radius'] - 100 #depois remover o 100
	speed = 2
	centers = []
	balls = []

	run = True
	first_loop = True
	while run:
		pygame.time.delay(100)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		if first_loop:
			for i in range(N):
				ball = Ball(circle_settings['colors'][i],
					circle_settings['centers'][i],
					circle_settings['radius'])
				balls.append(ball)
				balls[i].draw(win, y)
			first_loop = False
			centers = circle_settings['centers']
			
		else:
			centers = get_new_centers(centers, y)

		#win.fill(get_color())
		win.fill((0,0,0))
		for i in range(N):
			balls[i].draw(win, centers[i][1])
		pygame.display.update()

	pygame.quit()