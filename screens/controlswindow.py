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
        self.saveBtn = Button(
            70, 60, 30, 35, text="Save",
            callBack=lambda: (self.saveKeys())
        )

        self.defaultBtn = Button(
            140, 60, 30, 35, text="Default",
            callBack=lambda: (self.defaultKeys())
        )

        self.menuBtn = Button(
            660, 60, 30, 35, text="Menu",
            callBack=lambda: (self.setUp(), self.gameMgr.setState(MAIN_WINDOW))
        )

        self.helpBtn = Button(
            730, 60, 30, 35, text="Help",
            callBack=lambda: (self.helpSurface())
        )

        # self.okBtn = Button(
        #     730, 60, 30, 35, text="Help",
        #     callBack=lambda: (self.helpSurface())
        # )

        button_img = os.path.join(IMG_PATH, 'Solid_white.png')
        self.curr_pressed_key = None
        self.curr_pressed_button = None
        self.keys = loadKeys()
        self.assigned_keys = set()
        self.save_pressed = False

        self.players_command = {
            "p1": {
                "UP": Button(550, 140, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "DOWN": Button(550, 210, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "LEFT": Button(480, 210, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "RIGHT": Button(620, 210, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "BOMB": Button(550, 280, 200, 45, img=button_img, textColor=BLACK, textSize=25)
            },
            "p2": {
                "UP": Button(550, 390, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "DOWN": Button(550, 460, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "LEFT": Button(480, 460, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "RIGHT": Button(620, 460, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "BOMB": Button(550, 530, 200, 45, img=button_img, textColor=BLACK, textSize=20)
            }
        }

        for player, playerDiction in self.players_command.items():
            for key, button in playerDiction.items():
                button.text = pygame.key.name(self.keys[player][key])
                self.assigned_keys.add(pygame.key.name(self.keys[player][key]))

    def saveKeys(self):
        self.save_pressed = True
        for player, playerDiction in self.players_command.items():
            for key, button in playerDiction.items():
                key_code = pygame.key.key_code(button.text)
                self.keys[player][key] = key_code

        with open(os.path.join(RSRC_PATH, 'keycfg.pkl'), 'wb') as f:
            keys = pickle.dump(self.keys, f)

    def setUp(self):
        if not self.save_pressed:
            self.defaultKeys()

    def defaultKeys(self):
        self.keys = {
            "p1": {
                "UP": pygame.K_w,
                "DOWN": pygame.K_s,
                "LEFT": pygame.K_a,
                "RIGHT": pygame.K_d,
                "BOMB": pygame.K_SPACE
            },
            "p2": {
                "UP": pygame.K_UP,
                "DOWN": pygame.K_DOWN,
                "LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT,
                "BOMB": pygame.K_RETURN
            }
        }

        self.assigned_keys=set()
        for player, playerDiction in self.players_command.items():
            for key, button in playerDiction.items():
                button.text = pygame.key.name(self.keys[player][key])
                self.assigned_keys.add(pygame.key.name(self.keys[player][key]))


        with open(os.path.join(RSRC_PATH, 'keycfg.pkl'), 'wb') as f:
            keys = pickle.dump(self.keys, f)


    def handleEvent(self, event): # every frame every event
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) not in self.assigned_keys:
                self.curr_pressed_key = pygame.key.name(event.key)
                if self.curr_pressed_button:
                    if self.curr_pressed_button.text:
                        self.assigned_keys.remove(self.curr_pressed_button.text)
                        self.curr_pressed_button.text = self.curr_pressed_key
                        self.assigned_keys.add(self.curr_pressed_button.text)
            else:
                pass
                # print("no duplicates allowed")
    def update(self): # every frame before draw
        self.menuBtn.update()
        self.saveBtn.update()
        self.helpBtn.update()
        self.defaultBtn.update()

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

        rect2_surface = pygame.Surface((700, 245), pygame.SRCALPHA)
        pygame.draw.rect(rect2_surface, (238, 238, 238, 225.8), rect1_surface.get_rect(), border_radius=5)
        display.blit(rect2_surface, (50, 336))

        for player_commands in self.players_command.values():
            for button in player_commands.values():
                    button.draw(display)

        self.saveBtn.draw(display)
        self.menuBtn.draw(display)
        self.helpBtn.draw(display)
        self.defaultBtn.draw(display)

        # help_surface = pygame.Surface((700, 500), pygame.SRCALPHA)
        # pygame.draw.rect(help_surface, (238, 238, 238, 250), help_surface.get_rect(), border_radius=5)
        # display.blit(help_surface, (50, 82))

