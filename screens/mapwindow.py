import math
import pickle

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
		self.caps=False
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

		with open(os.path.join(RSRC_PATH, 'datacfg.pkl'), 'rb') as f:
			self.data = pickle.load(f)



		self.create_buttons()
		self.pl1Name = Button(
			270 + 70, 150 + 90, 100, 25, text=self.data["p1"],color=WHITE,center=True,textSize=15,
			textColor=BLACK,drawRect=True
		)
		self.pl2Name = Button(
			270 + W / 3 - 70, 150 + 90, 100, 25, text=self.data["p2"],color=WHITE,center=True,textSize=15,
			textColor=BLACK,drawRect=True)

		self.time = Button(
			(270 + W / 6), 150 + 170, 50, 25, text=self.getTimer(self.data["timer"]),color=WHITE,textSize=15,
			textColor=BLACK,drawRect=True)

		self.rounds = Button(
			(270 + W / 6), 150 + 245, 30, 25, text=str(self.data["rounds"]),color=WHITE,
			textColor=BLACK,drawRect=True)

		self.start = Button(
			270 + W / 3 - 70,150+H/2+30,50,25,text="Start",textColor=BLACK, center=True,
			callBack=lambda: (self.start_game(self.currMap["map_file"]))
		)

		self.back=Button(
			270+70,150+H/2+30,50,25,text="Back", textColor=BLACK, center=True,
			callBack=lambda : self.remove_popup()
		)


		self.showData = False

		self.btnBack = Button(
			30, 30, 30, 30, text="Back",
			callBack=lambda: (self.go_back())
		)

		self.btnStart=Button(
			W/2, H-60, 30, 30, text="Start",color=BLACK,textColor=BLACK,
			callBack=lambda : (self.popup_start())
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
		parts = file_name.split('/')
		picture_name = parts[2].split('.')
		flag = False

		if os.path.exists(file_name):
			# Check if picture_name is one of the restricted names
			if picture_name[0] not in ["defaultMap", "secondMap", "thirdMap"]:
				flag = True
				os.remove(file_name)

		picture_file_name = "sprites/map_pictures/" + picture_name[0] + ".jpg"
		if flag:
			if os.path.exists(picture_file_name):
				os.remove(picture_file_name)

			self.create_buttons()
			self.currInd = None
			self.totalWindow = len(self.mapPerPage) - 1

	def popup_start(self):
		if self.currInd:
			self.dataSurface = pygame.Surface((W / 3, (H / 2)+50))
			self.showData=True
			with open(os.path.join(RSRC_PATH, 'datacfg.pkl'), 'rb') as f:
				self.data = pickle.load(f)

	def remove_popup(self):
		self.showData = False
		self.currPressedName=None
		self.currPressedTime=None
		self.currPressedRounds=None
		self.data["p1"] = self.pl1Name.text
		self.data["p2"] = self.pl2Name.text
		time = self.time.text.split(":")
		self.data["timer"] = int(time[0]) * 60 + int(time[1])
		self.data["round"] = int(self.rounds.text)
		with open(os.path.join(RSRC_PATH, 'datacfg.pkl'), 'wb') as f:
			data = pickle.dump(self.data, f)


	def start_game(self, file_path):
		self.showData=False
		self.currPressedName = None
		self.currPressedTime = None
		self.currPressedRounds = None
		self.data["p1"] = self.pl1Name.text or "Aunt May"
		self.data["p2"] = self.pl2Name.text or "Uncle Ben"
		time=self.time.text.split(":")
		if time[1]:
			self.data["timer"]=int(time[0])*60+int(time[1])
		else:
			self.data["timer"] = 45

		self.data["round"]=int(self.rounds.text or 2)

		with open(os.path.join(RSRC_PATH, 'datacfg.pkl'), 'wb') as f:
			data = pickle.dump(self.data, f)
		if self.currInd:
			self.main.setState(GAME_WINDOW, GameWindow(file_path))
			self.gameMgr.setState(GAME_WINDOW)

	def go_back(self):
		self.currPressedName = None
		self.currPressedTime = None
		self.currPressedRounds = None
		self.gameMgr.setState(MAIN_WINDOW)

	def getTimer(self,timer):
		if timer <= 0:
			return ("00:00")
		else:
			min = str(math.floor(math.ceil(timer) / 60)).zfill(2)
			sec = str(math.ceil(timer) % 60).zfill(2)
			text = min + ":" + sec
			return text

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
			text = self.currPressedName.text
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "left shift":
					self.caps = True
				if pygame.key.name(event.key) == "backspace":
					text = text[:-1]
				elif pygame.key.name(event.key) == "enter":
					self.currPressedName = None
				elif pygame.key.name(event.key) == "space" and len(text)<12:
					text += " "
				elif re.search("^[a-z]{0,1}[A-Z]{0,1}[0-9]{0,1}-{0,1}_{0,1}$", pygame.key.name(event.key)) and len(text)<12:
					if self.caps:
						text += pygame.key.name(event.key).upper()
					else:
						text += pygame.key.name(event.key)

			if self.currPressedName:
				self.currPressedName.text = text
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
					if len(text)<1:
						text+=pygame.key.name(event.key)
					else:
						text = pygame.key.name(event.key)

			if self.currPressedRounds:
				self.currPressedRounds.text=text
		if event.type == pygame.KEYUP:
			if pygame.key.name(event.key) == "left shift":
				self.caps = False

	def update(self):
		if self.showData:
			self.start.update()
			self.back.update()

			self.pl1Name.update()
			self.pl2Name.update()
			if self.pl1Name.pressed:
				self.currPressedRounds=False
				self.currPressedTime=False
				self.currPressedName=self.pl1Name
			elif self.pl2Name.pressed:
				self.currPressedName = self.pl2Name

			self.time.update()

			if self.time.pressed:
				self.currPressedRounds = False
				self.currPressedName = False
				self.currPressedTime=self.time

			self.rounds.update()
			if self.rounds.pressed:
				self.currPressedName = False
				self.currPressedTime = False
				self.currPressedRounds=self.rounds
		else:
			self.btnBack.update()
			self.create_buttons()
			self.btnStart.update()
			self.deleteBtn.update()

			self.backwardStart.update()
			self.forwardStart.update()
			self.create_buttons()

			for ind, button in enumerate(self.buttons):
				button.update()
				if button.pressed:
					self.currMap = self.button_data[ind]
					self.currInd = button


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
			drawText(display,button.text[15:-4],button.x+button.w/2,button.y+button.h+25,size=20,color=BLACK)

		if self.currInd:
			self.currInd.draw(display,Border=True,BorderWidth=4)




		if self.showData:
			pygame.draw.rect(self.dataSurface, (238, 238, 238, 240), self.dataSurface.get_rect())
			display.blit(self.dataSurface, (270, 150))
			display.blit(self.pl1Image, (270+70-25, 150))
			display.blit(self.pl2Image, (270 + W / 3 - 70-25, 150))
			drawText(display,"Battle Royale Time", 270+W/6,150+135,size=18,color=BLACK)
			drawText(display, "Win Rounds", 270 + W / 6, 150 + 210, size=18, color=BLACK)
			self.pl1Name.draw(display,Border=True)
			self.pl2Name.draw(display,Border=True)
			self.time.draw(display,Border=True)
			self.rounds.draw(display,Border=True)
			self.back.draw(display)
			self.start.draw(display)








