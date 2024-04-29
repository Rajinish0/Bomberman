import unittest
from unittest import TestCase
from gamelevel import GameLevel
from gameObjects import Bomb, EmptySpace, Box, PowerUp
from point import Point
from mock import patch
from handlers import ImageHandler
import pygame

class TestBomb(TestCase):
    @patch('handlers.ImageHandler.load')
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')

    def setUp(self, load, loadImageMock, transformScale):
        load.return_value = None
        loadImageMock.return_value = None
        transformScale.return_value = None
        
        self.level = GameLevel('tests/maps/custom_map2.txt', 40, 40)
        self.player1 = self.level.players[0]
        self.player2 = self.level.players[1]
    
    def test_player1_position(self):
        self.assertEqual(
            self.player1.position,
            Point(1.5, 1.5)
        )
    
    def test_player2_position(self):
        self.assertEqual(
            self.player2.position,
            Point(3.5, 7.5)
        )
    
    def test_bomb_plant(self):
        #when
        self.player1.placeBomb()
        bombPos = Point.int(self.player1.position)
        #then
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x],
            Bomb
        )
    
    def test_bomb_explode_and_kill(self):
        #when
        self.player1.placeBomb()
        bombPos = Point.int(self.player1.position)
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x],
            Bomb
        )
        self.level.gameobjs[bombPos.y][bombPos.x].explode()
        for _ in range(5):
            self.level.gameobjs[bombPos.y][bombPos.x].update()
        
        #then
        self.assertEqual(
            self.player1.alive,
            False
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x+1],
            (EmptySpace, PowerUp)
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x+1],
            (EmptySpace, PowerUp)
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y+1][bombPos.x],
            (EmptySpace, PowerUp)
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y+1][bombPos.x+1],
            Box
        )

    
    def test_bigger_range_is_blocked_by_boxes(self):
        # given
        self.player2.incBombRange()
        self.player2.placeBomb()
        bombPos = Point.int(self.player2.position)
        bomb = self.level.gameobjs[bombPos.y][bombPos.x]

        # when
        bomb.explode()
        for _ in range(500):
            bomb.update()
        
        # then
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y+1][bombPos.x],
            (EmptySpace, PowerUp)
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y-1][bombPos.x],
            (EmptySpace, PowerUp)
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x+1],
            (EmptySpace, PowerUp)
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x-1],
            (EmptySpace, PowerUp)
        )
        
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x-2],
            Box
        )

        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x+2],
            Box
        )

        self.assertEqual(
            bomb.incUp,
            1
        )

        self.assertEqual(
            bomb.incDown,
            1
        )

        self.assertEqual(
            bomb.incRight,
            1
        )

        self.assertEqual(
            bomb.incLeft,
            1
        )
    
    def test_bigger_range_is_not_blocked(self):
        # given
        self.player2.position = self.player2.position.add(Point(3, 0))
        self.assertEqual(
            self.player2.position,
            Point(6.5, 7.5)
        )
        self.player2.incBombRange()

        # when
        self.player2.placeBomb()
        bombPos = Point.int(self.player2.position)
        bomb = self.level.gameobjs[bombPos.y][bombPos.x]
        bomb.explode()
        for _ in range(500):
            bomb.update()
        
        # then
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x-1],
            (EmptySpace, PowerUp)
        )

        self.assertEqual(
            bomb.incRight,
            2
        )

        self.assertEqual(
            bomb.incLeft,
            1
        )

        self.assertEqual(
            bomb.incUp,
            2
        )

        self.assertEqual(
            bomb.incDown,
            2
        )
    
    def test_bomb_kills_all_monsters(self):
        #given
        self.player2.position = self.player2.position.add(Point(4, 0))
        self.assertEqual(
            self.player2.position,
            Point(7.5, 7.5)
        )
        monsters = self.level.monsters[:]

        #when
        self.player2.placeBomb()
        bombPos = Point.int(self.player2.position)
        bomb = self.level.gameobjs[bombPos.y][bombPos.x]
        bomb.explode()
        for _ in range(500):
            bomb.update()

        #then
        self.assertEqual(
            self.level.monsters,
            []
        )

        for monster in monsters:
            self.assertEqual(
                monster.alive,
                False
            )




if __name__ == '__main__':
    unittest.main()