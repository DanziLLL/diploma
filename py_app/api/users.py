from flask_restful import Resource, reqparse, request
from flask import current_app, jsonify

from datetime import datetime, timedelta
import hashlib

from models.users import Users
from models.tokens.session_tokens import SessionTokens
from main import db


class Users(Resource):
    def post(self):
        return 200


class Password(Resource):
    def post(self):
        api_tok = None
        salt = current_app.config["MD5_SALT"]
        parser = reqparse.RequestParser()
        parser.add_argument("login")
        parser.add_argument("new_password")
        params = parser.parse_args()
        if params['new_password'] is None:
            response = jsonify({'status': 'err_no_new_password'})
            response.status_code = 400
            return response
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid'] and v['access_level'] == 'admin':
            if params['login'] is None:
                response = jsonify({'status': 'err_no_login'})
                response.status_code = 400
                return response
            usr = Users.query.filter_by(login=params['login'])
            if usr.first() is not None:
                new_salted_pass = hashlib.md5((salt + params['new_password'] + params['login']).encode('utf-8'))
                usr.update({'hashed_pass': new_salted_pass.hexdigest()})
                response = jsonify({'status': 'ok'})
                response.status_code = 200
                return response
        elif v['valid'] and v['access_level'] == 'user':
            user_login = Users.query.filter_by(id=v['user_id']).first().login
            new_salted_pass = hashlib.md5((salt + params['new_password'] + user_login).encode('utf-8'))
            Users.query.filter_by(id=v['user_id']).update({'hashed_pass': new_salted_pass.hexdigest()})
            response = jsonify({'status': 'ok'})
            response.status_code = 200
            return response


class Token(Resource):
    def get(self):
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
            v = SessionTokens.is_valid_token(api_tok)
            if v['valid']:
                response = jsonify({'access_level': v['access_level'],
                                    'user_id': v['user_id']})
                response.status_code = 200
            else:
                response = jsonify({'status': 'err_access_denied'})
                response.status_code = 403
        else:
            response = jsonify({'status': "err_no_token"})
            response.status_code = 400
        return response
