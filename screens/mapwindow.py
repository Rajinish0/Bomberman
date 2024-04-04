import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os

class MapWindow(Screen):
	def __init__(self):
		self.btnBack = Button(
			30, 30, 30, 30, text="Back",
			callBack=lambda: self.gameMgr.setState(MAIN_WINDOW)
		)

		self.Game1 = Button(200, 220, 150, 150,
								callBack = lambda: (self.gameMgr.set_game_window_file_path("sprites/defaultMap.txt"),
													self.gameMgr.setState(GAME_WINDOW)),
							  	img=os.path.join(IMG_PATH, 'Solid_white.png') )


		self.Game2 = Button(410, 220, 150, 150,
								callBack = lambda: (self.gameMgr.set_game_window_file_path("sprites/SecondMap.txt"),
													self.gameMgr.setState(GAME_WINDOW)),
							  	img=os.path.join(IMG_PATH, 'Solid_white.png') )


		self.Game3 = Button(610, 220, 150, 150,
							callBack=lambda: (self.gameMgr.set_game_window_file_path("sprites/ThirdMap.txt"),
											  self.gameMgr.setState(GAME_WINDOW)),
							img=os.path.join(IMG_PATH, 'Solid_white.png'))



	def update(self):
		self.btnBack.update()
		self.Game1.update()
		self.Game2.update()
		self.Game3.update()

	def draw(self, display):
		display.fill((255, 255, 255))
		background_image = pygame.image.load('sprites/background.png')
		scaled_image = pygame.transform.scale(background_image, (W, H))

		alpha_value_bg = 200
		scaled_image.set_alpha(alpha_value_bg)

		display.blit(scaled_image, (0, 0))

		rect1_surface = pygame.Surface((700, 500), pygame.SRCALPHA)
		pygame.draw.rect(rect1_surface, (238, 238, 238, 240), rect1_surface.get_rect(), border_radius=8)
		display.blit(rect1_surface, (50, 62))
		self.Game1.draw(display)
		self.Game2.draw(display)
		self.Game3.draw(display)

		self.btnBack.draw(display)