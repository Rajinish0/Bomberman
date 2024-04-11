import random

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
        self.direction=direction
        self.alive=True
        self.t = 1

    def update(self):
        if self.t < 0:
            self.randomDecision()
            if(not self.move(self.direction)):
                self.makeDecision()
            else:
                for pl in self.level.players:
                    if (pl.position - self.position).norm() < 1e-7:
                        self.kill(pl)
                    # if (pl.position.x == self.position.x and pl.position.y == self.position.y):
                    #     self.kill(pl)


            self.t = 1
        self.t -= 0.5


    def move(self,p):
        p= p.add(self.position)

        if (isinstance(self.level.gameobjs[int(p.y)][int(p.x)], (EmptySpace, PowerUp))):
            self.position=p
            return True

        return False

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
        self.level.monsters.remove(self)
        self.alive=False
