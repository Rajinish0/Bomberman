from .gameObject import GameObject
from .emptySpace import  EmptySpace
from constants import *
from .wall import Wall

class Bomb(GameObject):
    image = "sprites/gameobjects/Bomb.png"
    expImage = "sprites/gameobjects/Bomb.png"
    TIMER_CONST = 5
    EXPLODE_CONST = 3
    def __init__(self, position, range, player):
        super().__init__(position)

        self.isExploded = False
        self.range = range
        self.finished = False
        self.i, self.j = (position.y // self.level.bh, position.x // self.level.bw)
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
            else:
                self.kill()
                self.explodeTimer -= 0.1
                self.finished = self.explodeTimer <= 0
        else:
            self.Destroy()

    def draw(self, display):
        if not self.isExploded:
            display.blit(self.image, (self.position.x, self.position.y))
        else:
            # for i in range(max(0,self.i-self.player.bombRange), min(NUM_BOXES, self.i+self.player.bombRange+1)):
            for i in range(self.i, min(NUM_BOXES, self.i + self.player.bombRange + 1)):
                if isinstance(self.level.gameobjs[i][self.j], Wall):
                    break

                display.blit(self.expImage, (self.j * self.level.bw, i * self.level.bh))

            for i in range(self.i, max(0,self.i-self.player.bombRange-1), -1):
                if isinstance(self.level.gameobjs[i][self.j], Wall):
                    break

                display.blit(self.expImage, (self.j * self.level.bw, i * self.level.bh))

            for j in range(self.j, min(NUM_BOXES, self.j + self.player.bombRange + 1)):
                if isinstance(self.level.gameobjs[self.i][j], Wall):
                    break

                display.blit(self.expImage, (j * self.level.bw, self.i * self.level.bh))

            for j in range(self.j, max(0, self.j - self.player.bombRange-1), -1):
                if isinstance(self.level.gameobjs[self.i][j], Wall):
                    break

                display.blit(self.expImage, (j * self.level.bw, self.i * self.level.bh))

    def Destroy(self):
        self.level.gameobjs[self.i][self.j] = EmptySpace(self.position, self.level.bw, self.level.bh)
        self.player.incBombCount()

    def kill(self):
        for i in range(self.i+1, min(NUM_BOXES, self.i + self.player.bombRange + 1)):
            if isinstance(self.level.gameobjs[i][self.j], Wall):
                break

            for player in self.level.players:
                if player.position.x == self.j * self.level.bw and \
                    player.position.y == i * self.level.bh:
                    player.Destroy()
                    break

            for monster in self.level.monsters:
                if monster.position.x == self.j * self.level.bw and \
                    monster.position.y == i * self.level.bh:
                    monster.Destroy()
                    break

            self.level.gameobjs[i][self.j].Destroy()



        for i in range(self.i-1, max(0, self.i - self.player.bombRange - 1), -1):
            if isinstance(self.level.gameobjs[i][self.j], Wall):
                break

            for player in self.level.players:
                if player.position.x == self.j * self.level.bw and \
                        player.position.y == i * self.level.bh:
                    player.Destroy()
                    break

            for monster in self.level.monsters:
                if monster.position.x == self.j * self.level.bw and \
                        monster.position.y == i * self.level.bh:
                    monster.Destroy()
                    break

            self.level.gameobjs[i][self.j].Destroy()

        for j in range(self.j+1, min(NUM_BOXES, self.j + self.player.bombRange + 1)):
            if isinstance(self.level.gameobjs[self.i][j], Wall):
                break

            for player in self.level.players:
                if player.position.x == j * self.level.bw and \
                        player.position.y == self.i * self.level.bh:
                    player.Destroy()
                    break

            for monster in self.level.monsters:
                if monster.position.x == j * self.level.bw and \
                        monster.position.y == self.i * self.level.bh:
                    monster.Destroy()
                    break

            self.level.gameobjs[self.i][j].Destroy()

        for j in range(self.j-1, max(0, self.j - self.player.bombRange - 1), -1):
            if isinstance(self.level.gameobjs[self.i][j], Wall):
                break

            for player in self.level.players:
                if player.position.x == j * self.level.bw and \
                        player.position.y == self.i * self.level.bh:
                    player.Destroy()
                    break

            for monster in self.level.monsters:
                if monster.position.x == j * self.level.bw and \
                        monster.position.y == self.i * self.level.bh:
                    monster.Destroy()
                    break

            self.level.gameobjs[self.i][j].Destroy()

        if self.player.position.x == self.j * self.level.bw and \
            self.player.position.y == self.i * self.level.bh:
            if self.player in self.level.players:
                self.player.Destroy()

    def explode(self):
        self.isExploded = True
        pass

    def has_finished(self):
        return self.finished