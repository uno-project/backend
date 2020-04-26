from flask_restful import Resource
from flask import request, jsonify, current_app, g, make_response
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity

from uno.exceptions import UnoWinnerException
from uno.game import Game


class GameApi(Resource):

    @jwt_required
    def get(self, gameId):
        """
        Returns game information
        """
        if gameId not in current_app.config.games:
            return make_response(jsonify(message="Not found"), 404)

        # return player info
        players = current_app.config.games[gameId].players
        game_info = {"players": [p.id for p in players]}

        return make_response(jsonify(game_info))

    @jwt_required
    def post(self):
        """
        Creates a game
        """
        # parse request
        reqparse = RequestParser()
        reqparse.add_argument('players',
                              type=list,
                              location='json',
                              required=True,
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

    @jwt_required
    def put(self, gameId):
        """
        Play a card
        """
        # parse request
        reqparse = RequestParser()
        reqparse.add_argument('cardId',
                              type=str,
                              location='json',
                              required=True,
                              help="Player Id")
        reqparse.add_argument('unoFlag',
                              type=bool,
                              default=False,
                              location='json',
                              required=False,
                              help="Uno flag")

        args = reqparse.parse_args()

        # player Id
        playerId = get_jwt_identity()

        # search game
        if gameId not in current_app.config.games:
            return make_response(jsonify(message=f"Game {gameId} not found"), 404)
        game = current_app.config.games[gameId]

        # try to play card
        try:
            game.register_play(playerId,
                               args.cardId,
                               args.unoFlag)
        # winner
        except UnoWinnerException as e:
            return jsonify(message=str(e))

        except Exception as e:
            return make_response(jsonify(message=f"Cannot make play: {e}"), 400)

        return jsonify(message="success")
