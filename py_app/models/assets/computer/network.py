from main import db


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    ip = db.Column(db.String(16), nullable=True)
    linked_to = db.Column(db.String(10),  db.ForeignKey('computers.id'), nullable=True)

    def __init__(self, model, inventory_id, ip, linked_to=None):
        self.model = model
        self.inventory_id = inventory_id
        self.ip = ip
        self.linked_to = linked_to