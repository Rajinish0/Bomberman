import pygame

from button import Button
from constants import *
from .GameWindow import GameWindow
from .screen import Screen
import os

class MapWindow(Screen):

	def __init__(self):
		self.currWindow=0
		self.totalWindow=0
		self.create_buttons()
		self.currMap=self.button_data[0]
		self.currInd=None

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

	def decreasePage(self):
		if 0 <= self.currWindow - 1:
			self.currWindow -= 1

	def deleteMap(self):
		file_name = self.currInd.text
		if os.path.exists(file_name):
			os.remove(file_name)

		self.create_buttons()
		self.currInd = None
		self.totalWindow = len(self.mapPerPage) - 1

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
		self.mapPerPage = {}
		button_index = 0
		total_window = 0

		for filename in os.listdir(directory_name):
			if filename.endswith('.txt'):
				map_path = os.path.join(directory_name, filename)  # Get the full path of the map file

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
					"img": f'sprites/Solid_white.png'
				})

				button_index += 1  # Increment button index

				self.mapPerPage.update({
					total_window: button_index
				})


		self.buttons = []


		for data in self.button_data:
			if self.currWindow == data["page"]:
				button = Button(data["x"], data["y"], 150, 150,
								img=os.path.join(data["img"]), text=data["map_file"], textSize=10, textColor=BLACK, )
				self.buttons.append(button)

	def update(self):
		self.btnBack.update()
		self.create_buttons()
		self.btnStart.update()
		self.deleteBtn.update()

		self.backwardStart.update()
		self.forwardStart.update()

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
		self.deleteBtn.draw(display)

		self.btnBack.draw(display)
		for button in self.buttons:
			button.draw(display)

		if self.currInd:
			self.currInd.draw(display,Border=True,BorderWidth=4)





