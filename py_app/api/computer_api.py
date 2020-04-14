from flask_restful import Resource, reqparse
from flask import current_app, jsonify, request

from datetime import datetime
import json
import qrcode
from io import BytesIO
import base64

from models.tokens.session_tokens import SessionTokens
from models.assets.computer import Computer
from models.assets.computer_items.cpu import Cpu
from models.assets.computer_items.misc import Misc
from models.assets.computer_items.platform import Platform
from models.assets.computer_items.ram import Ram
from models.assets.computer_items.storage import Storage
from models.assets.computer_items.video import Video
from models.assets.computer_items.network import Network
from models.changelog import Changelog

from main import db


class ComputerApi(Resource):
    def post(self):  # TODO: encryption, no api token
        parser = reqparse.RequestParser()
        parser.add_argument("data")
        params = parser.parse_args()
        computer_id = None
        item_data = json.loads(params['data'].replace('\'', '"'))  # workaround for nested jsons
        hostname = item_data['misc']['hostname']
        entry_exists = Computer.query.filter_by(hostname=hostname).first() is not None
        if hostname != 'localhost' and not entry_exists:
            # creating computer entry
            computer_entry = Computer(hostname=item_data['misc']['hostname'], inventory_id='invapp_c_{}'.format(hostname))
            db.session.add(computer_entry)
            db.session.commit()
            computer_id = Computer.query.filter_by(hostname=item_data['misc']['hostname']).first().id
        if computer_id is not None:

            # CPU SECTION ### MO MULTICPU CONFIGURATIONS SUPPORTED YET ###
            cpu = item_data['cpu']
            cpu_entry = Cpu(cpu['model'], cpu['frequency'], cpu['physical_cores'], cpu['logical_cores'], computer_id)
            db.session.add(cpu_entry)
            # PLATFORM SECTION
            platform = item_data['platform']
            platform_entry = Platform(platform['manufacturer'], platform['model'],
                                      platform['version'], platform['bios_version'], computer_id)
            db.session.add(platform_entry)
            # RAM SECTION
            for k, v in item_data['ram'].items():
                ram_entry = Ram(v['manufacturer'], v['model'], v['size'], k, computer_id)
                db.session.add(ram_entry)
            # VIDEO SECTION
            video_entry = Video(item_data['video']['model'], computer_id)
            db.session.add(video_entry)
            # STORAGE SECTION
            for k, v in item_data['storage'].items():
                storage_entry = Storage(k, v['model'], v['size'], computer_id)
                db.session.add(storage_entry)
            # NETWORK SECTION
            for k, v in item_data['network'].items():
                network_entry = Network(k, v['ip'], v['mac'], computer_id)
                db.session.add(network_entry)
            # MISC SECTION:
            misc = item_data['misc']
            misc_entry = Misc(misc['os']['distro'], misc['os']['version'], datetime.now(),
                              datetime.now(), "", computer_id)
            db.session.add(misc_entry)
            db.session.commit()
            # RESPONSE
            response = jsonify({'status': 'created'})
            response.status_code = 200
            return response
        elif entry_exists:
            computer_id = Computer.query.filter_by(hostname=hostname).first().id
            new = item_data
            old = Computer.get_full_dict(computer_id=computer_id)
            changes = Computer.get_diff(new, old)
            for ch in changes:  # tuple (type_of_change, item, change)
                current_app.logger.info(ch)
                Computer.process_changes(ch, computer_id)
            response = jsonify({'status': 'updated'})
            response.status_code = 200
            return response

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("inventory_id")
        parser.add_argument("computer_id")
        parser.add_argument("all")
        data = {}
        params = parser.parse_args()
        api_tok = None
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
        v = SessionTokens.is_valid_token(api_tok)
        if v['valid'] and v['access_level'] == 'admin':
            if params['inventory_id'] is not None:
                q = Computer.query.filter_by(inventory_id=params['inventory_id']).first()
                if q is None:
                    response = jsonify({'status': 'err_not_found'})
                    response.status_code = 404
                    return response
                data = Computer.get_full_dict(q.id)
                data['id'] = q.id
            elif params['computer_id'] is not None:
                q = Computer.query.filter_by(id=params['computer_id']).first()
                if q is None:
                    response = jsonify({'status': 'err_not_found'})
                    response.status_code = 404
                    return response
                data = Computer.get_full_dict(computer_id=params['computer_id'])
            elif params['all'] is not None:
                q = Computer.query.all()
                data = {}
                for i in q:
                    data[i.id] = Computer.get_full_dict(computer_id=i.id)
            response = jsonify(data)
            response.status_code = 200
            return response
        elif v['valid'] and v['access_level'] == 'user':
            q = Computer.query.filter_by(inventory_id=params['inventory_id']).first()
            if q is None:
                response = jsonify({'status': 'err_not_found'})
                response.status_code = 404
                return response
            else:
                data = {'id': q.id}
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
        parser.add_argument("inventory_id")
        params = parser.parse_args()
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
            v = SessionTokens.is_valid_token(api_tok)
        else:
            response = jsonify({'status': 'err_no_token'})
            response.status_code = 401
            return response
        if v['valid'] and v['access_level'] == 'admin':
            q = Computer.query.filter_by(inventory_id=params['inventory_id'])
            delete_id = q.first().id
            Computer.delete_all(delete_id)
            current_app.logger.info('Deleted computer {}, inventory id {}'.format(params['inventory_id'], delete_id))
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


class Changes(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("computer_id")
        params = parser.parse_args()
        if 'api_token' in request.cookies:
            api_tok = request.cookies.get('api_token')
            v = SessionTokens.is_valid_token(api_tok)
        else:
            response = jsonify({'status': 'err_no_token'})
            response.status_code = 401
            return response
        if v['valid'] and v['access_level'] == 'admin':
            q = Changelog.query.filter_by(linked_to=params['computer_id']).all()
            data = {}
            for i in q:
                data[i.id] = {'change': i.entry_type, 'data': i.entry}
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


class QRCode(Resource):
    def get(self):
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
            inv_id = Computer.query.filter_by(id=params['id']).first().inventory_id
            buffered = BytesIO()
            qrcode.make(inv_id).save(buffered, format="PNG")
            b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            response = jsonify({'status': 'ok',
                                'code': b64})
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