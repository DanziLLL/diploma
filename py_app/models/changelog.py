from main import db


class Changelog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_type = db.Column(db.String(256), nullable=False)
    entry = db.Column(db.String(256), nullable=False)
    linked_to = db.Integer()

    def __init__(self, entry_type, entry, linked_to=None):
        self.entry_type = entry_type
        self.entry = entry
        self.linked_to = linked_to
