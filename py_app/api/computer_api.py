from flask_restful import Resource, reqparse
from flask import current_app, jsonify, request

from datetime import datetime, timedelta
import hashlib
import json

from models.users import Users
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
            computer_entry = Computer(hostname=item_data['misc']['hostname'], inventory_id='not_assign')
            db.session.add(computer_entry)
            db.session.commit()
            computer_id = computer_entry.id
        if computer_id is not None:
            # CPU SECTION ### MO MULTICPU CONFIGURATIONS SUPPORTED YET ###
            cpu = item_data['cpu']
            cpu_entry = Cpu(cpu['model'], cpu['frequency'], cpu['physical_cores'], cpu['logical_cores'], computer_id)
            db.session.add(cpu_entry)
            db.session.commit()
            # PLATFORM SECTION
            platform = item_data['platform']
            platform_entry = Platform(platform['manufacturer'], platform['model'],
                                      platform['version'], platform['bios_version'], computer_id)
            db.session.add(platform_entry)
            db.session.commit()
            # RAM SECTION
            for k, v in item_data['ram'].items():
                ram_entry = Ram(v['manufacturer'], v['model'], v['size'], k, computer_id)
                db.session.add(ram_entry)
                db.session.commit()
            # VIDEO SECTION
            video_entry = Video(item_data['video']['model'], computer_id)
            db.session.add(video_entry)
            db.session.commit()
            # STORAGE SECTION
            for k, v in item_data['storage'].items():
                storage_entry = Storage(k, v['model'], v['size'], computer_id)
                db.session.add(storage_entry)
                db.session.commit()
            # NETWORK SECTION
            for k, v in item_data['network'].items():
                network_entry = Network(k, v['ip'], v['mac'], computer_id)
                db.session.add(network_entry)
                db.session.commit()
            # MISC SECTION:
            misc = item_data['misc']
            misc_entry = Misc(misc['os']['distro'], misc['os']['version'], datetime.now(),
                              datetime.now(), "", computer_id)
            db.session.add(misc_entry)
            db.session.commit()
            response = jsonify({'status': 'created'})
            response.status_code = 200
            return response
        elif entry_exists:
            computer_id = Computer.query.filter_by(hostname=hostname).first().id
            new = item_data
            old = {}
            data = Computer.get_full_sql(computer_id=computer_id)
            for k, v in data.items():
                if isinstance(v, list):
                    old[k] = {}
                    for i in v:
                        for k1, v1 in i.to_dict().items():
                            old[k][k1] = v1
                else:
                    old[k] = v.to_dict()
            changes = Computer.get_diff(json.loads(json.dumps(new, sort_keys=True)),
                                        json.loads(json.dumps(old, sort_keys=True)))
            for ch in changes:  # tuple (type_of_change, item, change)
                current_app.logger.info(ch)
                Computer.process_changes(ch, computer_id)
            response = jsonify({'status': 'updated'})
            response.status_code = 200
            return response






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
            for i in Computer.get_full_sql(computer_id=q.id):
                if isinstance(i, list):
                    for it in i:
                        it.delete()
                else:
                    i.delete()
            for i in Changelog.query.filter_by(linked_to=q.id):
                i.delete()
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

# {"cpu": {"model": "Intel(R) Core(TM) i7-8550U CPU", "frequency": 1800, "physical_cores": 4, "logical_cores": 8}, "ram": {"ChannelA-DIMM0": {"size": "8192 MB", "manufacturer": "Samsung", "model": "M471A1K43CB1-CRC"}, "ChannelB-DIMM0": {"size": "8192 MB", "manufacturer": "Micron", "model": "8ATF1G64HZ-2G3E1"}}, "video": {"model": "Intel Corporation UHD Graphics 620 (rev 07)"}, "storage": {"nvme0n1": {"model": "INTEL SSDPEKKF512G8L", "size": "476 GB"}}, "platform": {"bios_version": "R0RET31W (1.14 )", "manufacturer": "LENOVO", "model": "20M50011RT", "version": "SDK0J40697 WIN"}, "network": {"wlp2s0": {"ip": "192.168.88.216", "mac": "fc:77:74:1d:14:e2"}, "virbr0": {"ip": "192.168.122.1", "mac": "52:54:00:f1:64:1e"}, "docker0": {"ip": "172.17.0.1", "mac": "02:42:84:92:c3:09"}, "br-c92de87aff0d": {"ip": "172.18.0.1", "mac": "02:42:db:a4:68:b6"}}, "misc": {"os": {"distro": "Fedora", "version": "31"}}}