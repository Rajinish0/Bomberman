import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os
import re

from utils import *

class MapWindow(Screen):

	def __init__(self):
		self.currWindow = 0
		self.create_buttons()
		self.currPressedName = None
		self.currPressedTime = None
		self.currPressedRounds = None
		self.pl1Image = self.imgHandler.load(os.path.join(IMG_PATH, 'players', 'g1.png'), (50, 70))
		self.pl2Image = self.imgHandler.load(os.path.join(IMG_PATH, 'players', 'g2.png'), (50, 70))
		self.totalWindow=0
		self.currMap=self.button_data[0]
		self.currInd=None

		self.create_buttons()
		self.pl1Name = Button(
			270 + 10, 150 + 80, 30, 30, text=PLAYER1_NAME,
			textColor=BLACK, center=False
		)
		self.pl2Name = Button(
			270 + W / 3 - 80, 150 + 80, 30, 30, text=PLAYER2_NAME,
			textColor=BLACK, center=False)

		self.time = Button(
			(270 + W / 6), 150 + 150, 30, 30, text="05:23",
			textColor=BLACK)

		self.rounds = Button(
			(270 + W / 6), 150 + 200, 30, 30, text="3",
			textColor=BLACK)

		self.dataSurface = pygame.Surface((W / 3, (H / 2)))
		self.showData = True

		self.btnBack = Button(
			30, 30, 30, 30, text="Back",
			callBack=lambda: (self.go_back())
		)

		self.btnStart=Button(
			W/2, H-60, 30, 30, text="Start",color=BLACK,textColor=BLACK,
			callBack=lambda : (self.start_game(self.currMap["map_file"]))
		)

		self.forwardStart=Button(
			W-100, H-60, 30, 30, text="-->",color=BLACK,textColor=BLACK,
			callBack=lambda : self.increasePage()
		)

		self.backwardStart=Button(
			W-150, H-60, 30, 30, text="<--",color=BLACK,textColor=BLACK,
			callBack=lambda : self.decreasePage()
		)

		self.deleteBtn=Button(
			100, H-60, 30, 30, text="Delete",color=BLACK,textColor=BLACK,
			callBack=lambda : self.deleteMap()
		)

	def increasePage(self):
		if self.totalWindow >= self.currWindow + 1:
			self.currWindow += 1
			self.currInd =None


	def decreasePage(self):
		if 0 <= self.currWindow - 1:
			self.currWindow -= 1
			self.currInd = None

	def deleteMap(self):
		file_name = self.currInd.text
		if os.path.exists(file_name):
			os.remove(file_name)

		self.create_buttons()
		self.currInd = None
		self.totalWindow = len(self.mapPerPage) - 1
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
		directory_name_img = 'sprites/map_pictures/'
		buttons_per_row = 3

		self.button_data = []
		self.mapPerPage = {}
		button_index = 0
		total_window = 0

		for filename in os.listdir(directory_name):
			map_path = os.path.join(directory_name, filename)
			map_name = os.path.splitext(filename)[0]

			img_path = os.path.join(directory_name_img, f"{map_name}.jpg")

			if button_index > 5:
				button_index = 0
				total_window += 1
				self.totalWindow = total_window

			x_position = (button_index % buttons_per_row) * 210 + 200
			y_position = (button_index // buttons_per_row) * 200 + 220

			self.button_data.append({
				"page": total_window,
				"x": x_position,
				"y": y_position,
				"map_file": map_path,  # Save the full path of the map file
				"position": button_index,
				"img": img_path
			})

			button_index += 1  # Increment button index

			self.mapPerPage.update({
				total_window: button_index
			})

		self.buttons = []
		# if not self.currWindow:
		# 	self.currWindow=0
		for data in self.button_data:
			if self.currWindow == data["page"]:
				button = Button(data["x"], data["y"], 150, 150,
								img=os.path.join(data["img"]), text=data["map_file"], textSize=1, color=(0, 0, 0, 0))
				self.buttons.append(button)


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

	def update(self):
		self.btnBack.update()
		self.create_buttons()
		self.btnStart.update()
		self.deleteBtn.update()

		self.backwardStart.update()
		self.forwardStart.update()
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
		self.forwardStart.draw(display)
		self.backwardStart.draw(display)
		self.deleteBtn.draw(display)

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







