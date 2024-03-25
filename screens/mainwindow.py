from .screen import Screen
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
		self.MapMenu = Button(W/2, H/2 - 150, 50, 50, text="Maps", textColor=WHITE)
		self.CntrlMenu = Button(W/2, H/2 - 50, 50, 50, text="Controls", textColor=WHITE)
		self.LvlEditor = Button(W/2, H/2 + 50, 50, 50, text="Editor", textColor=WHITE,
						  	 	callBack= lambda: self.gameMgr.setState(LEVEL_EDITOR) )
		self.ExitButton = Button(W/2, H/2 + 150, 50, 50, text="Exit", textColor=WHITE,
						   		 callBack=lambda: pygame.quit())
	
	def update(self):
		self.MapMenu.update()
		self.CntrlMenu.update()
		self.LvlEditor.update()
		self.ExitButton.update()
	
	def draw(self, display):
		display.fill((0, 0, 255))
		self.MapMenu.draw(display)
		self.CntrlMenu.draw(display)
		self.LvlEditor.draw(display)
		self.ExitButton.draw(display)
