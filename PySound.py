import pygame
import pySonic
import time

from Game import *
from pygame.locals import *

size = (640, 480)
pygame.init()
screen = pygame.display.set_mode(size)

world = pySonic.World()
start = pygame.time.get_ticks()
clock = pygame.time.Clock()
now = start
done = False

def handle_events():
	'''
	Returns true when the game should stop.
	'''
	while True:
		ev = pygame.event.poll()
		if ev.type == pygame.NOEVENT:
			return False
		if ev.type == pygame.QUIT:
			return True
		if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
			for obj in GameObject.all:
				obj.onClick(ev.pos)

def init_objects(data):
	for note_def in data['notes']:
		Note(note_def)
	for bubble_def in data['bubbles']:
		Bubble(bubble_def)
	Melody(data['melody'])
	Track(data['track'])

data = syck.load(open('melody.yml'))
init_objects(data)

while not done:
	delta = clock.tick()
	now += delta
	for obj in GameObject.all:
		obj.update()
	for obj in GameObject.all:
		obj.draw(screen)
	pygame.display.flip()
	done = handle_events()
