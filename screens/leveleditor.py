from .screen import Screen
from constants import *
from button import Button
from gameObjects import *
from utils import *
import pygame
from copy import deepcopy

'''
TEMPORARY CLASS FOR EXPERIMENTATION PURPOSES.
'''

imgs = {
  BOX  : Box.image,
  WALL : Wall.image
} 

def inBound(x, y, lx, ly, w, h):
	return ( lx <= x <= lx + w and 
		 ly <= y <= ly + h )

def ScreenCrdToIdx(x, y, width, height):
	return (y // height, x//width) 

class LevelEditor(Screen):
	def __init__(self):
		self.offSetX = 200
		self.offSetY = 0
		self.boxWidth = (W - self.offSetX)//NUM_BOXES
		self.boxHeight = (H - self.offSetY)//NUM_BOXES
		self.grid = [[EMPTY for i in range(NUM_BOXES)]
			         for j in range(NUM_BOXES)]
		self.backButton = Button(
			0, 0, 30, 30, text = "Back",
			callBack=lambda:self.gameMgr.setState(
				self.gameMgr.getPrevState(),
            		),	
			center=False
        	)
		self.boxButton = Button(
			0, 50, self.boxWidth, self.boxHeight, img=Box.image,
			callBack=lambda:self.setSelected(BOX),
			center=False
		)

		self.wallButton = Button(
			100, 50, self.boxWidth, self.boxHeight, img=Wall.image,
			callBack=lambda:self.setSelected(WALL),
			center=False
		)
		self.selected = None	
	
	def setSelected(self, elem):
		self.selected = elem
	
	def handlePlacement(self):
		(mx, my) = pygame.mouse.get_pos()
		if self.selected and inBound(mx, my, self.offSetX, self.offSetY, 
					     W-self.offSetX, H-self.offSetY):
			(i, j) = ScreenCrdToIdx(mx-self.offSetX, my-self.offSetY, self.boxWidth, self.boxHeight)
			self.grid[i][j] = self.selected
			return True
		else:
			return False
	
	def handleMouse(self):
		if self.evMgr.mousePressed:
			if not self.handlePlacement():
				self.setSelected(None)			

	def update(self):
		self.handleMouse()
		self.backButton.update()
		self.boxButton.update()
		self.wallButton.update()
	
	def load(self, img):
		return self.imgHandler.load(img, (self.boxWidth, self.boxHeight) )

	def draw(self, display):
		display.fill((125, 0, 125))
		self.backButton.draw(display)
		self.boxButton.draw(display)
		self.wallButton.draw(display)
		for i in range(NUM_BOXES):
			for j in range(NUM_BOXES):
				x = self.offSetX + j*self.boxWidth;
				y = self.offSetY + i*self.boxHeight;
				pygame.draw.rect(display, RED, (x, y, self.boxWidth, self.boxHeight), 1)
				if self.grid[i][j] != EMPTY:
					display.blit( self.load(imgs[self.grid[i][j]]), (x, y) )
					


		if self.selected is not None:
			(mx, my) = pygame.mouse.get_pos()
			img = self.load(imgs[self.selected])
			img.set_alpha(150)
			display.blit(img, (mx-self.boxWidth/2, my-self.boxHeight/2))
			img.set_alpha(255)
