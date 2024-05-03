from .gameObject import GameObject
from .emptySpace import EmptySpace

class PowerUp(GameObject):
    image = "sprites/gameobjects/grass.jpg"
    def __init__(self, position,width, height):
        super().__init__(position, width, height)
        self.image = self.imgHandler.load(self.image, (width, height))


    def empower(self, player):
        pass

    def Destroy_(self):
        # i, j = self.position.y // self.level.bh, self.position.x // self.level.bw
        self.level.gameobjs[self.position.y][self.position.x] = EmptySpace(self.position, self.level.bw, self.level.bh)

class RangePowerUp(PowerUp):
    image = "sprites/gameobjects/rangePowerup.png"

    def empower(self, player):
        # print("Called ")
        player.incBombRange()
        self.Destroy_()


class BombNumPowerUp(PowerUp):
    image = "sprites/gameobjects/bombPowerup.png"

    def empower(self, player):
        # print("Called ")
        player.incBombCount()
        self.Destroy_()
