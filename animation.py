import pygame
import pygame.gfxdraw
import random

def get_circle_settings(N, W, H, C):
	"""
	Generates the inicial settings for the balls to created on screen

	...

	Parameters
	----------
	N : int
		the number of extracted and processed tracks to be represented
		for the song
	W : int
		the screen width in pixels
	H : int
		the screen height in pixels
	C : [(int, int, int)]
		the list of n = 3 tuples of int representing the color scale

	Return
	------
	circle : dict
		a dictionary containing the colors, the radius, as well as the
		centers of each ball
	"""
	circle = {}

	color_rate = len(C)/N
	colors = []
	step = 0

	for i in range(N):
		colors.append(C[int(step)])
		step += color_rate

	max_w = (W) - 10
	min_w = 10
	rate = (max_w - min_w) / (N + 1)

	radius = min(10000, max(1, 0.4 * rate))

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
	"""
	Generates new values for the demo of visualization (USED FOR DEMO)

	...

	Parameters
	----------
	centers : [(float, float)]
		a list of n = 2 tuples of float representing the current centers
		of the balls (one for each track)
	H       : int
		the screen height in pixels

	Return
	------
	new_centers : [(float, float)]
		a list with the new values for the balls' positions
	"""
	new_centers = []
	for center in centers:
		x, y = center
		temp = tuple([x, random.uniform(max(0, y-75), min(H, y+75))])
		new_centers.append(temp)

	return new_centers

def color_list():
	"""
	Generates a list of 765 colors in RGB

	...

	Return
	------
	colors : [(int, int, int)]
		a list of n = 3 tuples representing the colors in RGB
	"""
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
	"""
	Generates a randomic color (USED FOR TESTING)

	...

	Return
	------
	_ : (int, int, int)
		a n = 3 tuple of int representing a color in RGB
	"""
	R = random.randint(0, 255)
	G = random.randint(0, 255)
	B = random.randint(0, 255)

	return (R, G, B)

def normalize_decibel(decibels, H):
	"""
	Responsible for normalizing the decibels in the screen height scale

	...

	Parameters
	----------
	decibels : [float]
		a list of float representing the decibels for each track being 
		visualized
	H        : int
		the screen height in pixels

	Return
	------
	n_decibels : [float]
		a list of float representing the decibel values in the new scale
	"""
	n_decibels = []
	for dec in decibels:
		dec = dec * (-1)
		value = (dec/80) * H
		n_decibels.append(value)

	return n_decibels


class Ball():
	"""
	Ball class, the chosen form for our visualization.

	...

	Attributes
	----------
	color    : (int, int, int)
		the color of the ball
	center_x : float
		the x value for the center of the ball (sphere)
	center_y : float
		the y value for the center of the ball (sphere)
	radius   : int
		the radius of the sphere in pixels

	Methods
	-------
	draw(screen, position_y)
		updates the y-value of the ball and print it on screen
	"""
	
	def __init__(self, color, center, radius):
		"""
		Parameters
		----------
		color  : (int, int, int)
			a n = 3 tuple of int representing the color of the ball in
			RGB format (varying from 0 to 255 on each dimension)
		center : (float, float)
			a n = 2 tuple of float representing x and y values for the
			center of the vball
		radius : int
			an int representing the radius of the sphere in pixels
		"""
		self.color = color
		self.center_x, self.center_y = center
		self.radius = radius

	def draw(self, screen, position_y):
		"""
		Updates the y value of the ball's center and draws it on its new
		position on the screen.

		...

		Parameters
		----------
		screen : pygame.Surface
			the surface (screen or window) where the ball will be drawn
		position_y : float
			the new height where the ball will be drawn, representing
			the decibel for that track

		Return
		------
		_ : pygame.Rect
			the drawing of the ball in its new position on the Surface
		"""
		self.center_y = position_y
		return pygame.draw.circle(screen, self.color, (self.center_x, self.center_y), self.radius)


if __name__ == '__main__':
	"""
	This script is responsible for the creation of the animation given
	a song in WAV format. It creates the animation using pygame library
	as well as librosa framework for music processing.

	It was created as a team project for the course IF754 - Computação
	Musical e Processamento de Som (Computational Music and Sound 
	Processing), taught by professor Giordano Cabral.
	"""
	N = 6000

	pygame.init()

	info = pygame.display.Info()
	win = pygame.display.set_mode((int(info.current_w), int(info.current_h)))
	pygame.display.set_caption("Nome da Música")

	#Detalhes da bola
	colors = color_list()
	circle_settings = get_circle_settings(N, int(info.current_w), int(info.current_h), colors)
	y = info.current_h - circle_settings['radius'] - 100 #valor 100 eh experimental
	speed = 2
	centers = []
	balls = []

	#count = 0

	run = True
	first_loop = True
	while run:
		pygame.time.delay(80)

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
			#balls[i].color = colors[count % 766]
			balls[i].draw(win, centers[i][1])
		pygame.display.update()
		#count += 1

	pygame.quit()