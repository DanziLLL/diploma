from main import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256), nullable=False)
    vram_size = db.Column(db.String(10), nullable=False)
    linked_to = db.Column(db.String(10),  db.ForeignKey('computers.id'), nullable=True)

    def __init__(self, model, vram_size, linked_to=None):
        self.model = model
        self.vram_size = vram_size
        self.linked_to = linked_to
