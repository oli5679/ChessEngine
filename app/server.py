
from flask import Flask, request
import json

from engine import alphabeta

app = Flask(__name__)

game = alphabeta.Engine(color='white',max_depth=3)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "Welcome to my chess API"


@app.route('/board', methods=['GET'])
def display_board():
    global game
    return json.dumps({'board':str(game.board)})


@app.route('/board', methods=['POST'])
def create_new_game(extras=dict()):
    if not request.json:
        abort(400)
    else:
        game_inputs = request.json
        global game
        game = alphabeta.Engine(color=game_inputs['color'],
        max_depth=game_inputs['max_depth'])
        return json.dumps({'board':str(game.board)})

    
@app.route('/move', methods=['POST'])
def make_move():
    game_inputs = request.json
    global game
    game.move(game_inputs['move'])
    return json.dumps({'board':str(game.board)})

@app.route('/play', methods=['POST'])
def play_move_and_get_response():
    game_inputs = request.json
    global game
    game.play(game_inputs['move'])
    return json.dumps({'board':str(game.board)})

@app.route('/undo', methods=['POST'])
def undo():
    game_inputs = request.json
    global game
    game.undo(1)
    return json.dumps({'board':str(game.board)})

@app.route('/evaluate', methods=['GET'])
def eval():
    game_inputs = request.json
    global game
    evaluation = game.evaluate(game.board)
    return json.dumps({'evaluation':evaluation})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")