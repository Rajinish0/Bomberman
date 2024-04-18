from .gameObject import GameObject
import os
from point import Point
from .wall import Wall
from .emptySpace import EmptySpace
from .powerup import *



'''
There were two reasons for choosing game character's position to be defined as the center coord 
instead of the top left.

1. Imagine the player is moving down, and there's a power up there. Then the player should be able 
to pick it up as soon as more than 50% of it is in the box. If the player's position is defined as its center coord
then this will follow naturally, in the other case (of top left coords) all of the player would need to be on top of 
the powerup to pick it up if the player is moving down. Or imagine if the player is moving to the left then only if the player
is slightly in the box, the powerup would be picked. Ofc since the monster collision is handled the same way, similar thing would 
happen for monsters killing players.


2. Suppose we stored the top left coordinates: The image that we draw is draw on the top left coordinate - it has transparent background. If let's say the relative width and height
of the player were 0.5 and 0.5, so the player is half as big as a box, then since we are drawing the image on the top left coordinate it would be extremely difficult to know
where the player is actually in the image. Since given an image the player is usually in the middle of the image with some height and width usually smaller than the image.
It is better to store the center coordinates and estimate player's height and width as relative height and width -- relative to the actual image.

'''
class GameCharacter(GameObject):
    def __init__(self,position,speed):
        super().__init__(position, self.level.bw, self.level.bh)
        self.position = self.position.add(Point(0.5, 0.5))
        self.speed=speed


    def update(self):
        pass

    def draw(self, display):
        x = self.position.x * self.w
        y = self.position.y * self.h
        x -= self.w //2 
        y -= self.h // 2

        display.blit(self.image, (x, y))


    # def move(self,p, isPlayer=True):
    #     p= p.add(self.position)

    #     if(isinstance(self.level.gameobjs[p.y][p.x],EmptySpace)):

    #         if isPlayer:
    #             for pl in self.level.players:

    #                 if pl.position == p:
    #                     return False
    #                 # if (pl.position.x == p.x and pl.position.y == p.y):

    #                 #     return False

    #         self.position=p
    #         return True
    #     if (isinstance(self.level.gameobjs[p.y][p.x], PowerUp)):
    #         self.position = p
    #         if isPlayer:
    #             for pl in self.level.players:
    #                 if pl.position == p:
    #                     self.level.gameobjs[p.y][p.x].empower(pl)                    
    #                 # if(pl.position.x == p.x and pl.position.y == p.y):
    #                 #     print("Correct position")
    #                 #     self.level.gameobjs[p.y // self.level.bh][p.x // self.level.bw].empower(pl)


    #         return True

    #     return False