import pygame.draw
import pygame
from button import Button
from constants import *
from .screen import Screen
import os

class ControlsWindow(Screen):

    def __init__(self):
        self.btnBack = Button(
            30, 30, 30, 30, text="Back",
            callBack=lambda: self.gameMgr.setState(MAIN_WINDOW)
        )
        self.curr_pressed_key = None

        self.curr_pressed_button = None

        self.player1commands = []
        self.player2commands = []

        self.button_list = [
            Button(550, 140, 50, 50, textColor=GREEN),
            Button(550, 210, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnDOWN1
            Button(550, 280, 200, 45, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnBOMB1
            Button(480, 210, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnLEFT1
            Button(620, 210, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnRIGHT1
            Button(550, 390, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnUP2
            Button(550, 460, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnDOWN2
            Button(550, 530, 200, 45, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnBOMB2
            Button(480, 460, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN),  # self.btnLEFT2
            Button(620, 460, 50, 50, img=os.path.join(IMG_PATH, 'Solid_white.png'), textColor=GREEN)  # self.btnRIGHT2
        ]

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.curr_pressed_key = str(pygame.key.name(event.key))
            if self.curr_pressed_button:
                self.curr_pressed_button.text = self.curr_pressed_key

    def update(self):
        self.btnBack.update()
        for button in self.button_list:
            button.update()
            if button.pressed:
                self.curr_pressed_button = button


    def draw(self, display):
        display.fill((110, 161, 100))
        # background_image = pygame.image.load('sprites/background.png')
        # scaled_image = pygame.transform.scale(background_image, (W, H))
        # alpha_value_bg = 140
        # scaled_image.set_alpha(alpha_value_bg)
        # display.blit(scaled_image, (0, 0))

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

        for button in self.button_list:
            button.draw(display)

        self.btnBack.draw(display)