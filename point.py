class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        return Point(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return Point(self.x - v.x, self.y - v.y)

    def mul(self, d):
        return Point(self.x * d, self.y * d)

    def div(self, d):
        return Point(self.x / d, self.y / d)