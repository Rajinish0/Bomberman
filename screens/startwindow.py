from button import Button
from constants import *
from .screen import Screen
import os

'''StartWindow currently has one button
which has a callBack function that sets the gameMgr's current state to the MAIN_WINDOW (main menu)
so when the start button is pressed it will change the state (i.e screen) to main window

all buttons must be updated before they are drawn
'''
class StartWindow(Screen):
	def __init__(self):
		self.btn = Button(W/2, H/2, 100, 100, 
						  callBack = lambda: self.gameMgr.setState( MAIN_WINDOW ),
						  img = os.path.join (IMG_PATH, 'start.png')  )

	def update(self):
		self.btn.update()

	def draw(self, display):
		display.fill((255, 255, 255))
		self.btn.draw(display)