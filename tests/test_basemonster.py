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
        self.level = GameLevel('tests/maps/custom_map_bm.txt', 40, 40)
        self.player1 = self.level.players[0]
        self.player2 = self.level.players[1]
        self.monster = self.level.monsters[0]

    def test_monster_position(self):
        self.assertEqual(
            self.monster.position, Point(13.5, 3.5)
        )

    # Test monster moving
    def test_monster_position_wall(self):
        self.monster.move(Point(1, 0))
        self.assertEqual(
            self.monster.position, Point(13.5, 3.5)
        )

    def test_monster_position_box(self):
        self.monster.move(Point(0, 1))
        self.assertEqual(
            self.monster.position, Point(13.5, 3.5)
        )

    def test_monster_position_success(self):
        self.monster.move(Point(0, -1))
        self.assertEqual(
            self.monster.position, Point(13.5, 2.5)
        )

    # Test monster killing player
    def test_monster_kill(self):
        self.assertEqual(self.monster.position, Point(13.5, 3.5))
        self.monster.move(Point(-12, -2))
        self.monster.update()
        self.assertEqual(self.player1.alive, False)


    # Test monster being killed by bomb
    def test_monster_destroy(self):
        self.assertEqual(self.monster.position, Point(13.5, 3.5))
        self.assertEqual(self.player2.position, Point(3.5, 7.5))
        self.monster.move(Point(-10, 4))
        # self.assertEqual(self.monster.position, Point(3.5, 7.5))
        self.player2.placeBomb()
        self.bombPos = Point.int(self.player2.position)
        self.level.gameobjs[self.bombPos.y][self.bombPos.x].explode()
        self.level.gameobjs[self.bombPos.y][self.bombPos.x].update()
        self.assertEqual(self.monster.alive, False)


if __name__ == '__main__':
    unittest.main()
