import unittest

import Reversi


class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Reversi.Board()

    def tearDown(self):
        del self.board

    def test_reset_board(self):
        new_board = Reversi.Board()
        new_board.board[2][3] = 'WHITE_TILE'
        new_board.board[2][2] = 'BLACK_TILE'
        new_board.reset_board()

        self.assertEqual(self.board.board, new_board.board)


class PlayerMoveTest(unittest.TestCase):

    def setUp(self):
        self.board = Reversi.Board()
        self.player_one = Reversi.PlayerMove('BLACK_TILE', self.board)
        self.player_two = Reversi.PlayerMove('WHITE_TILE', self.board)

    def tearDown(self):
        del self.player_one
        del self.board

    def test_is_valid_move(self):
        self.assertFalse(self.player_two.is_valid_move(8, 8))
        self.assertFalse(self.player_one.is_valid_move(3, 4))
        self.assertTrue(self.player_two.is_valid_move(4, 2))

    def test_valid_move(self):
        self.board.board[1][2] = 'WHITE_TILE'
        self.board.board[1][1] = 'WHITE_TILE'
        self.board.board[1][0] = 'WHITE_TILE'
        self.board.board[4][0] = 'BLACK_TILE'
        self.assertFalse(self.player_one.is_valid_move(1, 3))
        self.assertFalse(self.player_two.is_valid_move(4, 1))

    def test_get_valid_moves(self):
        self.assertEqual(len(self.player_one.get_valid_moves()), 4)


if __name__ == '__main__':
    unittest.main()
