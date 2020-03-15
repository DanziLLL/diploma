from main import db
from datetime import datetime


class SessionTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(256))
    hostname = db.Column(db.String(256), unique=True, nullable=False)
    cpu = db.Column(db.DateTime, nullable=False)
    ram = db.Column(db.String(120), db.ForeignKey('users.id'), nullable=False)
    hdd = db.Column(db.String(10), nullable=False)
    ip = db.Column(db.String(16), nullable=True)
    inventory_id = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, token, expiry_date, user_id, access_level):
        self.token = token
        self.expiry_date = expiry_date
        self.user_id = user_id
        self.access_level = access_level

    def __repr__(self):
        return '<Token %r>' % self.login

    @staticmethod
    def remove_expired_tokens():
        current_time = datetime.now()
        SessionTokens.query.filter(SessionTokens.expiry_date < current_time).delete()
        db.session.commit()
