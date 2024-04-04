from gameObjects.gameObject import GameObject

class Wall(GameObject):
    def __init__(self, name, position, image, level):
        super().__init__("wall", position, "sprites/wall.jpeg", level)
    def draw(self, display):
        pass