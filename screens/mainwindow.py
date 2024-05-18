from screens.screen import Screen
from button import Button 
from constants import *
import pygame
import os
'''
MainWindow has 4 buttons for each of the corresponding screens and an exit button
the callBack functions of the buttons just switches to that state while the Exit button calls pygame.quit() to exit the game

TO DO:
implement Map and Control menu screens
'''
class MainWindow(Screen):
	def __init__(self):
		font_path = os.path.join('UI/Press_Start_2P', 'PressStart2P-Regular.ttf')
		font_size = 10
		self.font = pygame.font.Font(font_path, font_size)

		self.MapMenu = Button(W/2, H/2 - 120, 300, 100, text="Maps", textColor=BLACK,
								callBack = lambda: self.gameMgr.setState(MAP_WINDOW),  img='UI/button.png', textSize=15)
		self.CntrlMenu = Button(W/2, H/2 , 300, 100, text="Controls", textColor=BLACK,
								callBack = lambda: self.gameMgr.setState(CONTROLS_WINDOW),  img='UI/button.png', textSize=15)
		self.LvlEditor = Button(W/2, H/2 + 120, 300, 100, text="Editor", textColor=BLACK,
						  	 	callBack= lambda: self.gameMgr.setState(LEVEL_EDITOR), img='UI/button.png', textSize=15)

		self.ExitButton = Button(930,70, 30, 30, textColor=BLACK,
						   		 callBack=lambda: pygame.quit(),  img='UI/exit.png', textSize=25)

		self.frame_image = pygame.image.load('UI/frame.png')
		self.frame_image = pygame.transform.scale(self.frame_image, (60, 80))

		self.wizard_image = pygame.image.load('UI/wizard2.png')
		self.wizard_image = pygame.transform.scale(self.wizard_image, (180, 180))
		self.wizard_position = (70,70)

	def update(self):
		self.MapMenu.update()
		self.CntrlMenu.update()
		self.LvlEditor.update()
		self.ExitButton.update()
	
	def draw(self, display):
		display.fill((114, 125, 104))
		display.blit(self.wizard_image, self.wizard_position)

		x_increment = 50
		frame_rotated_image = pygame.transform.rotate(self.frame_image, +90)
		for i in range(20):
			display.blit(frame_rotated_image, (35 + i * x_increment, -15))

		for i in range(20):
			display.blit(frame_rotated_image, (35 + i * x_increment, 550))

		y_increment = 50
		frame_rotated_image = pygame.transform.rotate(self.frame_image, -180)
		for i in range(12):
			display.blit(frame_rotated_image, (-15, -15 + i * y_increment))

		for i in range(12):
			display.blit(self.frame_image, (950, -15 + i * y_increment))

		self.MapMenu.draw(display)
		self.CntrlMenu.draw(display)
		self.LvlEditor.draw(display)
		self.ExitButton.draw(display)



