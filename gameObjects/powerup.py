from .gameObject import GameObject
from .emptySpace import EmptySpace

class PowerUp(GameObject):
    image = "sprites/gameobjects/grass.jpg"
    def __init__(self, position,width, height):
        super().__init__(position)
        self.image = self.imgHandler.load(self.image, (width, height))
    def draw(self, display):
        display.blit(self.image, (self.position.x, self.position.y))

    def empower(self, player):
        pass

    def Destroy_(self):
        i, j = self.position.y // self.level.bh, self.position.x // self.level.bw
        self.level.gameobjs[i][j] = EmptySpace(self.position, self.level.bw, self.level.bh)

class RangePowerUp(PowerUp):
    image = "sprites/orange.png"

    def empower(self, player):
        print("Called ")
        player.incBombRange()
        self.Destroy_()


class BombNumPowerUp(PowerUp):
    image = "sprites/Solid_white.png"

    def empower(self, player):
        print("Called ")
        player.incBombCount()
        self.Destroy_()
