import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        return Point(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return Point(self.x - v.x, self.y - v.y)

    def mul(self, d):
        if isinstance(d, Point):
            return Point(self.x * d.x, self.y * d.y)
        return Point(self.x * d, self.y * d)

    def div(self, d):
        return Point(self.x / d, self.y / d)

    def __lmul__(self, d):
        if isinstance(d, Point):
            return Point(self.x * d.x, self.y * d.y)
        return Point(self.x * d, self.y *d)
    __mul__ = __lmul__

    def __sub__(self, p):
        return Point(self.x-p.x, self.y-p.y)

    def norm(self, squared=True):
        n = self.x*self.x + self.y*self.y
        if squared: 
            return n
        return math.sqrt(n)

    def __eq__(self, other):
        return (self.x == other.x and 
                self.y == other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))
    @classmethod
    def int(cls, point):
        return cls( int(point.x), int(point.y) )


