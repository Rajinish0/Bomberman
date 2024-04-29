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
        self.player1.placeBomb()
        bombPos = Point.int(self.player1.position)
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x],
            Bomb
        )
    
    def test_bomb_explode_and_kill(self):
        self.player1.placeBomb()
        bombPos = Point.int(self.player1.position)
        self.assertIsInstance(
            self.level.gameobjs[bombPos.y][bombPos.x],
            Bomb
        )
        self.level.gameobjs[bombPos.y][bombPos.x].explode()
        for i in range(5):
            self.level.gameobjs[bombPos.y][bombPos.x].update()
        
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

    
    def test_bigger_range(self):
        pass
        

    


if __name__ == '__main__':
    unittest.main()