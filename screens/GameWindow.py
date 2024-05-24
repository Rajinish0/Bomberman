import math
import pickle

import gamelevel
from screens.screen import Screen
from constants import *
from button import Button
import pygame, os
from utils import *
from fileReading import GridReader
from gameObjects.wall import Wall
from gameObjects.box import Box
from gameObjects.emptySpace import EmptySpace
from gameObjects.Player import Player
from point import Point
from gamelevel import GameLevel


class GameWindow(Screen):
    def __init__(self, file_path=None):
        self.background_image = pygame.image.load(os.path.join('UI', 'background2.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (W, H))
        self.background_surface = pygame.Surface((W, H), pygame.SRCALPHA)
        self.background_surface.blit(self.background_image, (0, 0))
        self.background_surface.set_alpha(70)  # 50% transparency

        self.file_path = file_path
        self.offSetX = 200
        self.offSetY = 0
        self.gameWidth=800-self.offSetX
        self.gameHeight=520-self.offSetY
        self.boxWidth = (self.gameWidth) // NUM_BOXES
        self.boxHeight = (520 - self.offSetY) // NUM_BOXES
        self.level = GameLevel(file_path,self.boxWidth,self.boxHeight)
        self.gamesurface = pygame.Surface((self.gameWidth, self.gameHeight), pygame.SRCALPHA)
        self.infosurface = pygame.Surface((self.gameWidth, (H-self.gameHeight+70)))
        self.pWidth, self.pHeight = int(self.gameWidth*0.75), self.gameHeight//2
        self.popUpWindow = pygame.Surface(  (self.pWidth, self.pHeight), pygame.SRCALPHA )

        # self.pl1Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g1.png'), (50, 70) )
        # self.pl2Image = self.imgHandler.load( os.path.join(IMG_PATH, 'players', 'g2.png'), (50, 70) )
        self.pl1Image = self.imgHandler.load(os.path.join('UI', 'Mira_player.png'), (50, 70))
        self.pl2Image = self.imgHandler.load(os.path.join('UI', 'Thane_player.png'), (50, 70))
        self.timer=5
        self.timeList=[3,2,1]

        self.frame_image = pygame.image.load('UI/frame.png')
        self.frame_image = pygame.transform.scale(self.frame_image, (60, 80))

        self.button_image = pygame.image.load('UI/button.png')
        self.button_image = pygame.transform.scale(self.button_image, (230, 50))

        self.mira_image = pygame.image.load('UI/Mira_green.png')
        self.mira_image = pygame.transform.scale(self.mira_image, (125, 165))

        self.thane_image = pygame.image.load('UI/Thane_green.png')
        self.thane_image = pygame.transform.scale(self.thane_image, (125, 165))

        self.cat_image = pygame.image.load('UI/cat.png')
        self.cat_image = pygame.transform.scale(self.cat_image, (30, 25))
        self.name_fame_image = pygame.image.load('UI/button_clear.png')
        self.name_fame_image = pygame.transform.scale(self.name_fame_image, (W / 3, H / 3+100))
        self.ExitButton = Button(950, 20, 30, 30, textColor=BLACK,
                                 callBack=lambda: pygame.quit(), img='UI/exit.png', textSize=25)

       # self.battleTimer = 14 * 14
        self.backButton = Button(
            330, 35, 60, 65,
            callBack=lambda: self.gameMgr.setState(MAP_WINDOW),
            img='UI/wizard_no_cat.png'
        )

        # self.nextButton=Button(
        #     W/2,H/2+40,30,30,text="Next Round",
        #     callBack=lambda :(self.level.nextRound(),
        #                       resetCursor())
        # )
        self.menuButton=Button(
            W / 2, H / 2 + 40, 140, 30, text="Go to Menu", textSize=10,img="UI/button_clear.png",center=True,
            callBack=lambda: self.gameMgr.setState(MAIN_WINDOW),
            textColor = BLACK
        )
        self.restartButton=Button(
            W / 2, H / 2 + 80, 140, 30, text="Restart Game", textSize=10,img="UI/button_clear.png",center=True,
            callBack=lambda: (self.level.restart(),
                              resetCursor()),
            textColor = BLACK
        )


    def update(self):
        self.backButton.update()
        self.level.update()

        if self.level.finished:
            self.menuButton.update()
            self.restartButton.update()
        elif self.level.gameEnd:
            if self.timer>0:
                self.timer-=1/FPS
            else:
                self.level.nextRound()
                self.timer = 5
                self.level.nextRound()

    def getTimer(self):
        if self.level.brTimer<=0:
            return ("00:00",RED)
        else:
            min=str(math.floor(math.ceil(self.level.brTimer)/60)).zfill(2)
            sec=str(math.ceil(self.level.brTimer)%60).zfill(2)
            text=min+":"+sec
            if self.level.brTimer<4:
                # print(self.level.brTimer)
                return (text,RED)
            else:
                return (text,BLACK)

    def getBattleTimer(self):
        if self.level.battleTimer<=0:
            return ("00:00",RED)
        min=str(math.floor(math.ceil(self.level.battleTimer)/60)).zfill(2)
        sec=str(math.ceil(self.level.battleTimer)%60).zfill(2)
        text=min+":"+sec
        return (text,RED)


    def draw(self, display):
        display.fill((114, 125, 104))
        # display.blit(self.background_surface, (0, 0))

        self.gamesurface.fill((114, 125, 104))

        # self.infosurface.fill((114, 125, 104))
        # self.infosurface.blit(self.pl1Image, (0, 0))

       #self.infosurface.blit(self.pl2Image, ((self.gameWidth)-50, 0))
        self.backButton.draw(display)
        timer = self.getTimer()
        display.blit(self.button_image, (390, 10))
        drawText(display,timer[0],390+115,35,size=18,color=timer[1],center=True)

        display.blit(self.mira_image, (30, 100))
        display.blit(self.thane_image, (840, 100))
        drawText(display,self.level.player1Wins,30+125/2,300,size=40,center=True,color=WHITE)
        drawText(display,self.level.player2Wins,840+125/2,300,size=40,center=True,color=WHITE)

        display.blit(self.cat_image, (615, 44))
        self.ExitButton.draw(display)

        # for i in range(12):
        #     display.blit(self.frame_image, (950, -15 + i * y_increment))
        # if not self.level.brTimer <= 0:
        #     timer=self.getTimer()
        #     drawText(self.infosurface,timer[0],self.gameWidth/2,30,size=50,color=timer[1],center=True)
        # else:
        #     timer = self.getBattleTimer()
        #     drawText(self.infosurface, timer[0], self.gameWidth / 2, 30, size=50, color=timer[1], center=True)

        # drawText(self.infosurface,self.level.pl1Name,55,10,size=18,color=WHITE,center=False)
        # drawText(self.infosurface, self.level.player1Wins, 55, 30, size=18, color=WHITE, center=False)
        # drawText(self.infosurface, self.level.pl2Name, (self.gameWidth)-55, 10, size=18, color=WHITE, center=False, right=True)
        # drawText(self.infosurface, self.level.player2Wins, (self.gameWidth)-55, 30, size=18, color=WHITE, center=False,right=True)
        if self.level.finished:
            self.timer=5
           # pygame.draw.rect(self.popUpWindow, (238, 238, 238, 240), self.popUpWindow.get_rect(), border_radius=8)

            display.blit(self.name_fame_image,(W/2-W/6,H/2-H/6))
            text=self.level.players[0].name+ " has won!!!"

            self.level.draw(self.gamesurface)
            #display.blit(self.infosurface, (200, 5))
            display.blit(self.gamesurface, (200, 70))
            #display.blit(self.popUpWindow, (W/2 - self.pWidth/2, H/2 - self.pHeight/2) )

            display.blit(self.name_fame_image, (W / 2 - W / 6, H / 2 - H / 6-50))
            drawText(display, text, W / 2, H / 2 - 50, color=BLACK,size=18)
            self.menuButton.draw(display)
            self.restartButton.draw(display)

        elif self.level.gameEnd:
            self.level.draw(self.gamesurface)

            text = "No one won this round!!!"
            if self.level.players:
                text = self.level.players[0].name+" has won the round!!!"

            # display.blit(self.infosurface, (200, 5))
            display.blit(self.gamesurface, (200, 70))
            drawText(display,text,W/2,H/2,color=WHITE,size=20)
            drawText(display,math.ceil(self.timer), W / 2, H / 2 +100,color=WHITE,size=50)


            # self.nextButton.draw(display)
        else:
            self.level.draw(self.gamesurface)
            # display.blit(self.infosurface, (200, 5))
            display.blit(self.gamesurface, (200, 70))











