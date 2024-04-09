from .gameObject import GameObject
from .gamecharacter import GameCharacter
from .bomb import Bomb
import pygame
from point import Point
from .emptySpace import EmptySpace
from .powerup import PowerUp


class Player(GameCharacter):
    def __init__(self,n,position,speed,image,keys,w,h):
        super().__init__(position, speed)
        self.image=self.imgHandler.load(image,(w,h))
        self.wins=0
        self.keys=keys
        self.bombCount=1
        self.bombRange=1
        self.alive=True
        self.name=n

    def update(self):
        keys = pygame.key.get_pressed()
        self.checkForDeath()

        if keys[self.keys["UP"]]:
            self.move(Point(0,-1))

        elif keys[self.keys["DOWN"]]:
            self.move(Point(0,1))

        elif keys[self.keys["LEFT"]]:
            self.move(Point(-1,0))

        elif keys[self.keys["RIGHT"]]:
            self.move(Point(1,0))

        elif keys[self.keys["BOMB"]]:
            self.placeBomb()

    def checkForDeath(self):
        for monster in self.level.monsters:
            if monster.position == self.position:
                monster.kill(self)
                return

    def move(self, p):
        p= p.add(self.position)

        if (isinstance(self.level.gameobjs[p.y][p.x],EmptySpace)):

            for pl in self.level.players:
                if pl.position == p:
                    return

            self.position = p

        if (isinstance(self.level.gameobjs[p.y][p.x], PowerUp)):
            self.position = p
            self.level.gameobjs[p.y][p.x].empower(self)

            # for pl in self.level.players:
            #     if pl.position == p:
            #         self.level.gameobjs[p.y][p.x].empower(pl)


    def incBombCount(self):
        self.bombCount+=1

    def decBombCount(self):
        self.bombCount-=1

    def incBombRange(self):
        self.bombRange+=1

    def Destroy(self):
        self.level.startEnd(self)

        self.alive=False

    def placeBomb(self):
        if self.bombCount>0:
            bomb=Bomb(self.position,self.bombRange, self)
            self.level.gameobjs[self.position.y][self.position.x]=bomb
            self.decBombCount()


