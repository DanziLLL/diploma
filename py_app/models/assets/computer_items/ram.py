from main import db
import json


class Ram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(256), nullable=False)
    model = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    slot = db.Column(db.String(256), nullable=False)
    linked_to = db.Column(db.String(10), nullable=True)

    def __init__(self, manufacturer, model, size, slot, linked_to=None):
        self.model = model
        self.manufacturer = manufacturer
        self.slot = slot
        self.size = size
        self.linked_to = linked_to

    def to_dict(self):
        data = {self.slot: {'size': self.size,
                            'manufacturer': self.manufacturer,
                            'model': self.model}}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
