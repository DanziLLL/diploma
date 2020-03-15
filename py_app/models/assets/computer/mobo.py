from main import db


class Mobo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    revision = db.Column(db.String(10), nullable=False)
    bios_version = db.Column(db.String(10), nullable=False)
    linked_to = db.Column(db.String(10),  db.ForeignKey('computers.id'), nullable=True)

    def __init__(self, model, revision, bios_version, linked_to=None):
        self.model = model
        self.revision = revision
        self.bios_version = bios_version
        self.linked_to = linked_to
