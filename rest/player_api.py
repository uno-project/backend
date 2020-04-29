from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request, jsonify, current_app, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from uno.player import Player

class PlayerApi(Resource):

    @jwt_required
    def get(self):
        playerId = get_jwt_identity()

        # return player info
        player_info = {"id": playerId,
                       "name": current_app.config.players[playerId].name,
                       "cards": [c.reference for c in current_app.config.players[playerId].cards]}

        return make_response(jsonify(player_info))

    def post(self):
        # parse args
        reqparse = RequestParser()
        reqparse.add_argument('name',
                              type=str,
                              required=True,
                              location='json',
                              help="Player name")
        args = reqparse.parse_args()

        # new player
        new = Player(args.name)
        current_app.config.players[new.id] = new
        access_token = create_access_token(identity=new.id)
        return make_response(jsonify(access_token=access_token))



