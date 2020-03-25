from flask_restful import Resource, reqparse,
from flask import current_app, jsonify, request

from datetime import datetime, timedelta
import hashlib

from models.users import Users
from models.tokens.session_tokens import SessionTokens
from models.assets.computer import Computer
from main import db


class ComputerApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("data")
        params = parser.parse_args()
        api_tok = None
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid'] and v['access_level'] == 'admin':



    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("inventory_id")
        params = parser.parse_args()
        api_tok = None
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid'] and v['access_level'] == 'admin':
        return 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("inventory_id")
        params = parser.parse_args()
        api_tok = None
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
            v = SessionTokens.is_valid_token(api_tok)
        else:
            response = jsonify({'status': 'err'})
            response.status_code = 401
            return response
        if v['valid'] and v['access_level'] == 'admin':
            q = Computer.query.filter(inventory_id=params['inventory_id']).first()
            q.delete()
            db.session.commit()
            current_app.logger.info('Deleted computer {}, inventory id {}'.format(q.hostname, q.inventory_id))
            response = jsonify({'status': 'ok'})
            response.status_code = 200
            return response
        elif not v['valid']:
            response = jsonify({'status': 'err'})
            response.status_code = 401
            return response
        elif v['access_level'] != 'admin':
            response = jsonify({'status': 'err'})
            response.status_code = 403
            return response

        return 200

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("inventory_id")
        parser.add_argument("data")
        params = parser.parse_args()
        return 200

