from main import db
from datetime import datetime


class RegistrationTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, expiry_date):
        self.token = token
        self.expiry_date = expiry_date

    def __repr__(self):
        return '<Token %r>' % self.login

    @staticmethod
    def remove_expired_tokens():
        current_time = datetime.now()
        RegistrationTokens.query.filter(RegistrationTokens.expiry_date < current_time).delete()
        db.session.commit()

    @staticmethod
    def is_valid_token(token):
        q = RegistrationTokens.query.filter_by(token=token).first()
        if q is not None:
            return True
        else:
            return False
