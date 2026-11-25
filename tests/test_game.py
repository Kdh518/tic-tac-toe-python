import unittest

from game import TicTacToeGame, choose_ai_move


class TicTacToeGameTests(unittest.TestCase):
    def test_starts_with_empty_board_and_x_turn(self):
        game = TicTacToeGame()
        self.assertEqual(game.board, [None] * 9)
        self.assertEqual(game.current_player, "X")
        self.assertIsNone(game.winner)
        self.assertFalse(game.draw)

    def test_valid_moves_alternate_players(self):
        game = TicTacToeGame()
        game.play(0)
        game.play(4)
        self.assertEqual(game.board[0], "X")
        self.assertEqual(game.board[4], "O")
        self.assertEqual(game.current_player, "X")

    def test_rejects_occupied_square(self):
        game = TicTacToeGame()
        game.play(0)
        with self.assertRaises(ValueError):
            game.play(0)

    def test_detects_row_win_and_stops_game(self):
        game = TicTacToeGame()
        for move in (0, 3, 1, 4, 2):
            game.play(move)
        self.assertEqual(game.winner, "X")
        with self.assertRaises(ValueError):
            game.play(5)

    def test_detects_draw(self):
        game = TicTacToeGame()
        for move in (0, 1, 2, 4, 3, 5, 7, 6, 8):
            game.play(move)
        self.assertTrue(game.draw)
        self.assertIsNone(game.winner)

    def test_reset_clears_game_state(self):
        game = TicTacToeGame()
        game.play(0)
        game.reset()
        self.assertEqual(game.board, [None] * 9)
        self.assertEqual(game.current_player, "X")
        self.assertIsNone(game.winner)
        self.assertFalse(game.draw)

    def test_ai_takes_a_winning_move(self):
        board = ["O", "O", None, "X", "X", None, None, None, None]
        self.assertEqual(choose_ai_move(board, ai_player="O"), 2)

    def test_ai_blocks_an_immediate_loss(self):
        board = ["X", "X", None, "O", None, None, None, "O", None]
        self.assertEqual(choose_ai_move(board, ai_player="O"), 2)


if __name__ == "__main__":
    unittest.main()
