from flask_restful import Resource, reqparse
from flask import current_app, jsonify, request

from datetime import datetime

from models.tokens.session_tokens import SessionTokens
from models.tasks import Tasks

import json

from main import db


class TasksApi(Resource):
    def post(self):  # TODO: encryption, no api token
        parser = reqparse.RequestParser()
        parser.add_argument("summary")
        parser.add_argument("body")
        parser.add_argument("linked_to")
        params = parser.parse_args()
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        else:
            response = jsonify({'status': 'err_permission_denied'})
            response.status_code = 403
            return response
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid']:
            for i in params:
                if i is None:
                    response = jsonify({'status': 'err_arg_{}_missing'.format(i)})
                    response.status_code = 400
                    return response
            t = Tasks(params['summary'], params['body'], 'open', params['linked_to'], datetime.now(), v['user_id'])

            db.session.add(t)
            db.session.commit()
            response = jsonify({'status': 'ok'})
            response.status_code = 200
            return response
        elif not v['valid']:
            response = jsonify({'status': 'err_invalid_token'})
            response.status_code = 401
            return response

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("all")
        parser.add_argument("computer_id")
        params = parser.parse_args()
        api_tok = None
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        else:
            response = jsonify({'status': 'err_permission_denied'})
            response.status_code = 403
            return response
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid'] and v['access_level'] == 'admin':
            if params['id'] is not None:
                q = Tasks.query.filter_by(id=params['id']).filter_by(status='open').first()
                if q is not None:
                    response = jsonify({'summary': q.summary, 'body': q.body, 'linked_to': q.linked_to,
                                        'create_date': q.create_date, 'created_by': q.created_by})
                    response.status_code = 200
                    return response
                else:
                    response = jsonify({'status': 'err_not_found'})
                    response.status_code = 404
                    return response
            elif params['all'] is not None:
                q = Tasks.query.all()
                if q is not None:
                    data = {}
                    for i in q:
                        data[i.id] = {'summary': i.summary, 'body': i.body, 'linked_to': i.linked_to,
                                      'create_date': str(i.create_date), 'created_by': i.created_by}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
            elif params['computer_id'] is not None:
                q = Tasks.query.filter_by(linked_to=params['computer_id']).filter_by(status='open').all()
                if q is not None:
                    data = {}
                    for i in q:
                        data[i.id] = {'summary': i.summary, 'body': i.body, 'linked_to': i.linked_to,
                                      'create_date': str(i.create_date), 'created_by': i.created_by}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
        elif not v['valid']:
            response = jsonify({'status': 'err_invalid_token'})
            response.status_code = 401
            return response
        elif v['access_level'] != 'admin':
            response = jsonify({'status': 'err_permission_denied'})
            response.status_code = 403
            return response

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        params = parser.parse_args()
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
            v = SessionTokens.is_valid_token(api_tok)
        else:
            response = jsonify({'status': 'err_no_token'})
            response.status_code = 401
            return response
        if v['valid'] and v['access_level'] == 'admin':
            q = Tasks.query.filter_by(id=params['id']).delete()
            current_app.logger.info('Deleted task id {}'.format(params['id']))
            response = jsonify({'status': 'ok_deleted'})
            response.status_code = 200
            return response
        elif not v['valid']:
            response = jsonify({'status': 'err_invalid_token'})
            response.status_code = 401
            return response
        elif v['access_level'] != 'admin':
            response = jsonify({'status': 'err_permission_denied'})
            response.status_code = 403
            return response

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("status")
        params = parser.parse_args()
        for k, v in params.items():
            if v is None:
                response = jsonify({'status': 'err_args_missing'})
                response.status_code = 400
                return response
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
            v = SessionTokens.is_valid_token(api_tok)
        else:
            response = jsonify({'status': 'err_no_token'})
            response.status_code = 401
            return response
        if v['valid'] and v['access_level'] == 'admin':
            q = Tasks.query.filter_by(id=params['id'])
            if q.first() is None:
                response = jsonify({'status': 'err_not_found'})
                response.status_code = 404
                return response
            else:
                q.update({'status': params['status']})
                current_app.logger.info('Updated task id {}, changed status to {}'.format(params['id'], params['status']))
                response = jsonify({'status': 'ok_updated'})
                response.status_code = 200
            return response
        elif not v['valid']:
            response = jsonify({'status': 'err_invalid_token'})
            response.status_code = 401
            return response
        elif v['access_level'] != 'admin':
            response = jsonify({'status': 'err_permission_denied'})
            response.status_code = 403
            return response
