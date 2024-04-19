import random, pygame

from .gameObject import GameObject
from point import Point
from .gamecharacter import GameCharacter
from .Player import Player
from .powerup import PowerUp
from .emptySpace import EmptySpace
from .bomb import Bomb
from .wall import BorderWall

class Monster(GameCharacter):
    def __init__(self,position,speed,image,direction,w,h):
        super().__init__(position,speed)
        self.image=self.imgHandler.load(image, (w,h))
        self.rw = .9999
        self.rh = .9999
        self.direction=direction
        self.alive=True
        self.t = 1


    def update(self):
        self.randomDecision()
        if(not self.move(self.direction*self.speed)):
            self.makeDecision()
        else:
            for pl in self.level.players:
                if Point.int(pl.position) == Point.int(self.position):
                    self.kill(pl)


    def isValid(self, coord):
        mvi, mvj = coord         
        return isinstance(self.level.gameobjs[mvi][mvj],(EmptySpace, PowerUp))

    '''
    READ Player.move, the same invariant is used here.
    '''

    def move(self,p):
        dp= p.add(self.position)

        if self.isValid( ( int(dp.y+self.rh/2), int(dp.x+self.rw/2) ) ) and\
           self.isValid( ( int(dp.y-self.rh/2), int(dp.x-self.rw/2) ) ) and\
           self.isValid( ( int(dp.y-self.rh/2), int(dp.x+self.rw/2) ) ) and\
           self.isValid( ( int(dp.y+self.rh/2), int(dp.x-self.rw/2) ) ):
           self.position = dp 
           return True 

        return False

    def makeDecision(self):
        directions=self.decisionList()
        self.direction=random.choice(directions)

    def decisionList(self):
        ls=[]
        i=int(self.position.y)
        j=int(self.position.x)
        if(isinstance(self.level.gameobjs[i+1][j],(EmptySpace,PowerUp))):
            ls.append(Point(0,1))
        if (isinstance(self.level.gameobjs[i -1][j], (EmptySpace, PowerUp))):
            ls.append(Point(0, -1))
        if (isinstance(self.level.gameobjs[i][j+1], (EmptySpace, PowerUp))):
            ls.append(Point(1, 0))
        if (isinstance(self.level.gameobjs[i ][j-1], (EmptySpace, PowerUp))):
            ls.append(Point(-1, 0))

        return ls

    def randomDecision(self):
        x=random.choice(range(0,10000))
        if(x>9990):
            self.makeDecision()

    # def draw(self, display):
    #     pygame.draw.rect(
    #         display, (0, 0, 121), ( (self.position.x-self.rw/2)*self.level.bw, (self.position.y-self.rh/2)*self.level.bh, self.rw*self.level.bw, self.rh*self.level.bh )
    #         )
    #     super().draw(display)


    def kill(self,player):
        player.Destroy()

    def Destroy(self):
        self.level.monsters.remove(self)
        self.alive=False


class GhostMonster(Monster):

    def isValid(self, coord):
        mvi, mvj = coord
        if mvi<1 or mvj<1 or mvi>len(self.level.gameobjs)-2 or mvj>len(self.level.gameobjs[0])-2:
            return False
        return not isinstance(self.level.gameobjs[mvi][mvj], Bomb)

    def decisionList(self):
        ls=[]
        i=int(self.position.y)
        j=int(self.position.x)
        if(not isinstance(self.level.gameobjs[i+1][j],BorderWall)):
            ls.append(Point(0,1))
        if (not isinstance(self.level.gameobjs[i -1][j], BorderWall)):
            ls.append(Point(0, -1))
        if (not isinstance(self.level.gameobjs[i][j+1], BorderWall)):
            ls.append(Point(1, 0))
        if (not isinstance(self.level.gameobjs[i ][j-1], BorderWall)):
            ls.append(Point(-1, 0))

        return ls

