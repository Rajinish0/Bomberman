import pygame, sys
from handlers import *
from constants import *
from screens import *
from screens.mapwindow import MapWindow

pygame.init()

'''
Sets up the display that everything is going to be drawn on.
states are basically different screens(windows) that can be drawn at a given moment
this class gets the current state (screen) from the GameStateManager and updates and draws it every frame
'''
class Main:
	def __init__(self):
		self.display = pygame.display.set_mode((W, H))
		self.clock = pygame.time.Clock()
		self.run = True
		self.gameMgr = GameStateMgr()
		self.eventMgr = EventMgr()
		self.init()
		self.pressed_key = None

	'''
	this gets the events from the display. If the mouse button was pressed
	then the event manager's mousePressed is set to true, this makes it easy to access
	if mouse was pressed through out the whole program (just query eventMgr's mousePressed property)

	If the current window requires more control of the event then it can implement its handleEvent method
	which is just empty by default. pollEvents calls this function every frame for the current state(window).
	'''
	def pollEvents(self):
		self.eventMgr.reset()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.eventMgr.setMousePressed(True)
			if event.type == pygame.KEYDOWN:
				self.pressed_key = pygame.key.name(event.key)
			self.states[self.gameMgr.getState()].handleEvent(event)

	'''
	the update function is called before draw on all screens!!!
	'''

	def update(self):
		self.states[self.gameMgr.getState()].update()

	def draw(self):
		self.display.fill(BLACK)
		self.states[self.gameMgr.getState()].draw(self.display)

	'''
	Add new states (screens) using this method to the main class.
	Screen has a static reference to this main class, so any screen can add a new state to the main class at any time
	'''
	def setState(self, name, state):
		self.states[name] = state

	'''
	Screen has a static reference to this main class, this sets that static reference to itself.
	And also initializes the screens that are needed. GAME_WINDOW will not be initialized here because
	only MAP_WINDOW and LEVEL_EDITOR can initialize it (after they have initialized the GAME_WINDOW) those 
	classes would call setState to set GAME_WINDOW to the window they initialized.
	'''
	def init(self):
		Screen.setMain(self)
		self.states = {START_WINDOW: StartWindow(), MAIN_WINDOW: MainWindow(), LEVEL_EDITOR: LevelEditor(), MAP_WINDOW: MapWindow(), CONTROLS_WINDOW: ControlsWindow()}
		self.gameMgr.setState(START_WINDOW)

	'''
	basic pygame main loop.
	pygame.display.flip() -- updates the display.
	'''
	def mainLoop(self):
		try:
			while self.run:
				self.pollEvents()
				self.update()
				self.draw()
				pygame.display.flip()
				self.clock.tick(10)
		except pygame.error:
			sys.exit()

if __name__ == '__main__':
	main = Main()
	main.mainLoop()

	
