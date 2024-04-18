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
        self.rw = .7
        self.rh = .7
        self.wins=0
        self.keys=keys
        self.bombCount=1
        self.bombRange=1
        self.alive=True
        self.name=n
        self.bombBox = []

    def update(self):
        keys = pygame.key.get_pressed()
        self.checkForDeath()

        if keys[self.keys["UP"]]:
            self.move(Point(0,-1)*(self.speed))

        if keys[self.keys["DOWN"]]:
            self.move(Point(0,1)*(self.speed))

        if keys[self.keys["LEFT"]]:
            self.move(Point(-1,0)*(self.speed))

        if keys[self.keys["RIGHT"]]:
            self.move(Point(1,0)*(self.speed))

        if keys[self.keys["BOMB"]]:
            self.placeBomb()

    def checkForDeath(self):
        for monster in self.level.monsters:
            if Point.int(monster.position) == Point.int(self.position):
                monster.kill(self)
                return

    ## COLLISION B/W TWO RECTANGLES
    def collides(self, p):
        return rectsCollide(
                (self.position.x - self.rw/2, self.position.y - self.rh/2, self.rw, self.rh),
                (p.x - self.rw/2, p.y - self.rh/2, self.rw, self.rh),
            )

    def isValid(self, coord, any_):
        mvi, mvj = coord         
        if isinstance(self.level.gameobjs[mvi][mvj],(EmptySpace, PowerUp)):
            return True
        elif coord in self.bombBox:
            any_.append((mvi, mvj))
        # elif self.bombBox and (mvi == self.bombBox[0]) and (mvj == self.bombBox[1]):
            # any_[0] = True
            return True
        return False
    '''
    There's an invariant here: the player is basically a rectangle which has 4 corners.
    The invariant is that the matrix coordinates that these 4 corners refer to are EmptySpaces or
    Powerups. This is true obv at the start because all 4 corners are in the same grid block, the player is moved
    such that this invariant always holds.


    Logic for player on top of bomb:
    So, when the player plants a bomb it can move around in that box, when it leaves that box it cannot enter that box again (so long as the bomb is there).
    Everytime a player plants a bomb the coordinates of that bomb are stored in bombBox array and then if any of the 4 corners of the player
    are in bombBox array it can still move around; however if none of the 4 corners of the players are in bombBox array
    then the coordinates of the bomb are removed from the bombBox array - this stops the player from moving back into the box 
    with the bomb.

    A bomb's coords will not be in bombBox array after it has exploded because other wise the player would have died.
    '''

    def move(self, p):
        # if p.y > 0:
            # dp = p.add(Point(0, 1))
        # elif p.x > 0:
            # dp = p.add(Point(1, 0))
        # print(self.position)
        dp= p.add(self.position)

        any_ = []

        if self.isValid( ( int(dp.y+self.rh/2), int(dp.x+self.rw/2) ), any_ ) and\
           self.isValid( ( int(dp.y-self.rh/2), int(dp.x-self.rw/2) ), any_ ) and\
           self.isValid( ( int(dp.y-self.rh/2), int(dp.x+self.rw/2) ), any_ ) and\
           self.isValid( ( int(dp.y+self.rh/2), int(dp.x-self.rw/2) ), any_ ):

            for coord in self.bombBox:
                if coord not in any_:
                    self.bombBox.remove(coord)

            # if not any_[0]: self.bombBox = []

            for pl in self.level.players:
                if (not pl is self) and (pl.collides(dp)):
                    return

            self.position = p.add(self.position)

        ## IoU > .5

        if (isinstance(self.level.gameobjs[int(dp.y)][int(dp.x)], PowerUp)):
            self.position = p.add(self.position)
            self.level.gameobjs[int(dp.y)][int(dp.x)].empower(self)

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
        i, j = (int(self.position.y), int(self.position.x))
        if self.bombCount>0 and (not ( (i,j) in self.bombBox ) ):
            bomb=Bomb(Point(j, i),self.bombRange, self)
            self.level.gameobjs[i][j]=bomb
            self.decBombCount()
            self.bombBox.append((i, j))
            # self.bombBox = (i, j)

    # def draw(self, display):
    #     pygame.draw.rect(
    #         display, (0, 0, 121), ( (self.position.x-self.rw/2)*self.level.bw, (self.position.y-self.rh/2)*self.level.bh, self.rw*self.level.bw, self.rh*self.level.bh )
    #         )
    #     super().draw(display)
