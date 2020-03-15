from main import db


class Ram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    linked_to = db.Column(db.String(10),  db.ForeignKey('computers.id'), nullable=True)

    def __init__(self, model, size, linked_to=None):
        self.model = model
        self.size = size
        self.linked_to = linked_to
