from gameObjects.gameObject import GameObject

class Box(GameObject):
    def __init__(self, name, position, image, level):
        super().__init__("box", position, "sprites/box.png", level)
        self.hasPowerup = False
        self.powerUp = None

    def update(self, dt):
        pass

    def draw(self, display):
        pass

    def blowUp(self):
        pass

    def generatePowerUp(self):
        pass