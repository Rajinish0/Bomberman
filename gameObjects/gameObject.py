from point import Point
from handlers import ImageHandler

class GameObject:
    image = None
    level = None
    imageHandler = ImageHandler()

    def __init__(self, position, width, height):
        self.position = position # Point
        self.width = width
        self.height = height


    def draw(self, display):
        pass

    def update(self, dt):
        pass