from flask_restful import Resource, reqparse
from flask import current_app, request, jsonify

from datetime import datetime, timedelta
import hashlib

from models.users import Users
from models.tokens.session_tokens import SessionTokens
from models.tokens.registration_tokens import RegistrationTokens
from main import db


class Register(Resource):
    def post(self):
        salt = current_app.config["MD5_SALT"]
        parser = reqparse.RequestParser()
        parser.add_argument("login")
        parser.add_argument("password")
        parser.add_argument("token")
        params = parser.parse_args()
        current_app.logger.info('Salt = {}, password = {}, params = '.format(salt, params['password'], params))
        salted_pass = hashlib.md5((salt + params['password'] + params['login']).encode('utf-8')).hexdigest()
        valid = RegistrationTokens.is_valid_token(params['token'])
        exist = Users.query.filter(Users.login == params['login']).first()
        if valid and exist is None:
            usr = Users(login=params['login'], hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            db.session.commit()
            current_app.logger.info('Created user {}'.format(params['login']))
            RegistrationTokens.query.filter(RegistrationTokens.token == params['token']).delete()
            response = jsonify({'status': 'ok', 'user': params['login']})
            response.status_code = 200
            return response
        elif valid and exist is not None:
            response = jsonify({'status': 'err_already_exists'})
            response.status_code = 400
            return response
        elif not valid:
            response = jsonify({'status': 'err_auth_failed'})
            response.status_code = 403
            return response

    def get(self):
        api_tok = None
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid'] and v['access_level'] == 'admin':
            reg_tok = hashlib.md5((datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                   + api_tok).encode('utf-8')).hexdigest()
            entry = RegistrationTokens(token=reg_tok, expiry_date=(datetime.now() + timedelta(days=1)))

            db.session.add(entry)
            db.session.commit()
            response = jsonify({'registration_token': reg_tok})
            response.status_code = 200
            return response
        else:
            response = jsonify({'status': 'err_auth_failed'})
            response.status_code = 403
            return response
