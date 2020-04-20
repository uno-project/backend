from flask_restful import Resource
from flask import request, jsonify, current_app, g, make_response

from flask_restful.reqparse import RequestParser
from uno.game import Game


class GameApi(Resource):
    def get(self, gameId):
        if gameId not in current_app.config.games:
            return make_response(jsonify(message="Not found"), 404)

        # return player info
        players = current_app.config.games[gameId].players
        game_info = {"players": [p.id for p in players]}

        return make_response(jsonify(game_info))

    def post(self):
        reqparse = RequestParser()
        reqparse.add_argument('players',
                              type=list,
                              location='json',
                              required="True",
                              help="List of players")
        args = reqparse.parse_args()

        # check if players can be found
        players = []
        for player in args.players:
            if player not in current_app.config.players:
                return make_response(jsonify(message=f"Player {player} not found"), 404)
            players.append(current_app.config.players[player])

        game = Game(players)
        current_app.config.games[game.id] = game
        return jsonify({"gameId": game.id})



