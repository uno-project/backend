from flask_restful import Resource
from flask import request, jsonify, current_app, g, make_response


class Game(Resource):
    def get(self, albumId):
        return jsonify({"message": "ok"})


