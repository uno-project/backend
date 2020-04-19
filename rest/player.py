from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request, jsonify, current_app, make_response

from uno.player import Player

class PlayerApi(Resource):

    def get(self, playerId):
        if playerId not in current_app.config.players:
            return make_response(jsonify(message="Not found"), 404)

        # return player info
        player_info = {"name": current_app.config.players[playerId].name,
                       "cards": current_app.config.players[playerId].cards}

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
        print(current_app.config.players)
        return make_response(jsonify(playerId=new.id))



