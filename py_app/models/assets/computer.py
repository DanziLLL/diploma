from main import db


class Computer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(256), unique=True, nullable=False)
    inventory_id = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, token, expiry_date, user_id, access_level):
        self.token = token
        self.expiry_date = expiry_date
        self.user_id = user_id
        self.access_level = access_level
