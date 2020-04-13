from main import db


class Peripherals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(256), nullable=False)
    model = db.Column(db.DateTime, nullable=False)
    inventory_id = db.Column(db.String(10), nullable=False)
    linked_to = db.Column(db.String(10), nullable=True)

    def __init__(self, type, model, inventory_id, linked_to=None):
        self.type = type
        self.model = model
        self.inventory_id = inventory_id
        self.linked_to = linked_to
