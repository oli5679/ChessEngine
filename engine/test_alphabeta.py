import config
import alphabeta
import pytest
from time import sleep

ROOK_STR = "r . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."
BISHOP_STR = ". . . . . . . b\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."
QUEEN_STR = ". Q . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."


@pytest.fixture
def black_engine():
    return alphabeta.Engine(color="black", max_depth=2)


@pytest.fixture
def white_engine():
    return alphabeta.Engine(color="white", max_depth=2)


def test_engine_creation():
    e1 = alphabeta.Engine(color="white", max_depth=1)
    e2 = alphabeta.Engine(color="black", max_depth=1)


def test_evaluate(black_engine):
    assert black_engine.evaluate(black_engine.board) == 0
    assert black_engine.evaluate(ROOK_STR) == 50
    assert black_engine.evaluate(BISHOP_STR) == 33
    assert black_engine.evaluate(QUEEN_STR) == -99


def test_move(black_engine):
    black_engine.move("d2d4")
    assert (
        str(black_engine.board)
        == "r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . P . . . .\n. . . . . . . .\nP P P . P P P P\nR N B Q K B N R"
    )


def test_play_book(black_engine):
    black_engine.play("e2e4")
    black_engine.play("g1f3")
    assert (
        str(black_engine.board)
        == "r n b q k b n r\np p . . p p p p\n. . . p . . . .\n. . p . . . . .\n. . . . P . . .\n. . . . . N . .\nP P P P . P P P\nR N B Q K B . R"
    )


def test_out_of_book_black(black_engine):
    black_engine.move("e2e4")
    black_engine.move("d7d5")
    black_engine.play("b1a3")
    assert (
        str(black_engine.board)
        == "r n b q k b n r\np p p . p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . p . . .\nN . . . . . . .\nP P P P . P P P\nR . B Q K B N R"
    )


def test_out_of_book_white(white_engine):
    white_engine.move("g8f6")
    white_engine.move("e4e5")
    white_engine.play("a7a5")

    assert (
        str(white_engine.board)
        == "r n b q k b . r\n. p p p p p p p\n. . . . . P . .\np . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P . P P P\nR N B Q K B N R"
    )
