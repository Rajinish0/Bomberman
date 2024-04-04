import pygame
from functools import cache
from utils import resetCursor
from singleton import Singleton

'''
Singleton class (so that we can use it anywhere in the program)
curState - current screen
prevState - previous screen

setState - set the current state to some state
setState has to call resetCursor() because when a button is pressed to change the state (change the screen)
that button is no longer there to reset the cursor, so it must be done here.
'''
class GameStateMgr(Singleton):
	def __init__(self):
		self.curState = None
		self.prevState = None
		self.game_window_file_path = None

	def setState(self, state):
		resetCursor()
		self.prevState = self.curState
		self.curState = state
	
	def getState(self):
		return self.curState

	def getPrevState(self):
		return self.prevState

	def set_game_window_file_path(self, file_path):
		self.game_window_file_path = file_path
	def get_game_window_file_path(self):
		return self.game_window_file_path

class EventMgr(Singleton):
	def __init__(self):
		self.mousePressed = False
	
	def setMousePressed(self, t):
		self.mousePressed = True

	def reset(self):
		self.mousePressed = False




'''
a cached class for loading images, alternatively this could also be just a single cached function in utils.
'''
class ImageHandler(Singleton):
	
	def __init__(self):
		pass

	@cache	
	def load(self, img, dimensions):
		w, h = dimensions
		img = pygame.image.load(img)
		img = pygame.transform.scale(img, (w, h))
		return img	
	
