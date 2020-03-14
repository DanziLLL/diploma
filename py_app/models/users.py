from main import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    hashed_pass = db.Column(db.String(120), unique=True, nullable=False)
    access_level = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login
