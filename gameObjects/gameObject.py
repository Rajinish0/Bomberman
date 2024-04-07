from point import Point
from handlers import ImageHandler

class GameObject:
    imgHandler=ImageHandler()
    image = None
    level = None
    def __init__(self, position):
        self.position = position # Point

    @staticmethod
    def setLevel(lev):
        GameObject.level=lev
    def draw(self, display):
        pass

    def update(self):
        pass