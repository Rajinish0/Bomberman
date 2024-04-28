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

	def setState(self, state):
		resetCursor()
		self.prevState = self.curState
		self.curState = state
	
	def getState(self):
		return self.curState

	def getPrevState(self):
		return self.prevState

	def get_game_window_file_path(self):
		print(self.game_window_file_path)
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

class SpriteSheet:
	def __init__(self, sheetImage : str, width : int, height : int,
				 numActions : int, numImagesPerAction : int,
				 scaleSize : tuple = None, animationCoolDown = 100,
				 defaultAction = 0, defaultActionFrame = 0):
		self.image = pygame.image.load(sheetImage).convert_alpha()
		self.width  = width
		self.height = height
		self.numActions = numActions
		self.numImagesPerAction = numImagesPerAction
		self.scaleW, self.scaleH = scaleSize or (width, height)
		self.curAction = defaultAction
		self.curActionFrame = defaultActionFrame
		self.lastTime = pygame.time.get_ticks()
		self.animationCoolDown = animationCoolDown

	def setAction(self, action):
		assert action < self.numActions #for debugging
		if self.curAction != action:
			self.curActionFrame = 0
		else:
			self.update()
		self.curAction = action

	def update(self):
		curTime = pygame.time.get_ticks()
		if curTime - self.lastTime >= self.animationCoolDown:
			self.curActionFrame = ( self.curActionFrame + 1 ) % self.numImagesPerAction
			self.lastTime = curTime

	def getImage(self):
		imgSurface = pygame.Surface( (self.width, self.height), pygame.SRCALPHA )
		imgSurface.blit( self.image, (0, 0), ( self.curActionFrame*self.width,
											   self.curAction*self.height,
											   self.width, self.height ) )
		return pygame.transform.scale(imgSurface, (self.scaleW, self.scaleH) )
	
