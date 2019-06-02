import os
import tempfile

import pytest
import flask
import server
import easydict


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
