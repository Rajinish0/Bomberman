from point import Point

class GameObject:
    image = None
    level = None
    def __init__(self, position):
        self.position = position # Point


    def draw(self, display):
        pass

    def update(self, dt):
        pass