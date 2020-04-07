from main import db
import json


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.String(256), nullable=False)
    linked_to = db.Column(db.String(10), nullable=True)

    def __init__(self, device_id, model, size, linked_to=None):
        self.device_id = device_id
        self.model = model
        self.size = size
        self.linked_to = linked_to

    def to_dict(self):
        data = {self.device_id: {'model': self.model,
                                 'size': self.size}}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
