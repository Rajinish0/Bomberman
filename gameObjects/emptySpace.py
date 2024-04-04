from gameObjects.gameObject import GameObject

class EmptySpace(GameObject):
    def __init__(self, position, level):
        super().__init__("empty", position, "sprites/emptySpace.png", level)
    def draw(self, display):
        pass