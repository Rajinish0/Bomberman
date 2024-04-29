import unittest
from unittest import TestCase
from gamelevel import GameLevel
from gameObjects import Bomb
from point import Point
from mock import patch

class MyTestCase(unittest.TestCase):
    @patch('handlers.ImageHandler.load')
    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def setUp(self, load, loadImageMock, transformScale):
        load.return_value = None
        loadImageMock.return_value = None
        transformScale.return_value = None
        self.level = GameLevel('tests/maps/custom_map_gm.txt', 40, 40)
        self.player1 = self.level.players[0]
        self.player2 = self.level.players[1]
        self.monster = self.level.monsters[0]

    def test_monster_position(self):
        self.assertEqual(self.monster.position, Point(13.5, 3.5))

    def test_monster_move_wall(self):
        self.monster.move(Point(1, 0))
        self.assertEqual(self.monster.position, Point(13.5, 3.5))

    def test_monster_move_box(self):
        self.monster.move(Point(0, 1))
        self.assertEqual(self.monster.position, Point(13.5, 4.5))

    def test_monster_kill(self):
        self.monster.move(Point(-6, 0))
        self.monster.update()
        self.assertEqual(self.player1.alive, False)

    def test_monster_destroy(self):
        self.monster.move(Point())

if __name__ == '__main__':
    unittest.main()
