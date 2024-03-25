import pygame

'''
draws text on x, y coordinates (these are the center coordinates)
so if text is drawn at W/2, H/2 then it will centered at the middle of the screen

center : if true then x, y define the center coords of the text otherwise, 
		 they define the top left corner's coords
'''
def drawText(screen,text, x, y, size=30, 
			 color=(255, 0, 0), 
			 font_type = "Comic Sans MS",
			 center=True):
	text = str(text)
	font = pygame.font.SysFont(font_type, size)
	surface = font.render(text, True, color)
	text_width, text_height = font.size(text)
	if center:
		x = x-text_width/2
		y = y-text_height/2
	screen.blit(surface, (x, y))

'''
resets cursor back to arrow
'''
def resetCursor():
	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
