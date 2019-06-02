import os
import tempfile

import pytest
import flask
import server
import easydict
from engine import alphabeta
import json


@pytest.fixture
def client():
    yield server.app.test_client()


def test_base(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Welcome to my chess API"


def test_display_board(client):
    response = client.get("/board")
    assert response.status_code == 200
    assert (
        response.data
        == b'{"board": "r n b q k b n r\\np p p p p p p p\\n. . . . . . . .\\n. . . . . . . .\\n. . . . . . . .\\n. . . . . . . .\\nP P P P P P P P\\nR N B Q K B N R"}'
    )


def test_make_move(client):
    response = client.post("/move", data=json.dumps({"move": "e2e4"}))

    assert response.status_code == 200
    assert (
        response.data
        == b'{"board": "r n b q k b n r\\np p p p p p p p\\n. . . . . . . .\\n. . . . . . . .\\n. . . . P . . .\\n. . . . . . . .\\nP P P P . P P P\\nR N B Q K B N R"}'
    )


def test_make_move_and_get_response(client):
    response = client.post("/play", data=json.dumps({"move": "e7e5"}))
    assert response.status_code == 200
    assert len(json.loads(response.data)["board"]) > 100


def test_evaluate(client):
    response = client.get("/evaluate")
    assert response.status_code == 200
    assert json.loads(response.data)["evaluation"] > -1e7


def test_reset_board(client):
    # todo
    assert True


def test_undo_move(client):
    # todo
    assert True
