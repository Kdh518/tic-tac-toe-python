"""Tkinter user interface for Tic-Tac-Toe."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from game import TicTacToeGame, choose_ai_move


class TicTacToeApp:
    MODES = ("2인 플레이", "컴퓨터 대전")

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("틱택토")
        self.root.geometry("460x620")
        self.root.minsize(360, 500)
        self.root.configure(bg="#f3f6fb")
        self.game = TicTacToeGame()
        self.mode = tk.StringVar(value=self.MODES[0])
        self.status = tk.StringVar(value="X 차례")
        self.scores = {"X": 0, "O": 0, "draw": 0}
        self._ai_job: str | None = None
        self.cells: list[tk.Button] = []

        style = ttk.Style(root)
        try:
            style.theme_use("vista")
        except tk.TclError:
            style.theme_use("clam")
        style.configure("TFrame", background="#f3f6fb")
        style.configure("TLabel", background="#f3f6fb", foreground="#182230", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 26), foreground="#172b4d")
        style.configure("Status.TLabel", font=("Segoe UI Semibold", 16), foreground="#174ea6")
        style.configure("TButton", font=("Segoe UI", 11), padding=8)

        page = ttk.Frame(root, padding=20)
        page.pack(fill="both", expand=True)
        header = ttk.Frame(page)
        header.pack(fill="x", pady=(0, 8))
        ttk.Label(header, text="틱택토", style="Header.TLabel").pack(side="left")
        self.mode_box = ttk.Combobox(header, textvariable=self.mode, values=self.MODES, state="readonly", width=14)
        self.mode_box.pack(side="right")
        self.mode_box.bind("<<ComboboxSelected>>", self._mode_changed)

        ttk.Label(page, textvariable=self.status, style="Status.TLabel", anchor="center").pack(fill="x", pady=(4, 12))

        board_frame = ttk.Frame(page, padding=8)
        board_frame.pack(fill="both", expand=True)
        for row in range(3):
            board_frame.rowconfigure(row, weight=1, uniform="row")
        for column in range(3):
            board_frame.columnconfigure(column, weight=1, uniform="column")
        for index in range(9):
            button = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 38, "bold"),
                bg="#ffffff",
                fg="#174ea6",
                activebackground="#e7efff",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda cell=index: self.play_cell(cell),
            )
            button.grid(row=index // 3, column=index % 3, sticky="nsew", padx=5, pady=5, ipadx=8, ipady=8)
            self.cells.append(button)

        score_frame = ttk.Frame(page, padding=(0, 14, 0, 10))
        score_frame.pack(fill="x")
        self.score_labels: dict[str, ttk.Label] = {}
        for key, title in (("X", "X"), ("draw", "무승부"), ("O", "O")):
            panel = ttk.Frame(score_frame, padding=6)
            panel.pack(side="left", expand=True, fill="x")
            ttk.Label(panel, text=title, anchor="center").pack(fill="x")
            score = ttk.Label(panel, text="0", anchor="center", font=("Segoe UI Semibold", 20))
            score.pack(fill="x")
            self.score_labels[key] = score

        actions = ttk.Frame(page)
        actions.pack(fill="x", pady=(4, 0))
        ttk.Button(actions, text="새 게임", command=self.new_round).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(actions, text="점수 초기화", command=self.reset_scores).pack(side="left", expand=True, fill="x", padx=(4, 0))
        ttk.Label(page, text="키보드: 1–9로 칸 선택 · R로 새 게임", anchor="center", foreground="#5c6675").pack(fill="x", pady=(10, 0))
        root.bind("<Key>", self._on_key)
        self._render()

    def play_cell(self, index: int) -> None:
        if self.game.game_over:
            return
        if self.mode.get() == "컴퓨터 대전" and self.game.current_player == "O":
            return
        try:
            self.game.play(index)
        except ValueError:
            return
        self._after_move()
        if self.mode.get() == "컴퓨터 대전" and not self.game.game_over and self.game.current_player == "O":
            self.status.set("컴퓨터 생각 중…")
            self._render()
            self._ai_job = self.root.after(220, self._play_ai_move)

    def _play_ai_move(self) -> None:
        self._ai_job = None
        if self.mode.get() != "컴퓨터 대전" or self.game.game_over or self.game.current_player != "O":
            return
        move = choose_ai_move(self.game.board, ai_player="O")
        self.game.play(move)
        self._after_move()

    def _after_move(self) -> None:
        if self.game.winner:
            self.scores[self.game.winner] += 1
            self.status.set(f"{self.game.winner} 승리!")
            self._refresh_scores()
        elif self.game.draw:
            self.scores["draw"] += 1
            self.status.set("무승부!")
            self._refresh_scores()
        else:
            self.status.set(f"{self.game.current_player} 차례")
        self._render()

    def new_round(self) -> None:
        self._cancel_ai()
        self.game.reset()
        self.status.set("X 차례")
        self._render()

    def reset_scores(self) -> None:
        self.scores = {"X": 0, "O": 0, "draw": 0}
        self._refresh_scores()
        self.new_round()

    def _mode_changed(self, _event: tk.Event | None = None) -> None:
        self.reset_scores()

    def _cancel_ai(self) -> None:
        if self._ai_job is not None:
            try:
                self.root.after_cancel(self._ai_job)
            except tk.TclError:
                pass
            self._ai_job = None

    def _refresh_scores(self) -> None:
        for key, label in self.score_labels.items():
            label.configure(text=str(self.scores[key]))

    def _render(self) -> None:
        ai_turn = self.mode.get() == "컴퓨터 대전" and self.game.current_player == "O" and not self.game.game_over
        for index, button in enumerate(self.cells):
            mark = self.game.board[index]
            button.configure(
                text=mark or "",
                fg="#174ea6" if mark == "X" else "#c5221f" if mark == "O" else "#182230",
                state="disabled" if mark is not None or self.game.game_over or ai_turn else "normal",
                disabledforeground="#174ea6" if mark == "X" else "#c5221f" if mark == "O" else "#182230",
                bg="#e7f0ff" if mark == "X" else "#fde8e7" if mark == "O" else "#ffffff",
            )

    def _on_key(self, event: tk.Event) -> str | None:
        if event.char in "123456789":
            self.play_cell(int(event.char) - 1)
            return "break"
        if event.char.lower() == "r":
            self.new_round()
            return "break"
        return None


def main() -> None:
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
