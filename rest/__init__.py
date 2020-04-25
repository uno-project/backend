import logging
import os
import sys

from flask import Flask, current_app, request, g, jsonify, make_response
from flask_restful import Api

from .game_api import GameApi
from .player_api import PlayerApi

def create_app():
    # start config
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config.logger = logging.getLogger()
    app.config.games = {}
    app.config.players = {}

    # add endpoints
    api = Api(app)
    api.add_resource(GameApi, '/game', '/game/<gameId>')
    api.add_resource(PlayerApi, '/player', '/player/<playerId>')
    return app
