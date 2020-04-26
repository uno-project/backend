import logging

from flask import Flask, current_app, request, g, jsonify, make_response
from flask_restful import Api
from werkzeug.security import safe_str_cmp
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
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

    # add jwt
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    jwt = JWTManager(app)

    # add endpoints
    api = Api(app)
    api.add_resource(GameApi, '/game', '/game/<gameId>')
    api.add_resource(PlayerApi, '/player', '/player/<playerId>')
    return app


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
def login():
    # parse request
    reqparse = RequestParser()
    reqparse.add_argument('playerId',
                          type=str,
                          location='json',
                          required=True,
                          help="Player Id")
    reqparse.add_argument('playerName',
                          type=str,
                          location='json',
                          required=True,
                          help="Player Id")
    args = reqparse.parse_args()


    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=args.playerId)
    return jsonify(access_token=access_token), 200

