from main import db
import json


class Cpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    physical_cores = db.Column(db.Integer, nullable=False)
    logical_cores = db.Column(db.Integer, nullable=False)
    linked_to = db.Column(db.String(10), nullable=False)

    def __init__(self, model, frequency, physical_cores, logical_cores, linked_to=None):
        self.model = model
        self.frequency = frequency
        self.physical_cores = physical_cores
        self.logical_cores = logical_cores
        self.linked_to = linked_to

    def to_dict(self):
        data = {'model': self.model,
                'frequency': self.frequency,
                'physical_cores': self.physical_cores,
                'logical_cores': self.logical_cores}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())
