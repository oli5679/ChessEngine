import alphabeta
import pytest
from time import sleep

ROOK_STR = "r . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."
BISHOP_STR = ". . . . . . . b\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."
QUEEN_STR = ". Q . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."


@pytest.fixture
def engine():
    return alphabeta.Engine(max_depth=2)


def test_engine_creation():
    e1 = alphabeta.Engine(max_depth=1)
    e2 = alphabeta.Engine(max_depth=3)


def test_evaluate(engine):
    assert engine.evaluate(engine.board) == 0
    assert engine.evaluate(ROOK_STR) == -50
    assert engine.evaluate(BISHOP_STR) == -33
    assert engine.evaluate(QUEEN_STR) == 99


def test_move(engine):
    assert (
        engine.move("d2d4")
        == "r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . P . . . .\n. . . . . . . .\nP P P . P P P P\nR N B Q K B N R"
    )


def test_play_book(engine):
    engine.play("e2e4")
    response = engine.play("g1f3")
    assert (
        response
        == "r n b q k b n r\np p . . p p p p\n. . . p . . . .\n. . p . . . . .\n. . . . P . . .\n. . . . . N . .\nP P P P . P P P\nR N B Q K B . R"
    )


def test_out_of_book_black(engine):
    engine.move("e2e4")
    engine.move("d7d5")
    response = engine.play("b1a3")
    assert (
        response
        == "r n b q k b n r\np p p . p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . p . . .\nN . . . . . . .\nP P P P . P P P\nR . B Q K B N R"
    )

#def test_alphabeta_black(engine

def test_out_of_book_white(engine):
    engine.move("e2e4")
    engine.move("g8f6")
    engine.move("e4e5")
    result = engine.play("a7a5")

    assert (
        result
        == "r n b q k b . r\n. p p p p p p p\n. . . . . P . .\np . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P . P P P\nR N B Q K B N R"
    )