class FastMonster(Monster):

    def randomDecision(self):
        pass
    def makeDecision(self):
        directions=self.decisionList()
        if(len(directions)==1):
            self.direction=directions[0]
        else:
            self.direction=self.shortestPath()

        if(self.direction==Point(0,0)):
            super().makeDecision()
    def shortestPath(self):
        p=Point.int(self.position)
        queue=[]
        visited_nodes={}
        visited_nodes[p] = Point(0, 0)
        if isinstance(self.level.gameobjs[p.y+1][p.x],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(0,1)
            visited_nodes[p.add(Point(0, 1))] = Point(0, 1)
            queue.append(p.add(Point(0, 1)))
        if isinstance(self.level.gameobjs[p.y-1][p.x],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(0,-1)
            visited_nodes[p.add(Point(0, -1))] = Point(0, -1)
            queue.append(p.add(Point(0, -1)))
        if isinstance(self.level.gameobjs[p.y][p.x+1],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(1,0)
            visited_nodes[p.add(Point(1, 0))] = Point(1, 0)
            queue.append(p.add(Point(1, 0)))
        if isinstance(self.level.gameobjs[p.y][p.x-1],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(-1, 0)
            visited_nodes[p.add(Point(-1, 0))] = Point(-1, 0)
            queue.append(p.add(Point(-1, 0)))

        while len(queue)>0:
            temp=queue.pop(0)
            for pl in self.level.players:
                if Point.int(pl.position) == temp:
                    return visited_nodes.get(temp)

            i=temp.y
            j=temp.x

            if not visited_nodes.get(temp.add(Point(0,1))):

                for pl in self.level.players:
                    if Point.int(pl.position)==temp.add(Point(0,1)):
                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i+1][j],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point(0, 1))] = visited_nodes[temp]
                    queue.append(temp.add(Point(0, 1)))

            if not visited_nodes.get(temp.add(Point(0,-1))):

                for pl in self.level.players:
                    if Point.int(pl.position)==temp.add(Point(0,-1)):
                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i-1][j],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point(0, -1))] = visited_nodes[temp]
                    queue.append(temp.add(Point(0,-1)))

            if not visited_nodes.get(temp.add(Point(1,0))):


                for pl in self.level.players:


                    if Point.int(pl.position)==temp.add(Point(1,0)):

                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i][j+1],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point(1, 0))] = visited_nodes[temp]
                    queue.append(temp.add(Point(1, 0)))

            if not visited_nodes.get(temp.add(Point(-1,0))):
                for pl in self.level.players:
                    if Point.int(pl.position)==temp.add(Point(-1,0)):
                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i][j-1],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point( -1,0))] = visited_nodes[temp]
                    queue.append(temp.add(Point(-1,0)))





        return Point(0,0)

class PseudoIntelligentMonster(Monster):
    def randomDecision(self):
        x=round(self.position.x,2)
        y=round(self.position.y,2)
        if(str(x).endswith(".5") and str(y).endswith(".5")):
            directions = self.decisionList()

            if(self.isFork(directions)):
                d=self.shortestPath()
                if(d!=Point(0,0)):
                    self.direction=self.shortestPath()
                x= random.choice(range(0, 100))
                if(x>90):
                    directions=[d for d in directions if d!=self.direction]
                    self.direction=random.choice(directions)


    def isFork(self,points):
        x=0
        y=0
        for p in points:
            if p.x!=0:
                x=p.x
            if p.y!=0:
                y=p.y

        return x!=0 and y!=0






    def shortestPath(self):
        p=Point.int(self.position)
        queue=[]
        visited_nodes={}
        visited_nodes[p] = Point(0, 0)
        if isinstance(self.level.gameobjs[p.y+1][p.x],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(0,1)
            visited_nodes[p.add(Point(0, 1))] = Point(0, 1)
            queue.append(p.add(Point(0, 1)))
        if isinstance(self.level.gameobjs[p.y-1][p.x],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(0,-1)
            visited_nodes[p.add(Point(0, -1))] = Point(0, -1)
            queue.append(p.add(Point(0, -1)))
        if isinstance(self.level.gameobjs[p.y][p.x+1],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(1,0)
            visited_nodes[p.add(Point(1, 0))] = Point(1, 0)
            queue.append(p.add(Point(1, 0)))
        if isinstance(self.level.gameobjs[p.y][p.x-1],(EmptySpace,PowerUp)):
            for pl in self.level.players:
                if Point.int(pl.position) == p.add(Point(0, 1)):
                    return Point(-1, 0)
            visited_nodes[p.add(Point(-1, 0))] = Point(-1, 0)
            queue.append(p.add(Point(-1, 0)))

        while len(queue)>0:
            temp=queue.pop(0)
            for pl in self.level.players:
                if Point.int(pl.position) == temp:
                    return visited_nodes.get(temp)

            i=temp.y
            j=temp.x

            if not visited_nodes.get(temp.add(Point(0,1))):

                for pl in self.level.players:
                    if Point.int(pl.position)==temp.add(Point(0,1)):
                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i+1][j],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point(0, 1))] = visited_nodes[temp]
                    queue.append(temp.add(Point(0, 1)))

            if not visited_nodes.get(temp.add(Point(0,-1))):

                for pl in self.level.players:
                    if Point.int(pl.position)==temp.add(Point(0,-1)):
                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i-1][j],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point(0, -1))] = visited_nodes[temp]
                    queue.append(temp.add(Point(0,-1)))

            if not visited_nodes.get(temp.add(Point(1,0))):


                for pl in self.level.players:


                    if Point.int(pl.position)==temp.add(Point(1,0)):

                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i][j+1],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point(1, 0))] = visited_nodes[temp]
                    queue.append(temp.add(Point(1, 0)))

            if not visited_nodes.get(temp.add(Point(-1,0))):
                for pl in self.level.players:
                    if Point.int(pl.position)==temp.add(Point(-1,0)):
                        return visited_nodes.get(temp)
                if isinstance(self.level.gameobjs[i][j-1],(EmptySpace,PowerUp)):
                    visited_nodes[temp.add(Point( -1,0))] = visited_nodes[temp]
                    queue.append(temp.add(Point(-1,0)))





        return Point(0,0)