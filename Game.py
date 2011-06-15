import pygame
import syck
import pySonic

def distSq(pa, pb):
	dx = (pa[0] - pb[0])
	dy = (pa[1] - pb[1])
	return dx * dx + dy * dy	

class GameObject(object):
	all = set()
	def __init__(self, definition):
		for key, val in definition.items():
			self.__dict__[key] = val
		GameObject.all.add(self)

	def update(self):
		pass

	def draw(self, surface):
		pass

	def onClick(self, pos):
		pass

class Note(object):
	'''
	A note that can be played.
	While its playing, it can also be stopped.
	'''
	all = []
	@staticmethod
	def get(index):
		return Note.all[index]

	def __init__(self, filename):
		Note.all.append(self)
		self.sample = pySonic.FileSample(filename)
		self.source = pySonic.Source()

	def play(self):
		if self.source.IsPlaying():
			self.source.Stop()
		self.source.Sound = self.sample
		self.source.Play()

	def stop(self):
		if self.source.IsPlaying():
			self.source.Stop()

class Bubble(GameObject):
	'''
	An object that appears on the screen as a bubble.
	When the player clicks on it, a sound is played.
	'''
	def __init__(self, definition):
		GameObject.__init__(self, definition)
		self.color = pygame.color.Color(255, 255, 255)
		self.note = Note.get(self.note_index)

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, self.radius)

	def play(self):
		self.note.play()

	def onClick(self, pos):
		if distSq(pos, self.pos) <= self.radius * self.radius:
			self.play()

class Melody(GameObject):
	'''
	An object representing a sequence of notes.
	When it is played, its notes are played in order.
	It's represented as a clickable button.
	'''
	def __init__(self, definition):
		GameObject.__init__(self, definition)
		self.color = pygame.color.Color(255, 0, 0)
		self.playing = False
		self.curNote = 0

	def play(self):
		self.playing = pygame.time.get_ticks()
		self.curNote = 0
		Note.get(self.notes[self.curNote]['note']).play()

	def update(self):
		if not self.playing:
			return
		start = self.playing
		now = pygame.time.get_ticks()

		note_def = self.notes[self.curNote]
		if now - start > note_def['duration']:
			self.curNote += 1
			self.playing = now
			if self.curNote >= len(self.notes):
				self.playing = False
			else:
				Note.get(note_def['note']).stop()
				Note.get(self.notes[self.curNote]['note']).play()

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, self.radius)

	def onClick(self, pos):
		if distSq(pos, self.pos) <= self.radius * self.radius:
			self.play()
