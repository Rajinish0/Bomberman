from .gameobject import GameCharacter
from .gameobject import Bomb
import pygame

class Player(GameCharacter):
    def __init__(self,x,y,w,h,speed,keys,image):
        super().__init__(x,y,w,h,speed)
        self.img=self.imgHandler.load(image, (w,h))
        self.keys = keys
        self.wins=0
        self.bombCount=0
        self.bombRange=1
        self.alive=True
        self.bombs=[]

    def update(self):
        if self.eventMgr.keyPressed:
            if self.eventMgr.keyPressed(self.keys['UP']):
                self.y -= 0.1
            elif self.eventMgr.keyPressed(self.keys['DOWN']):
                self.y += 0.1
            elif self.eventMgr.keyPressed(self.keys['RIGHT']):
                self.x += 0.1
            elif self.eventMgr.keyPressed(self.keys['LEFT']):
                self.x -= 0.1
            elif self.eventMgr.keyPressed(self.keys['BOMB']):
                self.placeBomb()

        for b in self.bombs:
            if b.hasFinished():
                self.bombs.remove(b)
                self.incBombCount()

    def draw(self, display):
        display.blit(self.img, (self.x, self.y))

    def incBombCount(self):
        self.bombCount+=1

    def decBombCount(self):
        self.bombCount-=1

    def incBombRange(self):
        self.bombRange+=1

    def Destroy(self):
        self.alive=False

    def placeBomb(self):
        if self.bombCount>0:
            bomb=Bomb(self.x,self.y,self.bombRange)
            self.bombs.append(bomb)
            self.decBombCount()


