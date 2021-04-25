import logging

from flask import Flask, Response, current_app, g, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import JWTManager, create_access_token

from .game_api import GameApi
from .game_lobby import GameLobby
from .player_api import PlayerApi

from uno.exceptions import UnoRuleException

def create_app():
    # start config
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = 'super-secret'
    app.config.logger = logging.getLogger()
    app.config.games = {}
    app.config.players = {}

    # handle exceptions
    app.register_error_handler(UnoRuleException, handle_uno_exception)

    # add cors
    CORS(app, supports_credentials=True)

    # add jwt
    JWTManager(app)

    # add endpoints
    api = Api(app)
    api.add_resource(GameApi, '/game', '/game/<gameId>')
    api.add_resource(GameLobby, '/lobby/<gameId>')
    api.add_resource(PlayerApi, '/player', '/player/<playerId>')

    return app

def handle_uno_exception(e):
    return make_response(jsonify(message="".join(e.args)), 400)
