from handlers import GameStateMgr
'''
generic screen class

it has a static reference to the main class so that screens can set new screen in the main class
and also has a static reference to the gamestatemgr so that they can change the current state(screen) of the game
'''
class Screen:
	main = None
	gameMgr = GameStateMgr()

	'''main calls this function to connect the two classes'''
	@staticmethod
	def setMain(main):
		Screen.main = main
	
	def __init__(self):
		pass

	def handleEvent(self, event):
		pass

	def update(self):
		pass

	def draw(self, display):
		pass