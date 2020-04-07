from main import db
import json


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interface = db.Column(db.String(256), nullable=False)
    ip = db.Column(db.String(16), nullable=True)
    mac = db.Column(db.String(20), nullable=True)
    linked_to = db.Column(db.String(10), nullable=True)

    def __init__(self, interface, ip, mac, linked_to=None):
        self.interface = interface
        self.ip = ip
        self.mac = mac
        self.linked_to = linked_to

    def to_dict(self):
        data = {self.interface: {'ip': self.ip,
                                 'mac': self.mac}}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
