import random

from .gameObject import GameObject
from point import Point
from .gamecharacter import GameCharacter
from .Player import Player

class Monster(GameCharacter):
    def __init__(self,position,speed,image,direction,w,h):
        super().__init__(position,speed)
        self.img=self.imgHandler.load(image, (w,h))
        self.direction=direction
        self.alive=True
        self.t = 1

    def draw(self, display):
        display.blit(self.img, (self.position.x, self.position.y))

    def update(self):
        if self.t < 0:
            self.randomDecision()
            if(not self.move(self.direction,isPlayer=False)):
                self.makeDecision()
            else:
                for pl in self.level.players:
                    if(pl.position.x == self.position.x and pl.position.y == self.position.y):
                        self.kill(pl)


            self.t = 1
        self.t -= 0.5

    def makeDecision(self):
        directions=[Point(0,-1),Point(0,1),Point(1,0),Point(-1,0)]
        self.direction=random.choice(directions)

    def randomDecision(self):
        x=random.choice(range(0,100))
        if(x>90):
            self.makeDecision()


    def kill(self,player):
        player.Destroy()

    def Destroy(self):
        self.alive=False
