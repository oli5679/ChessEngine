from flask import Flask, jsonify, make_response, request, abort

from engine import alphabeta

app = Flask(__name__)
games = {}

# HTTP error - json rather than html to be more API friendly (not sure this is working)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.route("/")
def home():
    return "Welcome to my chess api!"


@app.route("/games", methods=["GET"])
def get_games():
    if games.keys():
        games_dict = {g: str(games[g].board) for g in games.keys()}

        games_json = json.dumps(games_dict)
    else:
        games_json = "No active games"
    return games_json


@app.route("/games/<game_id>", methods=["GET"])
def game(game_id):
    game_string = str(games[g].board)

    game_json = json.dumps(game_string)
    return game_json


@app.route("/games", methods=["POST"])
def create_game():
    if not request.json:
        abort(400)
    else:
        input_data = request.json

        return jsonify({"addition": input_data}), 201


if __name__ == "__main__":
    app.run(debug=True)
