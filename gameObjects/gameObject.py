from point import Point

class GameObject:
    def __init__(self, name, position, image, level):
        self.name = name
        self.position = position # Point
        self.image = image
        self.level = level

    def draw(self, display):
        pass

    def update(self, dt):
        pass