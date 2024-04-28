import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os

class MapWindow(Screen):
	def start_game(self, file_path):
		if self.currInd:
			self.currInd=None
			self.main.setState(GAME_WINDOW, GameWindow(file_path))
			self.gameMgr.setState(GAME_WINDOW)

	def go_back(self):
		self.currInd = None
		self.gameMgr.setState(MAIN_WINDOW)

	def create_buttons(self):
		directory_name = 'sprites/levels/'
		buttons_per_row = 3

		self.button_data = []
		button_index = 0

		for filename in os.listdir(directory_name):
			print(filename)
			if filename.endswith('.txt'):  # Filter out non-txt files
				map_path = os.path.join(directory_name, filename)  # Get the full path of the map file

				# Calculate the x position of the button
				x_position = (button_index % buttons_per_row) * 210 + 200

				# Calculate the y position of the button
				y_position = (button_index // buttons_per_row) * 200 + 220

				self.button_data.append({
					"x": x_position,
					"y": y_position,
					"map_file": map_path,  # Save the full path of the map file
					"img": f'sprites/Solid_white.png'
				})

				button_index += 1  # Increment button index


		self.buttons = []
		for data in self.button_data:
			button = Button(data["x"], data["y"], 150, 150,
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
			callBack=lambda: (self.go_back())
		)
		# self.button_data = [
		# 	{"x": 200, "y": 220, "map_file": 'sprites/levels/defaultMap.txt', "img": 'sprites/maps/map1.png'},
		# 	{"x": 410, "y": 220, "map_file": 'sprites/levels/SecondMap.txt', "img": 'sprites/maps/map2.png'},
		# 	{"x": 610, "y": 220, "map_file": 'sprites/levels/ThirdMap.txt', "img": 'sprites/maps/map3.png'}
		# ]

		self.create_buttons()

		self.currMap=self.button_data[0]
		self.currInd=None

		self.btnStart=Button(
			W/2, H-60, 30, 30, text="Start",color=BLACK,textColor=BLACK,
			callBack=lambda : (self.start_game(self.currMap["map_file"]))
		)


		self.forwardStart=Button(
			W-100, H-60, 30, 30, text="-->",color=BLACK,textColor=BLACK,
			callBack=lambda : (self.start_game(self.currMap["map_file"]))
		)


		self.backwardStart=Button(
			W-150, H-60, 30, 30, text="<--",color=BLACK,textColor=BLACK,
			callBack=lambda : (self.start_game(self.currMap["map_file"]))
		)

		#
		# self.buttons = []
		# for data in self.button_data:
		# 	button = Button(data["x"], data["y"], 150, 150,img=os.path.join(data["img"]))
		# 	self.buttons.append(button)




	def update(self):
		self.btnBack.update()
		self.btnStart.update()

		for ind,button in enumerate(self.buttons):
			button.update()
			if button.pressed:
				self.currMap=self.button_data[ind]
				self.currInd=button

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

		self.btnStart.draw(display)
		self.forwardStart.draw(display)
		self.backwardStart.draw(display)

		self.btnBack.draw(display)
		for button in self.buttons:
			button.draw(display)

		if self.currInd:
			self.currInd.draw(display,Border=True,BorderWidth=4)





