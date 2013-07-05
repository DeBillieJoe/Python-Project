import unittest

import Reversi


WHITE_TILE = Reversi.WHITE_TILE
BLACK_TILE = Reversi.BLACK_TILE


class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Reversi.Board()

    def tearDown(self):
        del self.board

    def test_reset_board(self):
        new_board = Reversi.Board()
        new_board.board[2][3] = WHITE_TILE
        new_board.board[2][2] = BLACK_TILE
        new_board = new_board.reset_board()

        self.assertEqual(self.board.board, new_board.board)


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.board = Reversi.Board()
        self.player_one = Reversi.Player(BLACK_TILE, self.board)
        self.player_two = Reversi.Player(WHITE_TILE, self.board)

    def tearDown(self):
        del self.player_one
        del self.board

    def test_is_valid_move(self):
        self.assertFalse(self.player_two.is_valid_move(8, 8))
        self.assertFalse(self.player_one.is_valid_move(3, 4))
        self.assertTrue(self.player_two.is_valid_move(4, 2))

    def test_valid_move(self):
        self.board.board[1][2] = WHITE_TILE
        self.board.board[1][1] = WHITE_TILE
        self.board.board[1][0] = WHITE_TILE
        self.board.board[4][0] = BLACK_TILE

        self.assertFalse(self.player_one.is_valid_move(1, 3))
        self.assertFalse(self.player_two.is_valid_move(4, 1))

    def test_get_valid_moves(self):
        self.assertEqual(len(self.player_one.get_valid_moves()), 4)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.board = Reversi.Board()
        self.player_one = Reversi.Player(BLACK_TILE, self.board)
        self.player_two = Reversi.Player(WHITE_TILE, self.board)

    def tearDown(self):
        del self.board
        del self.player_one
        del self.player_two

    def test_make_move(self):
        self.player_one.make_move(3, 2, self.player_two)
        self.player_two.make_move(4, 2, self.player_one)

        self.assertEqual(self.board.board[3][2], BLACK_TILE)
        self.assertFalse(self.player_one.make_move(3, 2, self.player_two))

    def test_score(self):
        self.board.reset_board()

        self.player_one.make_move(3, 2, self.player_two)
        self.player_two.make_move(4, 2, self.player_one)
        self.player_one.make_move(5, 3, self.player_two)
        self.player_two.make_move(2, 2, self.player_one)

        score = (self.player_one.score, self.player_two.score)
        self.assertEqual(score, (3, 5))


class TestComputer(unittest.TestCase):
    def setUp(self):
        self.board = Reversi.Board()
        self.player_one = Reversi.Player(BLACK_TILE, self.board)
        self.player_two = Reversi.Computer(WHITE_TILE, self.board)

    def tearDown(self):
        del self.board
        del self.player_one
        del self.player_two

    def test_good_moves(self):
        for i in range(1, 6):
            self.board.board[4][i] = WHITE_TILE
            if i != 4:
                self.board.board[i][4] = BLACK_TILE

        self.board.board[3][2] = BLACK_TILE
        self.board.board[5][2] = BLACK_TILE
        self.board.board[2][5] = BLACK_TILE

        move = self.player_two.computer_move()
        self.player_two.make_move(self.player_one)
        self.assertEqual(move, ((0, 4), [(3, 4), (2, 4), (1, 4)]))

        self.board.board[1][6] = BLACK_TILE
        second_move = self.player_two.computer_move()
        self.player_two.make_move(self.player_one)
        self.assertEqual(second_move, ((0, 7), [(2, 5), (1, 6)]))

    def test_bad_moves(self):
        pass


if __name__ == '__main__':
    unittest.main()
