from flask_restful import Resource, reqparse
from flask import current_app, jsonify

from datetime import datetime, timedelta
import hashlib

from models.users import Users
from models.tokens.session_tokens import SessionTokens
from main import db


class Auth(Resource):
    def post(self):
        salt = current_app.config["MD5_SALT"]
        parser = reqparse.RequestParser()
        parser.add_argument("login")
        parser.add_argument("password")
        params = parser.parse_args()
        salted_pass = hashlib.md5((salt + params['password'] + params['login']).encode('utf-8'))
        usr = Users.query.filter_by(login=params['login'], hashed_pass=salted_pass.hexdigest()).first()
        if usr is None:
            current_app.logger.info('Authorization failed for user {}'.format(params['login']))
            response = jsonify({'status': 'Authorization failed'})
            response.status_code = 401
            return response
        else:
            token = hashlib.md5((datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                 + salted_pass.hexdigest()).encode('utf-8')).hexdigest()
            expiry = datetime.now() + timedelta(minutes=30)
            entry = SessionTokens(token, expiry, usr.id, usr.access_level)
            db.session.add(entry)
            db.session.commit()
            current_app.logger.info('User {} logged in'.format(params['login']))
            response = jsonify({'status': 'ok'})
            response.set_cookie('api_token', value=token)
            response.status_code = 200
            return response


