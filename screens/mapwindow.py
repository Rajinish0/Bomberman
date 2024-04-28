import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os
import re

from utils import *

class MapWindow(Screen):

	def popup_start(self):
		self.dataSurface = pygame.Surface((self.gameWidth, (H - self.gameHeight + 70)))
		self.showData=True

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

	def handleEvent(self, event):
		if self.currPressedName:
			text=self.currPressedName.text
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key)=="backspace":
					text=text[:-1]
				elif pygame.key.name(event.key)=="enter":
					self.currPressedName=None
				elif re.search("^[a-z]{0,1}[A-Z]{0,1}[0-9]{0,1}-{0,1}_{0,1}$",pygame.key.name(event.key)):
					text+=pygame.key.name(event.key)
			if self.currPressedName:
				self.currPressedName.text=text
		elif self.currPressedTime:
			text = self.currPressedTime.text.split(":")
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key)=="backspace":
					if len(text[1])>0:
						text[1]=text[1][:-1]
					elif len(text[0])>0:
						text[0] = text[0][:-1]
				elif pygame.key.name(event.key)=="enter":
					self.currPressedTime=None
				elif re.search("^[0-9]{0,1}$",pygame.key.name(event.key)):
					if len(text[0])!=2:
						text[0] += pygame.key.name(event.key)
					elif len(text[1])!=2:
						text[1] += pygame.key.name(event.key)
				if self.currPressedTime:
					self.currPressedTime.text=text[0]+":"+text[1]
		elif self.currPressedRounds:
			text=self.currPressedRounds.text
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key)=="backspace":
					text=text[:-1]
				elif pygame.key.name(event.key)=="enter":
					self.currPressedRounds=None
				elif re.search("^[0-9]{0,1}$",pygame.key.name(event.key)):

					text+=pygame.key.name(event.key)
			if self.currPressedRounds:
				self.currPressedRounds.text=text









	def __init__(self):
		self.currPressedName=None
		self.currPressedTime=None
		self.currPressedRounds=None
		self.pl1Image = self.imgHandler.load(os.path.join(IMG_PATH, 'players', 'g1.png'), (50, 70))
		self.pl2Image = self.imgHandler.load(os.path.join(IMG_PATH, 'players', 'g2.png'), (50, 70))


		self.pl1Name = Button(
			270+10, 150 +80, 30, 30, text=PLAYER1_NAME,
			textColor=BLACK,center=False
		)
		self.pl2Name=Button(
			270+W/3-80, 150 + 80, 30, 30, text=PLAYER2_NAME,
			textColor=BLACK,center=False)

		self.time=Button(
			(270+W/6), 150 + 150, 30, 30, text="05:23",
			textColor=BLACK)

		self.rounds=Button(
			(270+W/6), 150 + 200, 30, 30, text="3",
			textColor=BLACK)

		self.dataSurface = pygame.Surface((W/3, (H/2)))
		self.showData=True
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
			W/2, H-100, 30, 30, text="Start",color=BLACK,textColor=BLACK,
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
		self.create_buttons()
		for ind,button in enumerate(self.buttons):
			button.update()
			if button.pressed:
				self.currMap=self.button_data[ind]
				self.currInd=button
		self.pl1Name.update()
		self.pl2Name.update()
		if self.pl1Name.pressed:
			self.currPressedName=self.pl1Name
		elif self.pl2Name.pressed:
			self.currPressedName = self.pl2Name

		self.time.update()

		if self.time.pressed:
			self.currPressedTime=self.time

		self.rounds.update()
		if self.rounds.pressed:
			self.currPressedRounds=self.rounds



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

		self.btnBack.draw(display)
		for button in self.buttons:
			button.draw(display)

		if self.currInd:
			self.currInd.draw(display,Border=True,BorderWidth=4)




		if self.showData:
			pygame.draw.rect(self.dataSurface, (238, 238, 238, 240), self.dataSurface.get_rect())
			display.blit(self.dataSurface, (270, 150))
			display.blit(self.pl1Image, (270+10, 150))
			display.blit(self.pl2Image, (270-10 + W / 3 - 50, 150))
			self.pl1Name.draw(display)
			self.pl2Name.draw(display)
			self.time.draw(display)
			self.rounds.draw(display)







