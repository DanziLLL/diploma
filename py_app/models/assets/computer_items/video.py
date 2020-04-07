from main import db
import json


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    linked_to = db.Column(db.String(10), nullable=True)

    def __init__(self, model, linked_to=None):
        self.model = model
        self.linked_to = linked_to

    def to_dict(self):
        return {'model': self.model}

    def to_json(self):
        return json.dumps(self.to_dict())
