from main import db


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(64), unique=True, nullable=False)
    body = db.Column(db.String(256), unique=True, nullable=False)
    status = db.Column(db.String(32), nullable=False)
    linked_to = db.Column(db.String(10), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer)

    def __init__(self, summary, body, status, linked_to, create_date, created_by):
        self.summary = summary
        self.body = body
        self.status = status
        self.linked_to = linked_to
        self.create_date = create_date
        self.created_by = created_by
