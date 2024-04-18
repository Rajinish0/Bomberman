from point import Point
from handlers import ImageHandler

class GameObject:
    imgHandler=ImageHandler()
    image = None
    level = None
    def __init__(self, position, width, height):
        self.position = position # Point
        self.w = width
        self.h = height

    @staticmethod
    def setLevel(lev):
        GameObject.level=lev


    def draw(self, display):
        display.blit(self.image, (self.position.x*self.w,
                                  self.position.y*self.h)) 

    def update(self):
        pass

    def Destroy(self):
        pass
