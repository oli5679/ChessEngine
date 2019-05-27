import config
import alphabeta
import pytest

ROOK_STR = "r . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."
BISHOP_STR = ". . . . . . . b\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."
QUEEN_STR = ". Q . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . ."


@pytest.fixture
def engine():
    return alphabeta.Engine(color="black", max_depth=3)


def test_engine_creation():
    e1 = alphabeta.Engine(color="white", max_depth=3)
    e2 = alphabeta.Engine(color="black", max_depth=4)


def test_evaluate(engine):
    assert engine.evaluate(engine.board) == 0
    assert engine.evaluate(ROOK_STR) == 50
    assert engine.evaluate(BISHOP_STR) == 33
    assert engine.evaluate(QUEEN_STR) == -99

def test_move(engine):
    engine.move('d2d4')
    assert str(engine.board) == 'r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . P . . . .\n. . . . . . . .\nP P P . P P P P\nR N B Q K B N R'


