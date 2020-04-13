from main import db
from datetime import datetime, timedelta


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
        q = SessionTokens.query.filter(SessionTokens.expiry_date < current_time)
        ids = []
        if q.first is not None:
            for i in q.all():
                ids.append(i.id)
        for i in ids:
            try:
                SessionTokens.query.filter_by(id=i).delete()
                db.session.commit()
            except:
                db.session.rollback()
        return

    @staticmethod
    def is_valid_token(token):
        q = SessionTokens.query.filter_by(token=token)
        tok = q.first()
        if tok is not None:
            q.update({'expiry_date': datetime.now() + timedelta(minutes=30)})
            db.session.commit()
            return {'valid': True, 'access_level': tok.access_level, 'user_id': tok.user_id}
        else:
            return {'valid': False}
