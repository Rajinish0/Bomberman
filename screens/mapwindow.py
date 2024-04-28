import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os
import os
class MapWindow(Screen):
	def start_game(self, file_path):
		self.gameMgr.set_game_window_file_path(file_path)
		game_window = GameWindow(file_path)
		self.gameMgr.setState(GAME_WINDOW, game_window)

	def create_buttons(self):
		directory_name = 'sprites/levels/'
		buttons_per_row = 3

		button_data = []
		button_index = 0

		for filename in os.listdir(directory_name):
			if filename.endswith('.txt'):  # Filter out non-txt files
				map_path = os.path.join(directory_name, filename)  # Get the full path of the map file

				# Calculate the x position of the button
				x_position = (button_index % buttons_per_row) * 210 + 200

				# Calculate the y position of the button
				y_position = (button_index // buttons_per_row) * 200 + 220

				button_data.append({
					"x": x_position,
					"y": y_position,
					"map_file": map_path,  # Save the full path of the map file
					"img": f'sprites/Solid_white.png'
				})

				button_index += 1  # Increment button index

		self.buttons = []
		for data in button_data:
			button = Button(data["x"], data["y"], 150, 150,
							callBack=lambda map_file=data["map_file"]: (
								self.main.setState(GAME_WINDOW, GameWindow(map_file)),
								self.gameMgr.setState(GAME_WINDOW)),
							img=os.path.join(data["img"]))
			self.buttons.append(button)

	# def __init__(self):
	# 	# ... existing code ...
	# 	self.Game1 = Button(
	# 		200, 220, 150, 150,
	# 		callBack=lambda: self.start_game("sprites/defaultMap.txt"),
	# 		img=os.path.join(IMG_PATH, 'Solid_white.png')
	# 	)
	def __init__(self):
		self.btnBack = Button(
			30, 30, 30, 30, text="Back",
			callBack=lambda: self.gameMgr.setState(MAIN_WINDOW)
		)

		self.create_buttons()
		# directory_name = 'sprites/levels/'
		# buttons_per_row = 3
		#
		# button_data = []
		# button_index = 0
		#
		# for filename in os.listdir(directory_name):
		# 	if filename.endswith('.txt'):  # Filter out non-txt files
		# 		map_path = os.path.join(directory_name, filename)  # Get the full path of the map file
		#
		# 		# Calculate the x position of the button
		# 		x_position = (button_index % buttons_per_row) * 210 + 200
		#
		# 		# Calculate the y position of the button
		# 		y_position = (button_index // buttons_per_row) * 200 + 220
		#
		# 		button_data.append({
		# 			"x": x_position,
		# 			"y": y_position,
		# 			"map_file": map_path,  # Save the full path of the map file
		# 			"img": f'sprites/Solid_white.png'
		# 		})
		#
		# 		button_index += 1  # Increment button index
		#
		# # Print button data for verification
		# for index, data in enumerate(button_data, start=1):
		# 	print(f"Button {index}:")
		# 	print(f"   x: {data['x']}")
		# 	print(f"   y: {data['y']}")
		# 	print(f"   map_file: {data['map_file']}")
		# 	print(f"   img: {data['img']}")
		# 	print()




	def update(self):
		self.btnBack.update()
		self.create_buttons()
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


		self.btnBack.draw(display)
		for button in self.buttons:
			button.draw(display)





