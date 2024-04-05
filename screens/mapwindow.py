import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os

class MapWindow(Screen):
	def start_game(self, file_path):
		self.gameMgr.set_game_window_file_path(file_path)
		game_window = GameWindow(file_path)
		self.gameMgr.setState(GAME_WINDOW, game_window)

	def __init__(self):
		# ... existing code ...
		self.Game1 = Button(
			200, 220, 150, 150,
			callBack=lambda: self.start_game("sprites/defaultMap.txt"),
			img=os.path.join(IMG_PATH, 'Solid_white.png')
		)
	def __init__(self):
		self.btnBack = Button(
			30, 30, 30, 30, text="Back",
			callBack=lambda: self.gameMgr.setState(MAIN_WINDOW)
		)
		self.buttons = []

	def update(self):
		self.btnBack.update()

		for button in self.buttons:
			button.update()


	def draw(self, display):
		display.fill((110, 161, 100))

		# BACKGROUND IMAGE
		# background_image = pygame.image.load('sprites/backgrnd.png')
		# scaled_image = pygame.transform.scale(background_image, (W, H))
		# alpha_value_bg = 260
		# scaled_image.set_alpha(alpha_value_bg)
		# display.blit(scaled_image, (0, 0))


		rect1_surface = pygame.Surface((700, 500), pygame.SRCALPHA)
		pygame.draw.rect(rect1_surface, (238, 238, 238, 220), rect1_surface.get_rect(), border_radius=8)
		display.blit(rect1_surface, (50, 62))

		button_data = [
			{"x": 200, "y": 220, "map_file": 'sprites/levels/defaultMap.txt', "img": 'sprites/maps/map1.png'},
			{"x": 410, "y": 220, "map_file": 'sprites/levels/SecondMap.txt',  "img": 'sprites/maps/map2.png'},
			{"x": 610, "y": 220, "map_file": 'sprites/levels/ThirdMap.txt',   "img": 'sprites/maps/map3.png'}
		]

		self.btnBack.draw(display)

		for data in button_data:
			button = Button(data["x"], data["y"], 150, 150,
							callBack=lambda map_file=data["map_file"]: (
							self.main.setState(GAME_WINDOW, GameWindow(map_file)),
							self.gameMgr.setState(GAME_WINDOW)),
							img=os.path.join(data["img"]))
			button.draw(display)
			self.buttons.append(button)


