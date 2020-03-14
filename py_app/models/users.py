from main import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True, nullable=False)
    hashed_pass = db.Column(db.String(128), unique=True, nullable=False)
    access_level = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login
