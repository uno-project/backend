from flask_restful import Resource
from flask import request, jsonify, current_app, make_response, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from uno.exceptions import UnoRuleException
from .game_api import GameApi

class GameLobby(Resource):

    def get(self, gameId):
        """
        Returns game information
        """
        # not found, return response
        game = GameApi.get_game(gameId)
        if isinstance(game, Response):
            return game

        def event_stream():
            for msg in game.notifications:
                yield msg
            game.notifications = []


        return Response(event_stream(),
                        mimetype="text/event-stream")

    @jwt_required
    def post(self, gameId):
        """
        Add a player
        """
        # check if players can be found
        playerId = get_jwt_identity()
        if playerId not in current_app.config.players.keys():
            return make_response(jsonify(message=f"Player {playerId} not found"), HTTPStatus.NOT_FOUND)

        # add players and start
        game = GameApi.get_game(gameId)
        try:
            game.addPlayer(current_app.config.players[playerId])
            game.add_notification("new_player")
        except UnoRuleException as e:
            return make_response(jsonify(message=str(e)), HTTPStatus.BAD_REQUEST)

        return 200

    @jwt_required
    def patch(self, gameId):
        """
        Starts a game
        """
        # add players and start
        game = GameApi.get_game(gameId)
        try:
            game.start()
        except UnoRuleException as e:
            return make_response(jsonify(message=str(e)), HTTPStatus.BAD_REQUEST)

        return 200
