from flask_restful import Resource, reqparse
from flask import current_app, abort, request

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
        salted_pass = hashlib.md5((salt + params['password']).encode('utf-8')).hexdigest()
        valid = RegistrationTokens.is_valid_token(params['token'])
        exist = Users.query.filter(Users.login == params['login']).first()
        if valid and exist is None:
            usr = Users(login=params['login'], hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            db.session.commit()
            current_app.logger.info('Created user {}'.format(params['login']))
            RegistrationTokens.query.filter(RegistrationTokens.token == params['token']).delete()
            db.session.commit()
            return 200, {'status': 'ok', 'user': params['login']}
        elif valid and exist is not None:
            return 400, {'status': 'err_already_exists'}
        elif not valid:
            abort(403, description='Authorization failed')

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
            return 200, {'registration_token': reg_tok}
        else:
            abort(403, description='Authorization failed')
