from .screen import Screen
from constants import *
from button import Button
import pygame

'''
TEMPORARY CLASS FOR EXPERIMENTATION PURPOSES.
'''

class LevelEditor(Screen):
	def __init__(self):
		self.offSetX = 200
		self.offSetY = 0
		self.boxWidth = (W - self.offSetX)//NUM_BOXES
		self.boxHeight = (H - self.offSetY)//NUM_BOXES
		self.grid = [[EMPTY for i in range(NUM_BOXES)]
			         for j in range(NUM_BOXES)]
		self.backButton = Button(
			30, 30, 30, 30, text = "Back",
			callBack=lambda:self.gameMgr.setState(
				self.gameMgr.getPrevState()
            )
        )

	def update(self):
		self.backButton.update()

	def draw(self, display):
		display.fill((125, 0, 125))
		self.backButton.draw(display)
		for i in range(NUM_BOXES):
			for j in range(NUM_BOXES):
				pygame.draw.rect(display, RED, ( self.offSetX + j*self.boxWidth, self.offSetY + i*self.boxHeight, self.boxWidth, self.boxHeight), 1)