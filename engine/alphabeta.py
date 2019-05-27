import chess
import numpy as np
from copy import deepcopy
from sys import _getframe
import config
import pandas as pd
from chess.polyglot import open_reader


class TailCallSigil(Exception):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call(function):
    """
	A decorator for functions set up for tail call optimization. If your
	function *isn't* set up for tail call optimization, this won't work
	as intended.
	"""

    def wrapper(*args, **kwargs):
        """
		Wraps a function optimized for tail calls, allowing them to reuse the
		stack.
		
		"""

        try:
            # Check to make sure we aren't our own grandparent.
            frame_0, frame_2 = _getframe(0), _getframe(2)

            if frame_2 and frame_0.f_code == frame_2.f_code:
                raise TailCallSigil(args, kwargs)

        except ValueError:
            pass

        while True:
            try:
                # Will be called decorated, hence the grandparents above.
                result = function(*args, **kwargs)

            except TailCallSigil as sigil:
                args, kwargs = sigil.args, sigil.kwargs

            else:
                return result

    return wrapper


class Engine:
    def __init__(self, color="white", max_depth=2, opening_book="Perfect2017.bin"):
        self.board = chess.Board()
        self.eval_hash = {}
        self.board_hash = {}
        self.max_depth = max_depth
        self.opening_book = opening_book
        if color == "white":
            self.minimax_scalar = -1
            self._auto_respond(self.max_depth)
        else:
            self.minimax_scalar = 1

    def evaluate(self, board):
        board_list = str(board).split()
        evaluation = 0
        position = 0
        for piece in board_list:
            evaluation += config.PIECE_VALUE[piece]
            evaluation += config.POSITION_VALUE[piece][position]
            position += 1
        return evaluation

    def move(self, move):
        print(f"move: {move}")
        self.board.push(chess.Move.from_uci(move))
        print(self.board)

    def play(self, move):
        self.move(move)
        if (
            self.board.is_stalemate()
            or self.board.is_insufficient_material()
            or self.board.can_claim_threefold_repetition()
        ):
            print("draw")
        elif self.board.is_checkmate():
            print("you win")
        print()
        self._auto_respond(self.max_depth)
        if (
            self.board.is_stalemate()
            or self.board.is_insufficient_material()
            or self.board.can_claim_threefold_repetition()
        ):
            print("draw")
        elif self.board.is_checkmate():
            print("you lose")

    def _move_copy(self, board, move):
        copy_board = deepcopy(board)
        copy_board.push(move)
        return copy_board

    def _alphabeta(self, board, max_depth, current_depth=0, alpha=-1e6, beta=1e6):
        if (
            board.is_stalemate()
            or board.is_insufficient_material()
            or board.can_claim_threefold_repetition()
        ):
            return 0
        elif board.is_checkmate():
            if current_depth % 2 == 1:
                return 1e6
            else:
                return -1e6

        else:
            hash_string = board.fen() + f"depth{max_depth-current_depth}"
            if hash_string in self.eval_hash.keys():
                return self.eval_hash[hash_string]
            else:
                current_depth += 1
                if current_depth == max_depth:
                    value = self.evaluate(board)

                elif current_depth % 2 == 1:
                    value = 1e6
                    for m in board.legal_moves:
                        value = min(
                            value,
                            self._alphabeta(
                                self._move_copy(board, m),
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
            values = np.array(
                [
                    self._alphabeta(self._move_copy(self.board, m), max_depth, 0)
                    for m in self.board.legal_moves
                ]
            )
            chosen_move = list(self.board.legal_moves)[np.argmax(values)]
        print(f"response {chosen_move}")
        self.board.push(chosen_move)
        print(self.board)
