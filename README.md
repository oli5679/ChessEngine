# chess-engine

Basic Python chess engine, including simple gui!

## Info

logic - minimax + heuristic https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

including opening book from http://rebel13.nl/download/books.html

## setup

prerequesite - https://www.anaconda.com/

    conda config --add channels conda-forge
    conda env create -n ChessEngine -f environment.yml
    conda activate ChessEngine

NOTE - Dockerfile not working yet

## Run tests

    pytest app/server.py

## Run server

    python app/server.py

## Play API

Uses uci move notation https://python-chess.readthedocs.io/en/latest/

Posting to 'play' endpoint submits move to board, and gets A.I response

    import requests
    import json

    data = json.dumps({'move':'e2e4'})
    path = 'http://0.0.0.0:5000/play'    
    resp = requests.post(url=path,data=data )

    #resp.data == b'{"from": "e7", "to": "e5"}'

## Play gui

go to app/static/index.html and open in browser

NOTE - A.I is always white, and starts with D2D4.
