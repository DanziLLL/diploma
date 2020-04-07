from main import db
import json


class Misc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distro = db.Column(db.String(32), nullable=False)
    version = db.Column(db.String(32), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    last_contacted = db.Column(db.DateTime,  nullable=True)
    employee = db.Column(db.String(10), nullable=True)
    linked_to = db.Column(db.String(10), nullable=False)

    def __init__(self, distro, version, last_updated, last_contacted, employee, linked_to=None):
        self.distro = distro
        self.version = version
        self.last_updated = last_updated
        self.last_contacted = last_contacted
        self.employee = employee
        self.linked_to = linked_to

    def to_dict(self):
        from models.assets.computer import Computer
        hostname = Computer.query.filter_by(id=self.linked_to).first().hostname
        data = {'os': {'distro': self.distro,
                       'version': self.version},
                'hostname': hostname}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
