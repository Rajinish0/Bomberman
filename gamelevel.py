import random

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


def init(map_, bw, bh):

    reader = GridReader(map_)
    reader.read_grid()
    map_ = reader.get_grid()

    gameobjs = []
    players = []
    monsters = []
    default_direction=Point(0,1)

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
                    players.append(Player(game_elements.PLAYER1_NAME,p,0.05,os.path.join(IMG_PATH, 'players', 'g1.png'),keys["p1"],bw,bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.PLAYER2:
                    players.append(Player(game_elements.PLAYER2_NAME,p,0.05,os.path.join(IMG_PATH, 'players', 'g2.png'),keys["p2"],bw,bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.BASE_MONSTER:
                    monsters.append(Monster(p,0.038,os.path.join(IMG_PATH, 'monsters', 'm1b.png'),default_direction,bw,bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.GHOST_MONSTER:
                    monsters.append(
                        GhostMonster(p, 0.025, os.path.join(IMG_PATH, 'monsters', 'm1b.png'), default_direction, bw, bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.FAST_MONSTER:
                    monsters.append(
                        FastMonster(p, 0.05, os.path.join(IMG_PATH, 'monsters', 'm1b.png'), default_direction, bw, bh))
                    elem = EmptySpace(p, bw, bh)
                case game_elements.PSEUDOINTELLIGENT_MONSTER:
                    monsters.append(
                        PseudoIntelligentMonster(p, 0.05, os.path.join(IMG_PATH, 'monsters', 'm1b.png'), default_direction, bw, bh))
                    elem = EmptySpace(p, bw, bh)
                case _:
                    elem = EmptySpace(p, bw, bh);
            L.append(elem)
        gameobjs.append(L)
    return (gameobjs, players,monsters)

class GameLevel:
    def __init__(self,mp,boxwidth,boxheight):
        self.bw = boxwidth
        self.bh = boxheight
        GameObject.setLevel(self)


        self.gameobjs,self.players, self.monsters = init(mp,boxwidth,boxheight)
        if(len(self.monsters)==0):
            self.monsters=self.initMonster(2)

        self.winTimer=10
        self.endStart=False

        self.gameEnd=False
       # self.powUps=self.randomizePowerUps()
        self.bombs=[]
        self.player1Wins=0;
        self.player2Wins=0;
        self.randomizePowerUps()


    def update(self):
        if(not self.gameEnd):
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






    def draw(self, display):

        bombs = []

        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
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


    def initMonster(self,x):
        spots=[]
        monsters=[]
        for i in range(NUM_BOXES):
            for j in range(NUM_BOXES):
                if(isinstance(self.gameobjs[i][j],EmptySpace)):
                    spots.append((i,j))

        for pl in self.players:
            spots.remove((int(pl.position.y), int(pl.position.x)))


        final_spots=random.choices(spots,k=x)

        for f in final_spots:
            p=Point(f[1],f[0])
            monsters.append(
                GhostMonster(p, 0.025, os.path.join(IMG_PATH,'monsters' ,'m1b.png'),Point(0,1),self.bw,self.bh))

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

        self.endStart=False
        self.gameEnd=True


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













