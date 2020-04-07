from main import db
import json


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(256), nullable=False)
    model = db.Column(db.String(256), nullable=False)
    revision = db.Column(db.String(256), nullable=False)
    bios_version = db.Column(db.String(256), nullable=False)
    linked_to = db.Column(db.String(10), nullable=True)

    def __init__(self, manufacturer, model, revision, bios_version, linked_to=None):
        self.model = model
        self.manufacturer = manufacturer
        self.revision = revision
        self.bios_version = bios_version
        self.linked_to = linked_to

    def to_dict(self):
        data = {'bios_version': self.bios_version,
                'manufacturer': self.manufacturer,
                'model': self.model,
                'version': self.revision}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
