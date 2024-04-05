from constants.colors import *
from handlers import *
from utils import *
import pygame

'''
default function for when the mouse is on top of a button,
it sets the cursor to a hand
'''
def _defHover():
	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

'''
BUTTONS MUST BE UPDATED BEFORE THEY ARE DRAWN.

the update method checks for mouse presses
'''

class Button:
	evMgr = EventMgr()
	imgHandler = ImageHandler()
	'''
	args :
	x - x coord
	y - y coord
	width - width
	height - height
	text - text to be drawn on top of the button
	textColor - color for the text
	img - image to be drawn on top the button
	color - the color for the bounding box
	callBack - a method that is called when the button is pressed
	onHover - called when the mouse is on top of the button
	center - if true then the x,y arguments define the center of the button otherwise they define the top left coordinates
			 it is true by default.
	drawRect - draw a bounding box around the button

	button sets its pressed property to true if it was clicked/pressed,
	and it sets its hovered property to true if the mouse is on top of it.

	img and drawRect are mutually exclusive for now; i.e you can either draw an image or a bounding box,
	but it can be edited if necessary.
	'''
	def __init__(self, x, y, width, height, *, text = None,
			     textColor = WHITE, img = None, color = RED,
				 callBack=None, onHover=_defHover, center=True,
				 drawRect = False, textSize = None):
		self.x = x
		self.y = y
		self.w = width
		self.h = height
		self.img = self.imgHandler.load(img, (width, height)) if img is not None else img
		self.color = color
		self.text = text
		self.textColor = textColor
		self.cb = callBack
		self.onHover = onHover
		self.drawRect = drawRect
		self.center = center
		self.pressed = False
		self.hovered = False
		self.textSize = textSize
		if center: self.centerCords()
	def centerCords(self):
		self.x -= self.w/2
		self.y -= self.h/2	

	def update(self):
		self.pressed = False
		if self.mouseInside():
			if (not self.hovered):
				self.onHover()
				self.hovered = True

			if self.evMgr.mousePressed:
				if self.cb is not None: self.cb()
				self.pressed = True
		elif self.hovered:
			resetCursor()
			self.hovered = False
			
			

	def mouseInside(self):
		(mx, my) = pygame.mouse.get_pos()
		return (mx >= self.x and mx <= self.x + self.w and
			my >= self.y and my <= self.y + self.h)

	def draw(self, display):
		if self.img is not None:
			display.blit(self.img, (self.x, self.y))
		elif self.drawRect:
			pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))
		if self.text is not None:
			x, y = self.x, self.y
			if self.center:
				x = self.x + self.w/2
				y = self.y + self.h/2
			sz = self.textSize or self.w//2
			drawText(display, self.text, x, y, size = sz,color=self.textColor, center=self.center)

