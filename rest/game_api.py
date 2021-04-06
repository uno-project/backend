from flask_restful import Resource
from flask import request, jsonify, current_app, g, make_response, Response
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from uno.exceptions import UnoWinnerException, UnoRuleException
from uno.game import Game


class GameApi(Resource):

    def _get_game(self, gameId):
        """
        Pick a game from the list
        """
        if gameId not in current_app.config.games:
            return make_response(jsonify(message="Not found"), HTTPStatus.NOT_FOUND)

        # return player info
        return current_app.config.games[gameId]

    @jwt_required
    def get(self, gameId):
        """
        Returns game information
        """
        # not found, return response
        game = self._get_game(gameId)
        if isinstance(game, Response):
            return game

        players = game.players
        game_info = {"players": [p.id for p in players]}

        return make_response(jsonify(game_info))


    @jwt_required
    def patch(self, gameId):
        """
        Starts a game
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
                return make_response(jsonify(message=f"Player {player} not found"), HTTPStatus.NOT_FOUND)
            players.append(current_app.config.players[player])

        # add players and start
        game = self._get_game(gameId)
        try:
            game.start(players)
        except UnoRuleException as e:
            return make_response(jsonify(message=str(e)), HTTPStatus.BAD_REQUEST)

        return 200

    @jwt_required
    def post(self):
        """
        Creates a game
        """
        try:
            game = Game()
        except UnoRuleException as e:
            return make_response(jsonify(message=str(e)),  HTTPStatus.BAD_REQUEST)

        current_app.config.games[game.id] = game
        return make_response(jsonify(gameId=game.id), HTTPStatus.CREATED)


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
            return make_response(jsonify(message=f"Game {gameId} not found"), HTTPStatus.NOT_FOUND)
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
            return make_response(jsonify(message=f"Cannot make play: {e}"), HTTPStatus.BAD_REQUEST)

        return jsonify(message="success")
