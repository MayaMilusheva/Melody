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

	def __init__(self, note_def):
		self.filename = note_def['filename']
		self.duration = note_def['duration']
		self.sample = pySonic.FileSample(self.filename)
		self.source = pySonic.Source()
		Note.all.append(self)

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
			Track.get().addNote(self.note)

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
		self.notes = [Note.get(note) for note in self.notes]

	def play(self):
		if len(self.notes) == 0:
			return
		self.playing = pygame.time.get_ticks()
		self.curNote = 0
		self.notes[self.curNote].play()

	def update(self):
		if not self.playing:
			return
		start = self.playing
		now = pygame.time.get_ticks()

		oldNote = self.notes[self.curNote]
		if now - start < oldNote.duration:
			return

		self.curNote += 1
		self.playing = now
		if self.curNote >= len(self.notes):
			self.playing = False
		else:
			oldNote.stop()
			newNote = self.notes[self.curNote]
			newNote.play()

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, self.radius)

	def onClick(self, pos):
		if distSq(pos, self.pos) <= self.radius * self.radius:
			self.play()

class Track(GameObject):
	instance = None
	@staticmethod
	def get():
		return Track.instance

	def __init__(self, definition):
		if Track.instance:
			raise 'Trying to create two instances of a singleton.'
		Track.instance = self
		GameObject.__init__(self, definition)
		self.color = pygame.color.Color(0, 0, 255)
		self.melody = Melody({
			'pos': (self.pos[0], self.pos[1] + self.size[1] / 2),
			'radius': self.size[1] / 2,
			'notes': []
		})

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.pos, self.size))
		for index, note in enumerate(self.melody.notes):
			pygame.draw.circle(surface, pygame.color.Color(0, 255, 255), (index*100, self.pos[1] +50), 50)
		

	def addNote(self, note):
		self.melody.notes.append(note)

	def removeNote(self, note):
		pass

	def onClick(self, pos):
		inX = pos[0] >= self.pos[0] and pos[0] <= self.pos[0] + self.size[0]
		inY = pos[1] >= self.pos[1] and pos[1] <= self.pos[1] + self.size[1]
		if inX and inY:
			print 'clicked!'
