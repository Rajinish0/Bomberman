import random, pygame

from .gameObject import GameObject
from point import Point
from .gamecharacter import GameCharacter
from .Player import Player
from .powerup import PowerUp
from .emptySpace import EmptySpace 

class Monster(GameCharacter):
    def __init__(self,position,speed,image,direction,w,h):
        super().__init__(position,speed)
        self.image=self.imgHandler.load(image, (w,h))
        self.rw = .9999
        self.rh = .9999
        self.direction=direction
        self.alive=True
        self.t = 1

    def update(self):
        self.randomDecision()
        if(not self.move(self.direction*0.05)):
            self.makeDecision()
        else:
            for pl in self.level.players:
                if Point.int(pl.position) == Point.int(self.position):
                    self.kill(pl)


    def isValid(self, coord):
        mvi, mvj = coord         
        return isinstance(self.level.gameobjs[mvi][mvj],(EmptySpace, PowerUp))

    '''
    READ Player.move, the same invariant is used here.
    '''

    def move(self,p):
        dp= p.add(self.position)

        if self.isValid( ( int(dp.y+self.rh/2), int(dp.x+self.rw/2) ) ) and\
           self.isValid( ( int(dp.y-self.rh/2), int(dp.x-self.rw/2) ) ) and\
           self.isValid( ( int(dp.y-self.rh/2), int(dp.x+self.rw/2) ) ) and\
           self.isValid( ( int(dp.y+self.rh/2), int(dp.x-self.rw/2) ) ):
           self.position = dp 
           return True 

        return False

    def makeDecision(self):
        directions=[Point(0,-1),Point(0,1),Point(1,0),Point(-1,0)]
        self.direction=random.choice(directions)

    def randomDecision(self):
        x=random.choice(range(0,100))
        if(x>96):
            self.makeDecision()

    # def draw(self, display):
    #     pygame.draw.rect(
    #         display, (0, 0, 121), ( (self.position.x-self.rw/2)*self.level.bw, (self.position.y-self.rh/2)*self.level.bh, self.rw*self.level.bw, self.rh*self.level.bh )
    #         )
    #     super().draw(display)


    def kill(self,player):
        player.Destroy()

    def Destroy(self):
        self.level.monsters.remove(self)
        self.alive=False
