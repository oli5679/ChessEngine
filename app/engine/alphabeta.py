import chess
import numpy as np
from copy import deepcopy
from sys import _getframe
import config
import pandas as pd
from chess.polyglot import open_reader


class Engine:
    def __init__(self, max_depth=2, opening_book="Perfect2017.bin"):
        self.board = chess.Board()
        self.eval_hash = {}
        self.max_depth = max_depth
        self.opening_book = opening_book
        self.board_hash = {}
        self.current_move = "white"
        self.game_state = "live"

    def evaluate(self, board):
        board_str = str(board)
        evaluation = self.board_hash.get(board_str)
        if evaluation:
            return evaluation
        else:
            board_list = board_str.split()
            evaluation, position = 0, 0
            for piece in board_list:
                evaluation += config.PIECE_VALUE[piece]
                evaluation += config.POSITION_VALUE[piece][position]
                position += 1
            self.board_hash[board_str] = evaluation
            return evaluation

    def move(self, move):
        self.board.push(chess.Move.from_uci(move))
        self.current_move = self._update_current_move(self.current_move)
        return self.board

    def _update_current_move(self, current_move):
        if current_move == "white":
            return "black"
        else:
            return "white"

    def _check_game_state(self):
        if (
            self.board.is_stalemate()
            or self.board.is_insufficient_material()
            or self.board.can_claim_threefold_repetition()
        ):
            self.game_state = "draw"
            return self.game_state
        elif self.board.is_checkmate():
            self.game_state = f"{self.current_move} win"
            return self.game_state
        else:
            return "live"

    def play(self, move):
        self.move(move)
        game_state = self._check_game_state()
        if game_state == "live":
            response = self._auto_respond(self.max_depth)
            game_state = self._check_game_state()
            if game_state == "live":
                return self.board

        return game_state

    def _move_copy(self, board, move):
        copy_board = deepcopy(board)
        copy_board.push(move)
        return copy_board

    def _alphabeta(
        self, board, color, max_depth, current_depth=0, alpha=-1e6, beta=1e6
    ):
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        elif board.is_checkmate():
            if color == "white":
                return 1e6
            else:
                return -1e6

        else:
            hash_string = board.fen() + f"depth{max_depth-current_depth}"
            if hash_string in self.eval_hash.keys():
                return self.eval_hash[hash_string]
            else:
                current_depth += 1
                next_color = self._update_current_move(color)
                if current_depth == max_depth:
                    value = self.evaluate(board)

                elif color == "black":
                    value = 1e6
                    for m in board.legal_moves:
                        value = min(
                            value,
                            self._alphabeta(
                                self._move_copy(board, m),
                                next_color,
                                max_depth,
                                current_depth,
                                alpha,
                                beta,
                            ),
                        )
                        beta = min(value, beta)
                        if alpha >= beta:
                            break

                else:
                    value = -1e6
                    for m in board.legal_moves:
                        value = max(
                            value,
                            self._alphabeta(
                                self._move_copy(board, m),
                                next_color,
                                max_depth,
                                current_depth,
                                alpha,
                                beta,
                            ),
                        )
                        alpha = max(value, alpha)
                        if alpha >= beta:
                            break

                self.eval_hash[hash_string] = value
                return value

    def _auto_respond(self, max_depth):
        with chess.polyglot.open_reader(self.opening_book) as reader:
            candidate_moves = list(reader.find_all(self.board))
        if candidate_moves:
            chosen_move = candidate_moves[0].move
        else:
            next_color = self._update_current_move(self.current_move)
            values = np.array(
                [
                    self._alphabeta(
                        self._move_copy(self.board, m), next_color, max_depth - 1, 0
                    )
                    for m in self.board.legal_moves
                ]
            )
            if self.color == "white":
                chosen_move = list(self.board.legal_moves)[np.argmax(values)]
            else:
                chosen_move = list(self.board.legal_moves)[np.argmin(values)]
        self.board.push(chosen_move)
        return self.board

    def undo(self, num_undoes):
        for i in range(num_undoes):
            self.board.pop()
