import tkinter as tk
import unittest

from app import TicTacToeApp


class TicTacToeAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = TicTacToeApp(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.app.mode.set("2인 플레이")
        self.app.new_round()

    def test_click_places_mark_and_updates_turn(self):
        self.app.play_cell(0)
        self.assertEqual(self.app.game.board[0], "X")
        self.assertEqual(self.app.game.current_player, "O")
        self.assertEqual(self.app.cells[0]["text"], "X")

    def test_x_win_updates_score(self):
        for move in (0, 3, 1, 4, 2):
            self.app.play_cell(move)
        self.assertEqual(self.app.game.winner, "X")
        self.assertEqual(self.app.scores["X"], 1)
        self.assertIn("X", self.app.status.get())

    def test_new_round_keeps_scores_and_clears_board(self):
        for move in (0, 3, 1, 4, 2):
            self.app.play_cell(move)
        self.app.new_round()
        self.assertEqual(self.app.game.board, [None] * 9)
        self.assertEqual(self.app.scores["X"], 1)

    def test_reset_scores_clears_scoreboard(self):
        self.app.scores["X"] = 2
        self.app.reset_scores()
        self.assertEqual(self.app.scores, {"X": 0, "O": 0, "draw": 0})

    def test_computer_takes_a_turn_after_human(self):
        self.app.mode.set("컴퓨터 대전")
        self.app.new_round()
        self.app.play_cell(0)
        self.app._cancel_ai()
        self.app._play_ai_move()
        self.assertEqual(self.app.game.current_player, "X")
        self.assertEqual(sum(mark is not None for mark in self.app.game.board), 2)


if __name__ == "__main__":
    unittest.main()
