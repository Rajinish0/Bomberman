import math
import random

import time
from constants import game_elements
from constants.game_constants import *
from gameObjects import *
from fileReading import GridReader

import pygame, pickle, os
from point import Point

def loadKeys():
    with open(os.path.join(RSRC_PATH, 'keycfg.pkl'), 'rb') as f:
        keys = pickle.load(f)
    return keys

def loadData():
    with open(os.path.join(RSRC_PATH, 'datacfg.pkl'), 'rb') as f:
        data=pickle.load(f)
    return data

def init(map_, bw, bh):

    reader = GridReader(map_)
    reader.read_grid()
    map_ = reader.get_grid()

    gameobjs = []
    players = []
    monsters = []
    default_direction=Point(0, 1)

    keys = loadKeys()
    for i in range(NUM_BOXES):
        L = []
        for j in range(NUM_BOXES):
            elem = None
            p=Point(j,i)
            match map_[i][j]:
                case game_elements.BOX:
                    elem = Box(p, bw, bh);
                case game_elements.WALL:
                    elem = Wall(p, bw, bh);
                case game_elements.BORDER_WALL:
                    elem = BorderWall(p, bw, bh);
                case game_elements.PLAYER1:
                    players.append(Player(game_elements.PLAYER1_NAME,p,0.075,os.path.join(IMG_PATH, 'players', 'bomber-sprite2.png'),keys["p1"],bw,bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.PLAYER2:
                    players.append(Player(game_elements.PLAYER2_NAME,p,0.075,os.path.join(IMG_PATH, 'players', 'bomber-sprite.png'),keys["p2"],bw,bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.BASE_MONSTER:
                    monsters.append(Monster(p,0.05,os.path.join(IMG_PATH, 'monsters', 'm1b.png'),default_direction,bw,bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.GHOST_MONSTER:
                    monsters.append(
                        GhostMonster(p, 0.025, os.path.join(IMG_PATH, 'monsters', 'm2.png'), default_direction, bw, bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.FAST_MONSTER:
                    monsters.append(
                        FastMonster(p, 0.066, os.path.join(IMG_PATH, 'monsters', 'm3.png'), default_direction, bw, bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.PSEUDOINTELLIGENT_MONSTER:
                    monsters.append(

                        PseudoIntelligentMonster(p, 0.05, os.path.join(IMG_PATH, 'monsters', 'm4.png'), default_direction, bw, bh))

                    elem = EmptySpace(p, bw, bh)
                case _:
                    elem = EmptySpace(p, bw, bh);
            L.append(elem)
        gameobjs.append(L)
    return (gameobjs, players,monsters)

class GameLevel:
    def __init__(self,mp,boxwidth,boxheight):
        self.mp=mp
        self.bw = boxwidth
        self.bh = boxheight
        GameObject.setLevel(self)
        self.phase = 0
        self.data=loadData()
        self.emptyImage = pygame.image.load(EmptySpace.image)
        self.emptyImage = pygame.transform.scale(self.emptyImage, (boxwidth, boxheight))

        self.gameobjs,self.players, self.monsters = init(mp,boxwidth,boxheight)

        self.pl1Name=self.data["p1"]
        self.pl2Name=self.data["p2"]
        self.brTimer = self.data["timer"]
        self.numRounds=self.data["round"]
        self.players[0].name=self.pl1Name
        self.players[1].name=self.pl2Name

        if(len(self.monsters)==0):
            self.monsters=self.initMonster()

        self.winTimer=10
        self.endStart=False

        self.gameEnd=False
       # self.powUps=self.randomizePowerUps()
        self.bombs=[]
        self.player1Wins=0;
        self.player2Wins=0;
        self.randomizePowerUps()
        self.finished=False

        self.brAnimationFinished=False

        self.start = 1
        self.end = 14
        self.row = 1
        self.col = 1
        self.count = 0
        self.switch = 1

        #self.battleTimer = 10

    def battleRoyal(self, row, col):
        margin = 0.1
        for player in self.players:
            # player_x = int(player.position.x)
            # player_y = int(player.position.y)
            if (Point.int(player.position) == Point(col, row)):
            # if (player_x - margin <= col <= player_x + 1 + margin or
                # player_x + 1 - margin <= col + 1 <= player_x + 1 + margin) and \
                    # (player_y - margin <= row <= player_y + 1 + margin or
                     # player_y + 1 - margin <= row + 1 <= player_y + 1 + margin):
                player.Destroy()
            else:
                if Point.int(Point(player.position.x - player.rw/2,
                             player.position.y)) == Point(col, row):
                    player.position = Point(col + 1, row).add(Point(0.5, 0.5))
                elif Point.int(Point(player.position.x + player.rw/2,
                             player.position.y)) == Point(col, row):
                    player.position = Point(col - 1, row).add(Point(0.5, 0.5))
                elif Point.int(Point(player.position.x,
                             player.position.y + player.rh/2)) == Point(col, row):
                    player.position = Point(col, row - 1).add(Point(0.5, 0.5))
                elif Point.int(Point(player.position.x,
                             player.position.y - player.rh/2)) == Point(col, row):
                    player.position = Point(col, row + 1).add(Point(0.5, 0.5))


        for monster in self.monsters:
            if (Point.int(monster.position) == Point(col, row)):
                monster.Destroy()
            else:
                if Point.int(Point(monster.position.x - monster.rw/2,
                             monster.position.y)) == Point(col, row):
                    monster.position = Point(col + 1, row).add(Point(0.5, 0.5))
                elif Point.int(Point(monster.position.x + monster.rw/2,
                             monster.position.y)) == Point(col, row):
                    monster.position = Point(col - 1, row).add(Point(0.5, 0.5))
                elif Point.int(Point(monster.position.x,
                             monster.position.y + monster.rh/2)) == Point(col, row):
                    monster.position = Point(col, row - 1).add(Point(0.5, 0.5))
                elif Point.int(Point(monster.position.x,
                             monster.position.y - monster.rh/2)) == Point(col, row):
                    monster.position = Point(col, row + 1).add(Point(0.5, 0.5))
            # monster_x = math.floor(monster.position.x)
            # monster_y = math.floor(monster.position.y)
            # if (monster_x - margin <= col <= monster_x + 1 + margin or
            #     monster_x + 1 - margin <= col + 1 <= monster_x + 1 + margin) and \
            #         (monster_y - margin <= row <= monster_y + 1 + margin or
            #          monster_y + 1 - margin <= row + 1 <= monster_y + 1 + margin):
                # monster.Destroy()

        self.gameobjs[row][col] = BorderWall(Point(col, row), self.bw, self.bh)

    def update(self):
        if(not self.gameEnd):
            if self.brTimer <= 0:
                if self.count == 15:
                    if self.switch == 1:
                        self.battleRoyal(self.row, self.col)
                        self.col += 1
                        if self.col == self.end+1:
                            self.col = self.end-1
                            self.switch = 2

                    elif self.switch == 2:
                        self.battleRoyal(self.row, self.col)
                        self.row += 1
                        if self.row == self.end + 1:
                            self.row = self.end - 1
                            self.switch = 3

                    elif self.switch == 3:
                        self.battleRoyal(self.row, self.col)
                        self.col -= 1
                        if self.col == self.start-1:
                            self.col = self.start
                            self.switch = 4

                    elif self.switch == 4:
                        self.battleRoyal(self.row, self.col)
                        self.row -= 1
                        if self.row == self.start - 1:
                            self.start += 1
                            self.end -= 1
                            self.row = self.start
                            self.row = self.start
                            self.switch = 1
                            self.brAnimationFinished = True
                    self.count = 0
                self.count += 1
                #self.battleTimer -= 0.016666

                #Insert Animation Logic : Returns self.brAnimationFinished=True

                if self.brAnimationFinished:
                    self.brTimer = self.data["timer"]
                    #self.battleTimer=10
                    self.brAnimationFinished=False

            self.brTimer-=0.016666
            #self.brTimer -= 0.2


            for i in range(NUM_BOXES):
                for j in range(NUM_BOXES):
                    self.gameobjs[i][j].update()
            # self.collisions()
            # self.bombExplosion()

            for player in self.players:
                player.update()

            for monster in self.monsters:
                monster.update()

            if(self.endStart):
                if(self.winTimer<=0):

                    if(self.players[0].name=="Aunt May"):
                        self.player1Wins+=1

                    else:
                        self.player2Wins+=1
                    self.isOver()
                else:
                    if(len(self.players)>0):
                        self.winTimer-=0.1
                    else:
                        self.isOver()

    def draw(self, display):

        bombs = []

        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                # pos = self.gameobjs[i][j].position
                display.blit(self.emptyImage, (j * self.bw, i * self.bh))
                if not isinstance(self.gameobjs[i][j], Bomb):
                # pygame.draw.rect(display, (255, 0, 0), (j * self.bw, i * self.bh, self.bw, self.bh), 1)
                    self.gameobjs[i][j].draw(display)
                else:
                    bombs.append((i, j))

        for i, j in bombs:
            self.gameobjs[i][j].draw(display)

        for player in self.players:
            player.draw(display)

        for monster in self.monsters:
            monster.draw(display)


    def nextRound(self):
        self.gameobjs, self.players, self.monsters = init(self.mp, self.bw, self.bh)
        self.players[0].name = self.pl1Name
        self.players[1].name = self.pl2Name
        if (len(self.monsters) == 0):
            self.monsters = self.initMonster()

        self.winTimer = 10
        self.endStart = False

        self.gameEnd = False
        # self.powUps=self.randomizePowerUps()
        self.bombs = []
        self.randomizePowerUps()

    def restart(self):
        self.__init__(self.mp,self.bw,self.bh)
    def initMonster(self):
        spots=[]
        monsters=[]
        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                if(isinstance(self.gameobjs[i][j],EmptySpace)):
                    spots.append((i,j))

        for pl in self.players:
            spots.remove((int(pl.position.y), int(pl.position.x)))


        f=random.choices(spots,k=4)
        monsters.append(Monster(Point(f[0][1],f[0][0]),0.05, os.path.join(IMG_PATH,'monsters' ,'m1b.png'),Point(0,1),self.bw,self.bh))
        monsters.append(GhostMonster(Point(f[1][1],f[1][0]),0.025, os.path.join(IMG_PATH,'monsters' ,'m2.png'),Point(0,1),self.bw,self.bh))
        monsters.append(FastMonster(Point(f[2][1],f[2][0]),0.066, os.path.join(IMG_PATH,'monsters' ,'m3.png'),Point(0,1),self.bw,self.bh))
        monsters.append(PseudoIntelligentMonster(Point(f[3][1],f[3][0]),0.05, os.path.join(IMG_PATH,'monsters' ,'m4.png'),Point(0,1),self.bw,self.bh))




        return monsters

    def randomizePowerUps(self):
        spots = []
        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                if (isinstance(self.gameobjs[i][j], Box)):
                    spots.append((i, j))

        powups=random.choices(spots,k=(len(spots)//5))
        for pow in powups:
            self.gameobjs[pow[0]][pow[1]].generatePowerUp()

        return powups

    def isOver(self):
        self.start = 1
        self.end = 14
        self.row = 1
        self.col = 1
        self.count = 0
        self.switch = 1
        self.endStart=False
        self.gameEnd=True
        self.finished = self.player1Wins == self.numRounds or self.player2Wins == self.numRounds
        self.brTimer = self.data["timer"]
        self.brAnimationFinished=False

    def startEnd(self,pl):
        self.players.remove(pl)
        self.endStart=True
        if(len(self.players)==0):
            self.gameEnd=True


        # def unpredictableMonster(self,monster):
    #     rand_num=random.randint(0,100)
    #     if(rand_num>90):
    #         monster.makeDecision()


    # def collisions(self):
    #     for mon in self.monsters:
    #         if (not isinstance(self.gameobjs[mon.x][mon.y], EmptySpace)):
    #             mon.makeDecision()
    #         else:
    #             self.unpredictableMonster(mon)
    #
    #         for pl in self.players:
    #             if(int(mon.x)==int(pl.x) and int(mon.y)==int(pl.y)):
    #                 mon.kill(pl)
    #                 self.players.remove(pl)

    # def bombExplosion(self):
    #     for bomb in self.bombs:
    #         if(bomb.isExploded):
    #             for i in range(bomb.x-bomb.range,bomb.x+bomb.range):
    #                 if(isinstance(self.gameobjs[i][bomb.y],Box)):
    #                     if((i,bomb.y,1) in self.powUps):
    #                         self.gameobjs[i][bomb.y]=BombNumPowerUp(bomb.y * bw, i * bh, bw, bh)
    #                     if ((i, bomb.y, 2) in self.powUps):
    #                         self.gameobjs[i][bomb.y] = RangePowerUp(bomb.y * bw, i * bh, bw, bh)
    #
    #                 for pl in self.players:
    #                     if (int(i) == int(pl.x) and int(bomb.y) == int(pl.y)):
    #                         pl.Destroy()
    #                         self.players.remove(pl)
    #
    #                 for mon in self.monsters:
    #                     if (int(i) == int(mon.x) and int(bomb.y) == int(mon.y)):
    #                         mon.Destroy()
    #                         self.monsters.remove(mon)
    #
    #             for i in range(bomb.y - bomb.range, bomb.y + bomb.range):
    #                 if (isinstance(self.gameobjs[bomb.x][i], Box)):
    #                     if ((bomb.x, i, 1) in self.powUps):
    #                         self.gameobjs[bomb.x][i] = BombNumPowerUp(i * bw, bomb.x * bh, bw, bh)
    #                     if ((bomb.x,i, 2) in self.powUps):
    #                         self.gameobjs[bomb.x][i] = RangePowerUp(i * bw, bomb.x * bh, bw, bh)
    #
    #                 for pl in self.players:
    #                     if (int(bomb.x) == int(pl.x) and int(i) == int(pl.y)):
    #                         pl.Destroy()
    #                         self.players.remove(pl)
    #
    #                 for mon in self.monsters:
    #                     if (int(bomb.x) == int(mon.x) and int(i) == int(mon.y)):
    #                         mon.Destroy()
    #                         self.monsters.remove(mon)
    #
    #         bomb.Destroy()
    #         self.bombs.remove(bomb)













