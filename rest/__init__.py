import logging

from flask import Flask, current_app, g, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import JWTManager, create_access_token

from .game_api import GameApi
from .player_api import PlayerApi

def create_app():
    # start config
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = 'super-secret'
    app.config.logger = logging.getLogger()
    app.config.games = {}
    app.config.players = {}

    # add cors
    cors = CORS(app, supports_credentials=True)

    # add jwt
    jwt = JWTManager(app)

    # add endpoints
    api = Api(app)
    api.add_resource(GameApi, '/game', '/game/<gameId>')
    api.add_resource(PlayerApi, '/player', '/player/<playerId>')
    return app


