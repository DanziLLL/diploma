from main import db
import datetime


class SessionTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey('users.id'), nullable=False)
    access_level = db.Column(db.String(10), nullable=False)

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
        expired = SessionTokens.query.filter_by(SessionTokens.expiry_date < current_time).all()
        db.session.remove(expired)
        db.session.commit()
