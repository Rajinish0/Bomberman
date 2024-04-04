from screens.screen import Screen
from button import Button 
from constants import *
import pygame

'''
MainWindow has 4 buttons for each of the corresponding screens and an exit button
the callBack functions of the buttons just switches to that state while the Exit button calls pygame.quit() to exit the game

TO DO:
implement Map and Control menu screens
'''
class MainWindow(Screen):
	def __init__(self):
		self.MapMenu = Button(W/2, H/2 - 150, 50, 50, text="Maps", textColor=WHITE,
								callBack = lambda: self.gameMgr.setState(MAP_WINDOW))
		self.CntrlMenu = Button(W/2, H/2 - 50, 50, 50, text="Controls", textColor=WHITE,
								callBack = lambda: self.gameMgr.setState(CONTROLS_WINDOW))
		self.LvlEditor = Button(W/2, H/2 + 50, 50, 50, text="Editor", textColor=WHITE,
						  	 	callBack= lambda: self.gameMgr.setState(LEVEL_EDITOR))
		self.ExitButton = Button(W/2, H/2 + 150, 50, 50, text="Exit", textColor=WHITE,
						   		 callBack=lambda: pygame.quit())
		self.GameWindowButton = Button(W/2, H/2 + 250, 50, 50, text="Play Game", textColor=WHITE,
						   		 callBack=lambda: self.gameMgr.setState(GAME_WINDOW))
	
	def update(self):
		self.MapMenu.update()
		self.CntrlMenu.update()
		self.LvlEditor.update()
		self.ExitButton.update()
		self.GameWindowButton.update()
	
	def draw(self, display):
		display.fill((255, 255, 255))

		background_image = pygame.image.load('sprites/background.png')
		scaled_image = pygame.transform.scale(background_image, (W, H))

		alpha_value_bg = 200
		scaled_image.set_alpha(alpha_value_bg)

		display.blit(scaled_image, (0, 0))

		self.MapMenu.draw(display)
		self.CntrlMenu.draw(display)
		self.LvlEditor.draw(display)
		self.ExitButton.draw(display)
		self.GameWindowButton.draw(display)

