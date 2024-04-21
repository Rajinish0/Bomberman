from .gameObject import GameObject
from .emptySpace import  EmptySpace
from constants import *
from .wall import BorderWall
from .wall import Wall 
from .box import Box
from point import Point

class Bomb(GameObject):
    image = "sprites/gameobjects/Bomb.png"
    expImage = "sprites/gameobjects/Bomb.png"
    TIMER_CONST = 10
    EXPLODE_CONST = 3
    def __init__(self, position,range, player):
        super().__init__(position, self.level.bw, self.level.bh)

        self.isExploded = False
        self.range = range
        self.finished = False
        self.i, self.j = (int(position.y), int(position.x))
        self.player = player
        self.timer = Bomb.TIMER_CONST
        self.explodeTimer = Bomb.EXPLODE_CONST
        self.image = self.imgHandler.load(self.image, (self.level.bw, self.level.bh))
        self.expImage = self.imgHandler.load(self.expImage, (self.level.bw, self.level.bh))

    def update(self):
        if not self.finished:
            if not self.isExploded:
                self.timer -= 0.1
                self.isExploded = self.timer <= 0
                if self.isExploded:
                    self.incUp, self.incDown, self.incLeft, self.incRight = self.player.bombRange, self.player.bombRange, self.player.bombRange, self.player.bombRange
            else:
                self.kill()
                self.explodeTimer -= 0.1
                self.finished = self.explodeTimer <= 0
        else:
            self.Destroy()

    def draw_recurse(self, display, i, j, move_i, move_j, depth):
        if depth < 0 or isinstance(self.level.gameobjs[i][j], (Wall,Box)):
            return

        display.blit(self.expImage, (j*self.level.bw, i*self.level.bh) )
        self.draw_recurse(display, i+move_i, j+move_j, move_i, move_j, depth-1)

    def draw(self, display):
        if not self.isExploded:
            super().draw(display)
            # display.blit(self.image, (self.position.x, self.position.y))
        else:
            self.draw_recurse(display, self.i, self.j, 1, 0, self.incDown)
            self.draw_recurse(display, self.i, self.j,-1, 0, self.incUp)
            self.draw_recurse(display, self.i, self.j, 0, 1, self.incRight)
            self.draw_recurse(display, self.i, self.j, 0, -1,self.incLeft)
            # for i in range(max(0,self.i-self.player.bombRange), min(NUM_BOXES, self.i+self.player.bombRange+1)):
            # for i in range(self.i, min(NUM_BOXES, self.i + self.player.bombRange + 1)):
            #     if isinstance(self.level.gameobjs[i][self.j], Wall):
            #         break

            #     display.blit(self.expImage, (self.j * self.level.bw, i * self.level.bh))

            # for i in range(self.i, max(0,self.i-self.player.bombRange-1), -1):
            #     if isinstance(self.level.gameobjs[i][self.j], Wall):
            #         break

            #     display.blit(self.expImage, (self.j * self.level.bw, i * self.level.bh))

            # for j in range(self.j, min(NUM_BOXES, self.j + self.player.bombRange + 1)):
            #     if isinstance(self.level.gameobjs[self.i][j], Wall):
            #         break

            #     display.blit(self.expImage, (j * self.level.bw, self.i * self.level.bh))

            # for j in range(self.j, max(0, self.j - self.player.bombRange-1), -1):
            #     if isinstance(self.level.gameobjs[self.i][j], Wall):
            #         break

            #     display.blit(self.expImage, (j * self.level.bw, self.i * self.level.bh))

    def Destroy(self):
        self.level.gameobjs[self.i][self.j] = EmptySpace(self.position, self.level.bw, self.level.bh)
        self.player.incBombCount()

                                 # 1  
    def kill_recurse(self, i, j, move_i, move_j, depth, counter=0):
        # i = i+move_i
        # j = j+move_j
        if depth < 0 or isinstance(self.level.gameobjs[i][j], BorderWall):
            return counter#+1

        if isinstance(self.level.gameobjs[i][j], Wall):
            return counter#+1
        elif isinstance(self.level.gameobjs[i][j], Bomb) and i != self.i and j != self.j:
            self.level.gameobjs[i][j].explode()
            return counter#+1
        elif isinstance(self.level.gameobjs[i][j], Box):
            self.level.gameobjs[i][j].Destroy()
            return counter+1

        for player in self.level.players:
            if Point.int(player.position) == Point(j, i):
                player.Destroy()
                return counter+1

        for monster in self.level.monsters:
            if Point.int(monster.position) == Point(j, i):
                monster.Destroy()
                return counter+1
        return self.kill_recurse(i+move_i, j+move_j, move_i, move_j, depth-1, counter+1)

    def kill(self):
        self.incDown   = self.kill_recurse(self.i, self.j, 1, 0, self.incDown, -1)
        self.incUp     = self.kill_recurse(self.i, self.j,-1, 0, self.incUp, -1)
        self.incRight  = self.kill_recurse(self.i, self.j, 0, 1, self.incRight, -1)
        self.incLeft   = self.kill_recurse(self.i, self.j, 0,-1, self.incLeft, -1)

        if (Point.int(self.player.position) == self.position and \
            self.player in self.level.players):
            self.player.Destroy()

    # def kill(self):
    #     for i in range(self.i+1, min(NUM_BOXES, self.i + self.player.bombRange + 1)):
    #         if isinstance(self.level.gameobjs[i][self.j], Wall):
    #             break

    #         for player in self.level.players:
    #             if Point.int(player.position) == Point(self.j, i):
    #                 player.Destroy()
    #                 break

    #         for monster in self.level.monsters:
    #             if Point.int(monster.position) == Point(self.j, i):
    #                 monster.Destroy()
    #                 break
    #             # if monster.position.x == self.j * self.level.bw and \
    #                 # monster.position.y == i * self.level.bh:
    #                 # monster.Destroy()
    #                 # break

    #         if isinstance(self.level.gameobjs[i][self.j], Bomb):
    #             self.level.gameobjs[i][self.j].explode()
    #         else:
    #             self.level.gameobjs[i][self.j].Destroy()



    #     for i in range(self.i-1, max(0, self.i - self.player.bombRange - 1), -1):
    #         if isinstance(self.level.gameobjs[i][self.j], Wall):
    #             break

    #         for player in self.level.players:
    #             if Point.int(player.position) == Point(self.j, i):
    #                 player.Destroy()
    #                 break
    #             # if player.position.x == self.j * self.level.bw and \
    #             #         player.position.y == i * self.level.bh:
    #             #     player.Destroy()
    #             #     break

    #         for monster in self.level.monsters:
    #             if Point.int(monster.position) == Point(self.j, i):
    #                 monster.Destroy()
    #                 break
    #             # if monster.position.x == self.j * self.level.bw and \
    #             #         monster.position.y == i * self.level.bh:
    #             #     monster.Destroy()
    #             #     break

    #     if isinstance(self.level.gameobjs[i][self.j], Bomb):
    #         self.level.gameobjs[i][self.j].explode()
    #     else:
    #         self.level.gameobjs[i][self.j].Destroy()

    #     for j in range(self.j+1, min(NUM_BOXES, self.j + self.player.bombRange + 1)):
    #         if isinstance(self.level.gameobjs[self.i][j], Wall):
    #             break

    #         for player in self.level.players:
    #             if Point.int(player.position) == Point(j, self.i):
    #                 player.Destroy()
    #                 break
    #             # if player.position.x == j * self.level.bw and \
    #             #         player.position.y == self.i * self.level.bh:
    #             #     player.Destroy()
    #             #     break

    #         for monster in self.level.monsters:
    #             if Point.int(monster.position )== Point(j, self.i):
    #                 monster.Destroy()
    #                 break
    #             # if monster.position.x == j * self.level.bw and \
    #             #         monster.position.y == self.i * self.level.bh:
    #             #     monster.Destroy()
    #             #     break

    #     if isinstance(self.level.gameobjs[self.i][j], Bomb):
    #         self.level.gameobjs[self.i][j].explode()
    #     else:
    #         self.level.gameobjs[self.i][j].Destroy()

    #     for j in range(self.j-1, max(0, self.j - self.player.bombRange - 1), -1):
    #         if isinstance(self.level.gameobjs[self.i][j], Wall):
    #             break

    #         for player in self.level.players:
    #             if Point.int(player.position) == Point(j, self.i):
    #                 player.Destroy()
    #                 break
    #             # if player.position.x == j * self.level.bw and \
    #             #         player.position.y == self.i * self.level.bh:
    #             #     player.Destroy()
    #             #     break

    #         for monster in self.level.monsters:
    #             if Point.int(monster.position) == Point(j, self.i):
    #                 monster.Destroy()
    #                 break
    #             # if monster.position.x == j * self.level.bw and \
    #             #         monster.position.y == self.i * self.level.bh:
    #             #     monster.Destroy()
    #             #     break

    #     if isinstance(self.level.gameobjs[self.i][j], Bomb):
    #         self.level.gameobjs[self.i][j].explode()
    #     else:
    #         self.level.gameobjs[self.i][j].Destroy()

    #     if (Point.int(self.player.position) == self.position and \
    #         self.player in self.level.players):

    #         self.player.Destroy()

        # if self.player.position.x == self.j * self.level.bw and \
        #     self.player.position.y == self.i * self.level.bh:
        #     if self.player in self.level.players:
        #         self.player.Destroy()

    def explode(self):
        self.isExploded = True

    def has_finished(self):
        return self.finished