from main import db


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
