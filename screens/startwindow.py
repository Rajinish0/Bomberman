import pygame

from button import Button
from constants import *
from .screen import Screen
import os

'''StartWindow currently has one button
which has a callBack function that sets the gameMgr's current state to the MAIN_WINDOW (main menu)
so when the start button is pressed it will change the state (i.e screen) to main window

all buttons must be updated before they are drawn
'''
class StartWindow(Screen):
	def __init__(self):
		self.btn = Button(600, 500, 200, 60,
						  callBack = lambda: self.gameMgr.setState( MAIN_WINDOW ),
						 text="Start", img='UI/button.png', textSize=15, textColor=BLACK)

		self.wizard_image = pygame.image.load('UI/wizard.png')
		self.wizard_image = pygame.transform.scale(self.wizard_image, (200, 200))
		self.wizard_position = (70,70)

		self.frame_image = pygame.image.load('UI/frame.png')
		self.frame_image = pygame.transform.scale(self.frame_image, (60, 60))

		self.des_image = pygame.image.load('UI/description.png')
		self.des_image = pygame.transform.scale(self.des_image, (620, 320))

		font_path = os.path.join('UI/Press_Start_2P', 'PressStart2P-Regular.ttf')
		font_size = 10
		self.font = pygame.font.Font(font_path, font_size)
		self.text = "In the heart of an enchanted forest, a powerful "
		self.text2 = "wizard named Zephyr guarded his realm fiercely."
		self.text3 = "One day, two adventurers, Mira and Thane,"

		self.text4 = "unknowingly crossed into his territory. Zephyr"
		self.text5 = "appeared in a flash of light, his eyes cold."
		self.text6 = "\"You have trespassed on sacred ground. Fight "
		self.text7 = ",and the victor may leave.\""
		self.text8 = "Bound by the wizard's spell, Mira and Thane"
		self.text9 = "had no choice."
		self.text_color = BLACK


	def update(self):
		self.btn.update()

	def draw(self, display):
		display.fill((114, 125, 104))
		self.btn.draw(display)

		display.blit(self.wizard_image, self.wizard_position)
		display.blit(self.des_image, (280, 120))

		x_increment = 50
		frame_rotated_image = pygame.transform.rotate(self.frame_image, -90)
		for i in range(20):
			display.blit(frame_rotated_image, (40 + i * x_increment, -10))

		for i in range(20):
			display.blit(frame_rotated_image, (40 + i * x_increment, 550))

		y_increment = 50
		frame_rotated_image = pygame.transform.rotate(self.frame_image, -180)
		for i in range(12):
			display.blit(frame_rotated_image, (-10, -5 + i * y_increment))

		for i in range(12):
			display.blit(self.frame_image, (950, -5 + i * y_increment))

		text_surface = self.font.render(self.text, True, self.text_color)
		display.blit(text_surface, (380,190))
		text_surface = self.font.render(self.text2, True, self.text_color)
		display.blit(text_surface, (380, 210))
		text_surface = self.font.render(self.text3, True, self.text_color)
		display.blit(text_surface, (380, 250))

		text_surface = self.font.render(self.text4, True, self.text_color)
		display.blit(text_surface, (380, 270))
		text_surface = self.font.render(self.text5, True, self.text_color)
		display.blit(text_surface, (380, 290))
		text_surface = self.font.render(self.text6, True, self.text_color)
		display.blit(text_surface, (380, 310))

		text_surface = self.font.render(self.text7, True, self.text_color)
		display.blit(text_surface, (380, 330))

		text_surface = self.font.render(self.text8, True, self.text_color)
		display.blit(text_surface, (380, 370))

		text_surface = self.font.render(self.text9, True, self.text_color)
		display.blit(text_surface, (380, 390))

