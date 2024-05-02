import unittest
from unittest import TestCase
from gamelevel import GameLevel, loadKeys
from gameObjects import Bomb
from gameObjects.powerup import BombNumPowerUp, RangePowerUp
from point import Point
from mock import patch
class TestPlayer(TestCase):
    @patch('handlers.ImageHandler.load')
    def setUp(self,load):
        load.return_value = None
        playersKeys = loadKeys()
        keyPressedDict = {key:False for key in playersKeys['p1'].values()}
        keyPressedDict.update({key:False for key in playersKeys['p2'].values()})

        self.keyPressedPatch = patch('pygame.key.get_pressed', return_value=keyPressedDict)
        self.keyPressedMock = self.keyPressedPatch.start()

        self.imageLoadPatch = patch('pygame.image.load', return_value=None)
        self.imageLoadMock  = self.imageLoadPatch.start()

        self.transformScalePatch = patch('pygame.transform.scale', return_value=None)
        self.transformScaleMock = self.transformScalePatch.start()

        self.level = GameLevel('tests/maps/custom_map_gl.txt', 40, 40)
        self.player1 = self.level.players[0]
        self.player2 = self.level.players[1]
    
    def tearDown(self) -> None:
        self.keyPressedPatch.stop()
        self.imageLoadPatch.stop()
        self.transformScalePatch.stop()
    
    def test_player1_position(self):
        self.assertEqual(
            self.player1.position, Point(1.5, 1.5)
        )
    
    def test_player2_position(self):
        self.assertEqual(
            self.player2.position, Point(3.5, 7.5)
        )
    
    def test_player_dead_ends_game(self):
        self.level.monsters[0].move(Point(-1, 0))

        self.level.update()

        self.assertEqual(
            self.player1.alive,
            False
        )

        self.level.monsters[0].Destroy()

        for i in range(101):
            self.level.update()
        
        self.assertEqual(
            self.level.gameEnd,
            True
        )

        self.assertEqual(
            self.level.player2Wins,
            1
        )
    
    def test_battle_royal_kills_player_and_game_ends(self):
        '''
        701 --> 120/0.2 = 600 + 50(enough time for wall to build up) 
            --> BR_TIMER/BR_TIMER_DELTA + ENOUGH_TIME (if constants are defined)
        '''
        self.level.monsters[0].Destroy()
        for _ in range(650):
            self.level.update()
        
        self.assertEqual(
            self.player1.alive,
            False
        )

        for _ in range(101):
            self.level.update()
        
        self.assertEqual(
            self.level.gameEnd,
            True
        )

        self.assertEqual(
            self.level.player2Wins,
            1
        )
    
    def test_max_win_round_ends_game(self):
        '''
        Should be done:
        change these values in gamelevel. These should be defined as global constants.
        how is 101 calculated? Level subtracts 0.1 from winTimer per frame and total winTimer is 10
        so after 100 updates winterTimer will be 10 and at the 101th update it's certain the other player would have won

        if constants are defined:
        101 --> ceil(WIN_TIMER/WIN_TIMER_DELTA) + 1
        for i in range(2) --> for i in range(MAX_WINS)
        if i < 1 --> if i < MAX_WINS - 1 
        '''
        for i in range(2):
            self.level.monsters[0].move(Point(-1, 0))
            self.level.update()

            self.assertEqual(
                self.player1.alive,
                False
            )

            for _ in range(101):
                self.level.update()
            
            self.assertEqual(
                self.level.gameEnd,
                True
            )

            self.assertEqual(
                self.level.player2Wins,
                i+1
            )

            if i < 1:
                self.level.nextRound()
                self.player1 = self.level.players[0]
                self.player2 = self.level.players[1]

        self.assertEqual(
            self.level.finished,
            True
        )

        


if __name__ == '__main__':
    unittest.main()