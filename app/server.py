import flask
import json
from flask_cors import CORS
from engine import alphabeta
import chess

app = flask.Flask(__name__)
CORS(app)  # This will enable CORS for all routes

game = alphabeta.Engine(max_depth=3)


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


@app.route("/")
def index():
    return "Welcome to my chess API"


@app.route("/board", methods=["GET"])
def display_board():
    global game
    return json.dumps({"board": str(game.board)})


@app.route("/move", methods=["POST"])
def make_move():
    game_inputs = json.loads(flask.request.data)
    global game
    game.move(game_inputs["move"])
    return json.dumps({"board": str(game.board)})


@app.route("/play", methods=["POST"])
def play_move_and_get_response():
    game_inputs = json.loads(flask.request.data)
    global game
    ai_response = chess.Move.from_uci(game.play(game_inputs["move"]))
    from_square = chess.SQUARE_NAMES[ai_response.from_square]
    to_square = chess.SQUARE_NAMES[ai_response.to_square]
    return json.dumps({"from": from_square, "to": to_square})


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


@app.route("/reset", methods=["GET"])
def reset():
    global game
    game = alphabeta.Engine(max_depth=3)
    return json.dumps({"board": str(game.board)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
