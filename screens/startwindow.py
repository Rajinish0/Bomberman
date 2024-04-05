import pygame

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
		self.btn = Button(W/2, 520, 100, 100,
						  callBack = lambda: self.gameMgr.setState( MAIN_WINDOW ),
						 text="Start")

	def update(self):
		self.btn.update()

	def draw(self, display):
		display.fill((110, 161, 100))
		self.btn.draw(display)

		# background_image = pygame.image.load('sprites/backgrnd.png')
		# scaled_image = pygame.transform.scale(background_image, (W, H))
		# alpha_value_bg = 260
		# scaled_image.set_alpha(alpha_value_bg)
		# display.blit(scaled_image, (0, 0))

		rect1_surface = pygame.Surface((700, 400), pygame.SRCALPHA)
		pygame.draw.rect(rect1_surface, (238, 238, 238, 220), rect1_surface.get_rect(), border_radius=8)
		display.blit(rect1_surface, (50, 62))