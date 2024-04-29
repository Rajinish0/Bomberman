import unittest


from unittest import TestCase
from gamelevel import GameLevel
from gameObjects import Bomb
from point import Point
from mock import patch
from gameObjects.emptySpace import EmptySpace
from gameObjects.powerup import PowerUp
class TestFastMonster(unittest.TestCase):
    @patch('handlers.ImageHandler.load')
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def setUp(self, load, loadImageMock, transformScale):
        load.return_value = None
        loadImageMock.return_value = None
        transformScale.return_value = None
        self.level = GameLevel('tests/maps/fastmonster_map.txt', 40, 40)
        self.player1 = self.level.players[0]
        self.player2 = self.level.players[1]
        self.monster1=self.level.monsters[0]
        self.monster2=self.level.monsters[1]




    def test_monster1_position(self):

        self.assertEqual(
            self.monster1.position,Point(4.5,1.5)
        )
    def test_monster2_position(self):

        self.assertEqual(
            self.monster2.position, Point(8.5, 3.5)
        )

    def test_initial_direction_monster1(self):
        self.assertEqual(
            self.monster1.direction, Point(0,1)
        )

    def test_initial_direction_monster(self):
        self.assertEqual(
            self.monster2.direction, Point(0, 1)
        )

    def test_monster1_first_move(self):
        self.monster1.move(self.monster1.direction)
        self.assertEqual(
            self.monster1.position,Point(4.5,2.5)
        )

    def test_monster2_first_move(self):
        self.assertEqual(
            self.monster2.move(self.monster2.direction),False)
        self.monster2.direction=self.monster2.shortestPath()
        self.assertEqual(
            self.monster2.direction,Point(1,0)
        )
        self.monster2.move(self.monster2.direction)
        self.assertEqual(
            self.monster2.position,Point(9.5,3.5)
        )

    def test_monster1_hits_wall(self):
        self.monster1.position=Point(4.5,5.5)
        self.assertEqual(
            self.monster1.move(self.monster1.direction),False
        )
        self.monster1.direction=self.monster1.shortestPath()
        self.assertEqual(
            self.monster1.direction,Point(0,-1)
        )
        self.monster1.move(self.monster1.direction)
        self.assertEqual(
            self.monster1.position,Point(4.5,4.5)
        )

    def test_monster2_fork(self):
        self.monster2.position=Point(9.5,3.5)
        self.monster2.direction=self.monster2.shortestPath()
        self.assertEqual(
            self.monster2.direction,Point(1,0)
        )
        self.monster2.move(self.monster2.direction)

        self.assertEqual(
            self.monster2.position,Point(10.5,3.5)
        )
        directions=self.monster2.decisionList()
        self.assertEqual(
            self.monster2.isFork(directions),True
        )

    def test_monster1_kills_player(self):
        self.monster1.speed=1
        self.monster1.update()
        self.assertEqual(
            self.monster1.position,Point(4.5,2.5)
        )
        self.monster1.update()
        self.assertEqual(
            self.monster1.position, Point(4.5, 3.5)
        )
        self.monster1.direction=self.monster1.shortestPath()
        self.assertEqual(
            self.monster1.direction,Point(-1,0)
        )
        self.monster1.update()
        self.assertEqual(
            self.monster1.position, Point(3.5, 3.5)
        )
        self.monster1.update()
        self.assertEqual(
            self.monster1.position, Point(2.5, 3.5)
        )
        self.monster1.update()
        self.assertEqual(
            self.monster1.position, Point(1.5, 3.5)
        )
        self.assertEqual(
            self.player1.alive,False
        )
        self.assertEqual(
            self.player2.alive,True
        )
        self.assertEqual(
            self.monster1.shortestPath(),Point(0,0)
        )


    def test_monster2_kills_player(self):
        self.player2.position=Point(9.5,3.5)
        self.monster2.direction=self.monster2.shortestPath()
        self.monster2.move(self.monster2.direction)
        self.assertEqual(
            self.monster2.position, Point(9.5, 3.5)
        )
        self.monster2.speed=0.001
        self.monster2.update()
        self.assertEqual(
            self.player1.alive, True
        )
        self.assertEqual(
            self.player2.alive, False
        )
        self.assertEqual(
            self.monster2.shortestPath(), Point(0, 0)
        )

    def test_monster1_finds_player2(self):
        self.monster1.position=self.player1.position
        self.monster1.speed=0
        self.monster1.update()
        self.assertEqual(
            self.player1.alive,False
        )
        self.level.gameobjs[8][1].Destroy()
        self.assertIsInstance(
          self.level.gameobjs[8][1],(EmptySpace,PowerUp)
        )
        self.monster1.direction=self.monster1.shortestPath()
        self.assertEqual(
            self.monster1.direction,Point(0,1)
        )

    def test_monster2_finds_player1(self):
        self.monster2.position = self.player2.position
        self.monster2.speed = 0
        self.monster2.update()
        self.assertEqual(
            self.player2.alive, False
        )
        self.level.gameobjs[8][1].Destroy()

        self.assertIsInstance(
           self.level.gameobjs[8][1], (EmptySpace,PowerUp)
        )
        self.monster2.direction = self.monster2.shortestPath()
        self.assertEqual(
            self.monster2.direction, Point(-1, 0)
        )

    def test_bomb_kills_monster1(self):
        self.monster1.position=self.player1.position.add(Point(1,0))
        self.player1.placeBomb()
        self.level.gameobjs[int(self.player1.position.y)][int(self.player1.position.x)].explode()
        self.level.gameobjs[int(self.player1.position.y)][int(self.player1.position.x)].update()
        self.assertEqual(
            self.monster1.alive,False
        )
        self.assertEqual(
            self.player1.alive,False
        )

    def test_bomb_kills_monster2(self):
        self.monster2.position = self.player2.position.add(Point(0, -1))
        self.player2.placeBomb()
        self.level.gameobjs[int(self.player2.position.y)][int(self.player2.position.x)].explode()
        self.level.gameobjs[int(self.player2.position.y)][int(self.player2.position.x)].update()
        self.assertEqual(
            self.monster2.alive, False
        )
        self.assertEqual(
            self.player2.alive, False
        )











if __name__ == '__main__':
    unittest.main()
