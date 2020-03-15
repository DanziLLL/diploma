from main import db


class Cpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    physical_cores = db.Column(db.Integer, nullable=False)
    logical_cores = db.Column(db.Integer, nullable=False)
    linked_to = db.Column(db.String(10),  db.ForeignKey('computers.id'), nullable=False)

    def __init__(self, model, frequency, physical_cores, logical_cores, linked_to=None):
        self.model = model
        self.frequency = frequency
        self.physical_cores = physical_cores
        self.logical_cores = logical_cores
        self.linked_to = linked_to