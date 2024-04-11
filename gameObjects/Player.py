from .gameObject import GameObject
from .gamecharacter import GameCharacter
from .bomb import Bomb
import pygame
from point import Point
from .emptySpace import EmptySpace
from .powerup import PowerUp
from utils import *


class Player(GameCharacter):
    def __init__(self,n,position,speed,image,keys,w,h):
        super().__init__(position, speed)
        self.image=self.imgHandler.load(image,(w,h))
        self.rw = 0.5
        self.rh = 0.7
        self.wins=0
        self.keys=keys
        self.bombCount=1
        self.bombRange=1
        self.alive=True
        self.name=n
        self.bombBox = None

    def update(self):
        keys = pygame.key.get_pressed()
        self.checkForDeath()

        if keys[self.keys["UP"]]:
            self.move(Point(0,-1)*(0.1))

        if keys[self.keys["DOWN"]]:
            self.move(Point(0,1)*(0.1))

        if keys[self.keys["LEFT"]]:
            self.move(Point(-1,0)*(0.1))

        if keys[self.keys["RIGHT"]]:
            self.move(Point(1,0)*(0.1))

        if keys[self.keys["BOMB"]]:
            self.placeBomb()

    def checkForDeath(self):
        for monster in self.level.monsters:
            if (monster.position - self.position).norm() < 1e-7:
                monster.kill(self)
                return

    ## NEED COLLISION B/W TWO RECTANGLES
    def collides(self, p):
        return rectsCollide(
                (self.position.x - self.rw/2, self.position.y - self.rh/2, self.rw, self.rh),
                (p.x - self.rw/2, p.y - self.rh/2, self.rw, self.rh),
            )

    '''
    There's an invariant here: the player is basically a rectangle which has 4 corners.
    The invariant is that the matrix coordinates that these 4 corners refer to are EmptySpaces or
    Powerups. This is true obv at the start because all 4 corners are in the same grid block, the player is moved
    such that this invariant always holds.
    '''

    def move(self, p):
        # if p.y > 0:
            # dp = p.add(Point(0, 1))
        # elif p.x > 0:
            # dp = p.add(Point(1, 0))
        # print(self.position)
        dp= p.add(self.position)

        if isinstance(self.level.gameobjs[int(self.position.y)][int(self.position.x)], Bomb):
            self.position = p.add(self.position) 
            return
        # print(dp)
        # print(dp.y+self.rh/2, dp.x+self.rh/2)
        # print(dp.y-self.rh/2, dp.x-self.rh/2)
        # print(dp.y-self.rh/2, dp.x+self.rw/2)
        # print(dp.y+self.rh/2, dp.x-self.rh/2)

        if (isinstance(self.level.gameobjs[int(dp.y+self.rh/2)][int(dp.x+self.rw/2)],(EmptySpace, PowerUp)) and 
            isinstance(self.level.gameobjs[int(dp.y-self.rh/2)][int(dp.x-self.rw/2)],(EmptySpace, PowerUp)) and
            isinstance(self.level.gameobjs[int(dp.y-self.rh/2)][int(dp.x+self.rw/2)],(EmptySpace, PowerUp)) and 
            isinstance(self.level.gameobjs[int(dp.y+self.rh/2)][int(dp.x-self.rw/2)],(EmptySpace, PowerUp)) ):

            for pl in self.level.players:
                if (not pl is self) and (pl.collides(dp)):
                    return

            self.position = p.add(self.position)

        ## IoU > .5

        if (isinstance(self.level.gameobjs[int(p.y)][int(p.x)], PowerUp)):
            self.position = p.add(self.position)
            self.level.gameobjs[int(p.y)][int(p.x)].empower(self)

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
            bomb=Bomb(Point(int(self.position.x), int(self.position.y)),self.bombRange, self)
            self.level.gameobjs[int(self.position.y)][int(self.position.x)]=bomb
            self.decBombCount()

    def draw(self, display):
        pygame.draw.rect(
            display, (0, 0, 121), ( (self.position.x-self.rw/2)*self.level.bw, (self.position.y-self.rh/2)*self.level.bh, self.rw*self.level.bw, self.rh*self.level.bh )
            )
        super().draw(display)
