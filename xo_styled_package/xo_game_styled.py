#!/usr/bin/env python3
"""
XO — Styled Tic-Tac-Toe
- Single-file tkinter app, includes Vs Computer (minimax) and 2-player
- To run: python xo_game_styled.py
- To build a Windows exe (example):
    pip install pyinstaller
    pyinstaller --onefile --windowed --icon=assets/game_icon.ico xo_game_styled.py
"""
import tkinter as tk
from tkinter import messagebox, ttk
import os
EMPTY = ""
PLAYER_X = "X"
PLAYER_O = "O"

class TicTacToe:
    def __init__(self):
        self.board = [EMPTY]*9
        self.current = PLAYER_X
        self.game_over = False

    def reset(self):
        self.board = [EMPTY]*9
        self.current = PLAYER_X
        self.game_over = False

    def make_move(self, idx):
        if self.board[idx] != EMPTY or self.game_over:
            return False
        self.board[idx] = self.current
        if self.check_winner(self.current):
            self.game_over = True
        elif EMPTY not in self.board:
            self.game_over = True
        else:
            self.current = PLAYER_O if self.current == PLAYER_X else PLAYER_X
        return True

    def check_winner(self, player):
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in lines:
            if self.board[a]==player and self.board[b]==player and self.board[c]==player:
                return True
        return False

    def winner(self):
        if self.check_winner(PLAYER_X):
            return PLAYER_X
        if self.check_winner(PLAYER_O):
            return PLAYER_O
        if EMPTY not in self.board:
            return "Draw"
        return None

    def available_moves(self):
        return [i for i,v in enumerate(self.board) if v==EMPTY]

    def minimax(self, is_maximizing):
        winner = self.winner()
        if winner == PLAYER_X:
            return -1
        if winner == PLAYER_O:
            return 1
        if winner == "Draw":
            return 0
        if is_maximizing:
            best = -999
            for mv in self.available_moves():
                self.board[mv] = PLAYER_O
                score = self.minimax(False)
                self.board[mv] = EMPTY
                if score > best:
                    best = score
            return best
        else:
            best = 999
            for mv in self.available_moves():
                self.board[mv] = PLAYER_X
                score = self.minimax(True)
                self.board[mv] = EMPTY
                if score < best:
                    best = score
            return best

    def best_move(self):
        best_score = -999
        move = None
        for mv in self.available_moves():
            self.board[mv] = PLAYER_O
            score = self.minimax(False)
            self.board[mv] = EMPTY
            if score > best_score:
                best_score = score
                move = mv
        return move

class TicTacToeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XO — Styled Tic Tac Toe")
        # set window icon if available
        try:
            this_dir = os.path.dirname(__file__)
            ico = os.path.join(this_dir, "assets", "game_icon.ico")
            if os.path.exists(ico):
                self.iconbitmap(ico)
        except Exception:
            pass
        self.resizable(False, False)
        self.game = TicTacToe()
        self.vs_ai = tk.BooleanVar(value=True)
        self.scores = {PLAYER_X:0, PLAYER_O:0, "Draw":0}
        self._build_ui()
        self.update_ui()

    def _build_ui(self):
        self.configure(bg="#0f1724")
        header = tk.Frame(self, bg="#071024", pady=10, padx=12)
        header.grid(row=0, column=0, columnspan=2, sticky="we")
        title = tk.Label(header, text="XO — Styled", font=("Segoe UI", 18, "bold"), fg="white", bg="#071024")
        title.pack(side="left")
        mode_frame = tk.Frame(header, bg="#071024")
        mode_frame.pack(side="right")
        tk.Radiobutton(mode_frame, text="Vs Computer", variable=self.vs_ai, value=True, indicatoron=0, width=12, command=self.on_mode_change).pack(side="left", padx=4)
        tk.Radiobutton(mode_frame, text="2 Players", variable=self.vs_ai, value=False, indicatoron=0, width=12, command=self.on_mode_change).pack(side="left", padx=4)

        board_frame = tk.Frame(self, bg="#071024", padx=12, pady=12)
        board_frame.grid(row=1, column=0, padx=12, pady=6)
        self.btns = []
        btn_font = ("Segoe UI", 28, "bold")
        for r in range(3):
            for c in range(3):
                i = r*3 + c
                b = tk.Button(board_frame, text="", font=btn_font, width=3, height=1,
                              relief="groove", bd=4, command=lambda idx=i: self.on_cell_click(idx))
                b.grid(row=r, column=c, padx=8, pady=8)
                self.btns.append(b)

        right = tk.Frame(self, bg="#071024", padx=10, pady=10)
        right.grid(row=1, column=1, sticky="ns", padx=(0,12))
        self.lbl_status = tk.Label(right, text="Status", fg="white", bg="#071024", font=("Segoe UI", 12))
        self.lbl_status.pack(pady=(0,10))
        self.scoreboard = tk.Label(right, text=self._score_text(), fg="white", bg="#071024", justify="left", font=("Segoe UI", 11))
        self.scoreboard.pack(pady=(0,12))
        tk.Button(right, text="Restart", command=self.restart_round, width=18).pack(pady=4)
        tk.Button(right, text="Reset Scores", command=self.reset_scores, width=18).pack(pady=4)
        tk.Button(right, text="Quit", command=self.quit, width=18).pack(pady=4)

    def _score_text(self):
        return f"X: {self.scores[PLAYER_X]}   O: {self.scores[PLAYER_O]}   Draws: {self.scores['Draw']}"

    def on_mode_change(self):
        self.restart_round()

    def on_cell_click(self, idx):
        if self.game.game_over:
            return
        moved = self.game.make_move(idx)
        if not moved:
            return
        self.update_ui()
        self.after(80, self.post_move_actions)

    def post_move_actions(self):
        winner = self.game.winner()
        if winner:
            self.finish_round(winner)
            return
        if self.vs_ai.get() and self.game.current == PLAYER_O and not self.game.game_over:
            mv = self.game.best_move()
            if mv is not None:
                self.game.make_move(mv)
                self.update_ui()
                winner = self.game.winner()
                if winner:
                    self.finish_round(winner)

    def finish_round(self, winner):
        if winner == PLAYER_X:
            self.scores[PLAYER_X] += 1
            messagebox.showinfo("Winner", "Player X wins!")
        elif winner == PLAYER_O:
            self.scores[PLAYER_O] += 1
            messagebox.showinfo("Winner", "Player O wins!")
        else:
            self.scores["Draw"] += 1
            messagebox.showinfo("Draw", "It's a draw!")
        self.game.game_over = True
        self.update_ui()

    def restart_round(self):
        self.game.reset()
        self.update_ui()

    def reset_scores(self):
        self.scores = {PLAYER_X:0, PLAYER_O:0, "Draw":0}
        self.restart_round()

    def update_ui(self):
        for i,b in enumerate(self.btns):
            b.config(text=self.game.board[i] or "")
            if self.game.board[i] == PLAYER_X:
                b.config(fg="#ef4444", bg="#fff1f0")
            elif self.game.board[i] == PLAYER_O:
                b.config(fg="#1e90ff", bg="#eef6ff")
            else:
                b.config(fg="#0b1220", bg="#f8fafc")
            b.config(state="normal" if not self.game.game_over and self.game.board[i]==EMPTY else "disabled")

        if self.game.game_over:
            w = self.game.winner()
            if w == "Draw":
                self.lbl_status.config(text="Round over — Draw")
            else:
                self.lbl_status.config(text=f"Round over — {w} wins")
        else:
            self.lbl_status.config(text=f"Turn: {self.game.current}")
        self.scoreboard.config(text=self._score_text())

if __name__ == "__main__":
    app = TicTacToeUI()
    app.mainloop()
