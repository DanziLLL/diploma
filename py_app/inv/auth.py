from flask_restful import Resource, reqparse
from flask_jsonpify import jsonify
from flask import current_app, abort
from models.users import Users
import sys
import hashlib


class Auth(Resource):
    def post(self):
        salt = current_app.config["MD5_SALT"]
        parser = reqparse.RequestParser()
        parser.add_argument("login")
        parser.add_argument("password")
        params = parser.parse_args()
        salted_pass = hashlib.md5((salt + params['password']).encode('utf-8'))
        usr = Users.query.filter_by(login=params['login'], hashed_pass=salted_pass.hexdigest()).first()
        if usr is None:
            abort(401, description='Authorization failed')
        else:
            return jsonify({'salted': salted_pass.hexdigest()})
