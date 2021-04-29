import sys
import pygame
import pygame.gfxdraw
import random

'''
Alguns testes com o pygame.
Se rodar ele cria uma bolinha que oscila como um espectograma aleatório.

A FAZER:
Parametrizar isso.
Receber uma lista de frequencias, criar um limite superior acima da frequencia máxima,
criar um limite inferior abaixo da frequencia mínima, normalizar as frequencias com
base nesses novos limites e multiplicar pela metade da altura da janela (valor encontrado
em teste), dessa forma cria uma "margem" para que a bolinha não vá até os limites da
janela.

usar os valores dessa nova lista com o 'step' onde a bolinha vai parar.

Criar uma forma de deixar "rastro" (talvez com listas de imagens que mudam o alpha e
quando chega em alpha = 0 é removida da lista).
'''

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
	min_w = (W/2) + 10
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

	return circle

if __name__ == '__main__':
	pygame.init()

	info_object = pygame.display.Info()
	width = int(info_object.current_w/2)
	height = int(info_object.current_h/2)

	speed = [0, 1]
	black = 0, 0, 0

	screen = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()

	#MOCK
	'''
	N = random.randint(1, 400)
	mock = create_mock(N)
	circle = circle_settings(N, width/2)'''

	x = width / 4
	y = height / 2
	step = random.randint(0, height/2)
	while 1:
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT: sys.exit()

	    if x < 0 or x > width/2:
	        speed[0] = -speed[0]
	    if y < 0 or y > height/2:
	        speed[1] = -speed[1]
	    if y == step:
	    	speed[1] = -speed[1]
	    	step = random.randint(0, height/2)

	    screen.fill(black)
	    ball = pygame.draw.circle(screen, (255,0,0), (x, y), 20)
	    ball2 = pygame.draw.circle(screen, (0,0,255), (x, y), 20)
	    x += speed[0]
	    y += speed[1]
	    screen.blit(screen, ball)
	    screen.blit(screen, ball2)
	    pygame.display.flip()
	    clock.tick(200)
