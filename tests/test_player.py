import unittest
from unittest import TestCase
from gamelevel import GameLevel
from gameObjects import Bomb
from point import Point
from mock import patch
from handlers import ImageHandler
class TestPlayer(TestCase):
    @patch('handlers.ImageHandler.load')
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def setUp(self,load,loadImageMock, transformScale):
        load.return_value = None
        loadImageMock.return_value = None
        transformScale.return_value = None
        self.level = GameLevel('tests/maps/custom_map.txt', 40, 40)
        self.player1 = self.level.players[0]
        self.player2 = self.level.players[1]
    
    def test_player1_position(self):
        self.assertEqual(
            self.player1.position, Point(1.5, 1.5)
        )
    
    def test_player2_position(self):
        self.assertEqual(
            self.player2.position, Point(3.5, 7.5)
        )
    
    def test_player1_move_fail(self):
        self.player1.move(Point(0, -1))
        self.assertEqual(
            self.player1.position, Point(1.5, 1.5)
        )
    
    def test_player1_move_success(self):
        self.player1.move(Point(1, 0))
        self.assertEqual(
            self.player1.position, Point(2.5, 1.5)
        )
    
    def test_player_to_player_collision(self):
        self.player1.position = Point(1.5, 1.5)
        self.player2.position = Point(2.5, 1.5)
        self.player1.move(Point(1, 0))
        self.assertEqual(
            self.player1.position, Point(1.5, 1.5)
        )
        self.assertEqual(
            self.player2.position, Point(2.5, 1.5)
        )
    
    def test_continuous_movement(self):
        self.player1.move(Point(1, 0)*0.3)
        self.assertEqual(
            self.player1.position, 
            Point(1.8, 1.5)
        )
    
    def test_plant_bomb(self):
        self.player1.placeBomb()
        self.bombPos = Point.int(self.player1.position)
        self.assertIsInstance(
            self.level.gameobjs[self.bombPos.y][self.bombPos.x] ,            
            Bomb
        )
    
    def test_bomb_explode_kills(self):
        self.player1.placeBomb()
        self.bombPos = Point.int(self.player1.position)
        self.level.gameobjs[self.bombPos.y][self.bombPos.x].explode()
        self.level.gameobjs[self.bombPos.y][self.bombPos.x].update()
        self.assertEqual(
            self.player1.alive,
            False
        )
    


if __name__ == '__main__':
    unittest.main()