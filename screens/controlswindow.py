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
        self.ExitButton = Button(920, 70, 30, 30, textColor=BLACK,
                                 callBack=lambda: pygame.quit(), img='UI/exit.png', textSize=25)

        self.saveBtn = Button(
            250, 85, 30, 35,
            callBack=lambda: (self.saveKeys()), img="UI/save.png"
        )

        self.defaultBtn = Button(
            200, 85, 30, 35,
            callBack=lambda: (self.defaultKeys()), img="UI/delete.png"
        )

        self.menuBtn = Button(
            150, 85, 30, 35,
            callBack=lambda: (self.setUp(), self.gameMgr.setState(MAIN_WINDOW)), img="UI/wizard2.png"
        )

        button_img = os.path.join('UI/key.png')
        self.curr_pressed_key = None
        self.curr_pressed_button = None
        self.keys = loadKeys()
        self.assigned_keys = set()
        self.save_pressed = False

        self.players_command = {
            "p1": {
                "UP": Button(650, 160, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "DOWN": Button(650, 215, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "RIGHT": Button(705, 215, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "LEFT": Button(595, 215, 50, 50, img=button_img, textColor=BLACK, textSize=20),
                "BOMB": Button(650, 270, 200, 40, img=button_img, textColor=BLACK, textSize=18)
            },
            "p2": {
                "UP": Button(650, 385, 50, 50, img=button_img, textColor=BLACK, textSize=10),
                "DOWN": Button(650, 440, 50, 50, img=button_img, textColor=BLACK, textSize=10),
                "RIGHT": Button(705, 440, 50, 50, img=button_img, textColor=BLACK, textSize=9),
                "LEFT": Button(595, 440, 50, 50, img=button_img, textColor=BLACK, textSize=9),
                "BOMB": Button(650, 495, 200, 40, img=button_img, textColor=BLACK, textSize=18)
            }
        }
        self.frame_image = pygame.image.load('UI/frame.png')
        self.frame_image = pygame.transform.scale(self.frame_image, (60, 80))

        self.control_image = pygame.image.load('UI/controls_panel.png')
        self.control_image = pygame.transform.scale(self.control_image, (760, 220))

        for player, playerDiction in self.players_command.items():
            for key, button in playerDiction.items():
                button.text = pygame.key.name(self.keys[player][key])
                self.assigned_keys.add(pygame.key.name(self.keys[player][key]))

    def saveKeys(self):
        self.save_pressed = True
        self.curr_pressed_button=None
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
        self.curr_pressed_button=None
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
        self.defaultBtn.update()
        self.ExitButton.update()

        for player_commands in self.players_command.values():
            for button in player_commands.values():
                button.update()
                if button.pressed:
                    self.curr_pressed_button = button



    def draw(self, display): # Draw is called every frame
        display.fill((114, 125, 104))
        display.blit(self.control_image, (105, 325))
        display.blit(self.control_image, (105, 100))

        for player_commands in self.players_command.values():
            for button in player_commands.values():
                    button.draw(display)

        if self.curr_pressed_button:
            self.curr_pressed_button.draw(display,Border=True)

        self.saveBtn.draw(display)
        self.menuBtn.draw(display)
        self.defaultBtn.draw(display)

        x_increment = 50
        frame_rotated_image = pygame.transform.rotate(self.frame_image, +90)
        for i in range(20):
            display.blit(frame_rotated_image, (30 + i * x_increment, -15))

        frame_rotated_image = pygame.transform.rotate(self.frame_image, -90)
        for i in range(20):
            display.blit(frame_rotated_image, (35 + i * x_increment, 550))

        y_increment = 50
        frame_rotated_image = pygame.transform.rotate(self.frame_image, -180)
        for i in range(12):
            display.blit(frame_rotated_image, (-15, -15 + i * y_increment))

        for i in range(12):
            display.blit(self.frame_image, (950, -15 + i * y_increment))

        self.ExitButton.draw(display)



