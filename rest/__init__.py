import logging
import os
import sys

from flask import Flask, current_app, request, g, jsonify, make_response
from flask_restful import Api

from .game import Game
from .player import Player

# setup logging and start app

def create_app():
    # start config
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config.logger = logging.getLogger()

    # add endpoints
    api = Api(app)
    api.add_resource(Game, '/game', '/game/<gameId>')
    api.add_resource(Player, '/game', '/game/<gameId>')
    return app
