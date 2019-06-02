from flask import Flask, request, jsonify
import json

from engine import alphabeta

app = Flask(__name__)

game = alphabeta.Engine(max_depth=3)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.route("/")
def index():
    return "Welcome to my chess API"


@app.route("/board", methods=["GET"])
def display_board():
    global game
    return json.dumps({"board": str(game.board)})


@app.route("/move", methods=["POST"])
def make_move():
    game_inputs = json.loads(request.data)
    global game
    game.move(game_inputs["move"])
    return json.dumps({"board": str(game.board)})


@app.route("/play", methods=["POST"])
def play_move_and_get_response():
    game_inputs = json.loads(request.data)
    global game
    game.play(game_inputs["move"])
    return json.dumps({"board": str(game.board)})


@app.route("/undo", methods=["POST"])
def undo():
    global game
    game.undo(1)
    return json.dumps({"board": str(game.board)})


@app.route("/evaluate", methods=["GET"])
def eval():
    global game
    evaluation = game.evaluate(game.board)
    return json.dumps({"evaluation": evaluation})


@app.route("/reset", methods=["POST"])
def reset():
    global game
    game = alphabeta.Engine(max_depth=3)
    return json.dumps({"board": str(game.board)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
