import pygame.draw
import pygame
from button import Button
from constants import *
from .screen import Screen
from gamelevel import loadKeys
import os
import pickle


class ControlsWindow(Screen):

    def __init__(self):
        self.btnBack = Button(
            30, 30, 30, 30, text="Back",
            callBack=lambda: (self.gameMgr.setState(MAIN_WINDOW), self.saveKeys())
        )

        self.curr_pressed_key = None
        self.curr_pressed_button = None
        self.keys = loadKeys()

        button_img = os.path.join(IMG_PATH, 'Solid_white.png')
        self.players_command = {
            "p1": {
                "UP": Button(550, 140, 50, 50, img=button_img, textColor=BLACK),
                "DOWN": Button(550, 210, 50, 50, img=button_img, textColor=BLACK),
                "LEFT": Button(480, 210, 50, 50, img=button_img, textColor=BLACK),
                "RIGHT": Button(620, 210, 50, 50, img=button_img, textColor=BLACK),
                "BOMB": Button(550, 280, 200, 45, img=button_img, textColor=BLACK, textSize=25)
            },
            "p2": {
                "UP": Button(550, 390, 50, 50, img=button_img, textColor=BLACK),
                "DOWN": Button(550, 460, 50, 50, img=button_img, textColor=BLACK),
                "LEFT": Button(480, 460, 50, 50, img=button_img, textColor=BLACK),
                "RIGHT": Button(620, 460, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "BOMB": Button(550, 530, 200, 45, img=button_img, textColor=BLACK, textSize=25)
            }
        }

        for player, playerDiction in self.players_command.items():
            for key, button in playerDiction.items():
                button.text = pygame.key.name(self.keys[player][key])

    def saveKeys(self):
        for player, playerDiction in self.players_command.items():
            for key, button in playerDiction.items():
                 self.keys[player][key] = pygame.key.key_code(button.text)

        with open(os.path.join(RSRC_PATH, 'keycfg.pkl'), 'wb') as f:
            keys = pickle.dump(self.keys, f)

    def handleEvent(self, event): # every frame every event
        if event.type == pygame.KEYDOWN:
            self.curr_pressed_key = pygame.key.name(event.key)
            if self.curr_pressed_button:
                self.curr_pressed_button.text = self.curr_pressed_key
    def update(self): # every frame before draw
        self.btnBack.update()
        for player_commands in self.players_command.values():
            for button in player_commands.values():
                button.update()
                if button.pressed:
                    self.curr_pressed_button = button

    def draw(self, display): # Draw is called every frame
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

        for player_commands in self.players_command.values():
            for button in player_commands.values():
                    button.draw(display)

        self.btnBack.draw(display)