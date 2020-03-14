from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@mariadb/inventory_app'.format(app.config['MYSQL_USER'],
                                                                                     app.config['MYSQL_PASSWORD'])
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    from inv.auth import Auth
    api = Api(app)
    api.add_resource(Auth, "/api/auth", "/api/auth/")
    app.run(host='0.0.0.0', port='9000')


