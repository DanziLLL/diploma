from main import db
from datetime import datetime


class SessionTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(120), nullable=False)
    access_level = db.Column(db.String(10), nullable=False)

    def __init__(self, token, expiry_date, user_id, access_level):
        self.token = token
        self.expiry_date = expiry_date
        self.user_id = user_id
        self.access_level = access_level

    @staticmethod
    def remove_expired_tokens():
        current_time = datetime.now()
        SessionTokens.query.filter(SessionTokens.expiry_date < current_time).delete()
        db.session.commit()

    @staticmethod
    def is_valid_token(token):
        q = SessionTokens.query.filter_by(token=token).first()
        if q is not None:
            return {'valid': True, 'access_level': q.access_level}
        else:
            return {'valid': False}