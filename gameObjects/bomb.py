from .gameObject import GameObject

class Bomb(GameObject):
    image = "sprites/gameobjects/Bomb.png"
    def __init__(self, position, timer, range):
        super().__init__(position)
        self.timer = timer
        self.isExploded = False
        self.range = range
        self.explodeTimer = None
        self.explosionImages = [""] * 5
        self.finished = False
        self.positionOnBoard = (0, 0)

    def update(self, dt):
        pass

    def draw(self, display):
        pass

    def destroy(self):
        pass

    def explode(self):
        self.isExploded = True
        pass

    def has_finished(self):
        return self.finished