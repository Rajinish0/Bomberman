import pygame.draw

from button import Button
from constants import *
from .screen import Screen
import os

class ControlsWindow(Screen):
    def __init__(self):
        self.btn = Button(W / 6, H / 3, 100, 100,
                          callBack=lambda: self.gameMgr.setState(MAIN_WINDOW),
                          img=os.path.join(IMG_PATH, 'start.png'))
        #Buttons PLAYER 1
        self.btnUP1 = Button(550, 140, 50, 50,
                          img=os.path.join(IMG_PATH, 'Solid_white.png'), text="")
        self.btnDOWN1 = Button(550, 210, 50, 50,
                          img=os.path.join(IMG_PATH, 'Solid_white.png'), text="")
        self.btnBOMB1 = Button(550, 280, 200, 45,
                               img=os.path.join(IMG_PATH, 'Solid_white.png'), text="")
        self.btnLEFT1 = Button(480, 210, 50, 50,
                          img=os.path.join(IMG_PATH, 'Solid_white.png'), text="")
        self.btnRIGHT1 = Button(620, 210, 50, 50,
                               img=os.path.join(IMG_PATH, 'Solid_white.png'), text="")

        # Buttons PLAYER 2

    def update(self):
        self.btn.update()

    def draw(self, display):
        background_image = pygame.image.load('sprites/background.png')
        scaled_image = pygame.transform.scale(background_image, (W, H))

        alpha_value_bg = 140
        scaled_image.set_alpha(alpha_value_bg)

        display.blit(scaled_image, (0, 0))

        rect1_surface = pygame.Surface((700, 245), pygame.SRCALPHA)
        pygame.draw.rect(rect1_surface, (238, 238, 238, 225.8), rect1_surface.get_rect(), border_radius=5)
        display.blit(rect1_surface, (50, 82))

        rect2_surface = pygame.Surface((120, 35), pygame.SRCALPHA)
        pygame.draw.rect(rect2_surface, (238, 238, 238, 240), rect2_surface.get_rect(), border_radius=5)
        display.blit(rect2_surface, (490, 30))

        rect3_surface = pygame.Surface((120, 35), pygame.SRCALPHA)
        pygame.draw.rect(rect3_surface, (238, 238, 238, 240), rect2_surface.get_rect(), border_radius=5)
        display.blit(rect3_surface, (630, 30))

        rect4_surface = pygame.Surface((700, 245), pygame.SRCALPHA)
        pygame.draw.rect(rect4_surface, (238, 238, 238, 225.8), rect1_surface.get_rect(), border_radius=5)
        display.blit(rect4_surface, (50, 336))

        # Buttons player 1
        self.btnUP1.draw(display)
        self.btnDOWN1.draw(display)
        self.btnBOMB1.draw(display)
        self.btnLEFT1.draw(display)
        self.btnRIGHT1.draw(display)
