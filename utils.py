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


## x1, y1 and x2, y2 are the top left coords
def rectsCollide(r1 : tuple , r2 : tuple) -> bool:
	(x1, y1, w1, h1) = r1
	(x2, y2, w2, h2) = r2

	return (
		(x1 <= x2 <= x1 + w1 and y2 <= y1 + h1 and y1 <= y2 +h2) or 
		(x1 <= x2 + w1 <= x1 + w1 and y2 <= h1 + h1 and y1 <= h2 + h2) or 
		(y1 <= y2 + h2 <= y1 + h1 and x2 <= x1 + w1 and x1<=x2 + w2) or
		(y1 <= y2 <= y1 + h1 and x2 <= x1 + w1 and x1 <= x2 + w2)
		)