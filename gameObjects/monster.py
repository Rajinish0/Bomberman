import random

from .gameobject import GameCharacter
from .gameobject import Player

class Player(GameCharacter):
    def __init__(self,x,y,w,h,speed,image,direction):
        super().__init__(x,y,w,h,speed)
        self.img=self.imgHandler.load(image, (w,h))
        self.direction=direction
        self.alive=True

    def draw(self, display):
        display.blit(self.img, (self.x, self.y))

    def update(self):
        if self.direction=="UP":
            self.y -= 0.1
        elif self.direction=="DOWN":
            self.y += 0.1
        elif self.direction=="RIGHT":
            self.x += 0.1
        elif self.direction=="LEFT":
            self.x -= 0.1

    def makeDecision(self):
        directions=["UP","DOWN","RIGHT","LEFT"]
        directions.remove(self.direction)
        self.direction=random.choice(directions)


    def kill(self,player):
        player.Destroy()

    def Destroy(self):
        self.alive=False
