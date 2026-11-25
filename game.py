"""Pure game rules and an unbeatable minimax opponent for Tic-Tac-Toe."""

from __future__ import annotations

from math import inf

Board = list[str | None]
WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)
MOVE_ORDER = (4, 0, 2, 6, 8, 1, 3, 5, 7)


def find_winner(board: Board) -> str | None:
    """Return X or O when that player has a line; otherwise return None."""
    _validate_board(board)
    for a, b, c in WINNING_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def _validate_board(board: Board) -> None:
    if len(board) != 9 or any(cell not in (None, "X", "O") for cell in board):
        raise ValueError("보드는 None, X, O 값 9개로 이루어져야 합니다.")


class TicTacToeGame:
    """Mutable state for one local Tic-Tac-Toe game."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board: Board = [None] * 9
        self.current_player = "X"
        self.winner: str | None = None
        self.draw = False

    @property
    def game_over(self) -> bool:
        return self.winner is not None or self.draw

    def play(self, index: int) -> str | None:
        """Place the current player's mark; return the winner if the game ends."""
        if self.game_over:
            raise ValueError("게임이 끝났습니다. 새 게임을 시작하세요.")
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < 9:
            raise ValueError("칸 번호는 0~8이어야 합니다.")
        if self.board[index] is not None:
            raise ValueError("이미 선택된 칸입니다.")

        player = self.current_player
        self.board[index] = player
        self.winner = find_winner(self.board)
        if self.winner is None:
            self.draw = all(cell is not None for cell in self.board)
        if not self.game_over:
            self.current_player = "O" if player == "X" else "X"
        return self.winner


def choose_ai_move(board: Board, ai_player: str = "O") -> int:
    """Choose an optimal move with minimax; the opponent cannot force a win."""
    _validate_board(board)
    if ai_player not in ("X", "O"):
        raise ValueError("AI 기호는 X 또는 O여야 합니다.")
    if find_winner(board) is not None or all(cell is not None for cell in board):
        raise ValueError("게임이 끝난 보드에는 수를 둘 수 없습니다.")
    opponent = "O" if ai_player == "X" else "X"
    working = board.copy()
    best_score = -inf
    best_move: int | None = None

    for index in MOVE_ORDER:
        if working[index] is not None:
            continue
        working[index] = ai_player
        score = _minimax(working, opponent, ai_player, opponent, depth=1)
        working[index] = None
        if score > best_score:
            best_score, best_move = score, index

    if best_move is None:
        raise ValueError("둘 수 있는 칸이 없습니다.")
    return best_move


def _minimax(board: Board, player: str, ai_player: str, opponent: str, depth: int) -> int:
    winner = find_winner(board)
    if winner == ai_player:
        return 10 - depth
    if winner == opponent:
        return depth - 10
    if all(cell is not None for cell in board):
        return 0

    scores: list[int] = []
    for index in MOVE_ORDER:
        if board[index] is not None:
            continue
        board[index] = player
        next_player = opponent if player == ai_player else ai_player
        scores.append(_minimax(board, next_player, ai_player, opponent, depth + 1))
        board[index] = None
    return max(scores) if player == ai_player else min(scores)
