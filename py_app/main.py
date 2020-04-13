from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from logging.config import dictConfig
import atexit


app = Flask(__name__)
app.config.from_object(Config)
# app.config['SQLALCHEMY_ECHO'] = True
app.config['JSON_SORT_KEYS'] = False
app.config.update(
    {'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://{}:{}@mysql/inventory_app'.
        format(app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'])})
db = SQLAlchemy(app)


def create_logger():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })


@app.route('/')
def index():
    return "Hello, World!"


def create_api():
    api = Api(app)
    from api.auth import Auth
    api.add_resource(Auth, "/api/auth", "/api/auth/")
    from api.register import Register
    api.add_resource(Register, "/api/register", "/api/register/")
    from api.computer_api import ComputerApi
    api.add_resource(ComputerApi, "/api/computer", "/api/computer/")
    from api.users import Password
    api.add_resource(Password, "/api/users/password", "/api/users/password/")
    from api.users import Token
    api.add_resource(Token, "/api/validate_token", "/api/validate_token/")
    from api.computer_api import Changes
    api.add_resource(Changes, "/api/computer/changes", "/api/computer/changes/")
    from api.tasks import TasksApi
    api.add_resource(TasksApi, "/api/tasks", "/api/tasks/")
    from api.computer_api import QRCode
    api.add_resource(QRCode, "/api/computer/qrcode", "/api/computer/qrcode/")
    from api.users import Users_api
    api.add_resource(Users_api, "/api/users", "/api/users/")


if __name__ == '__main__':
    create_logger()

    create_api()

    from db import create_db
    create_db()

    from db import create_admin
    create_admin()

    from cron import create_cron
    cron = create_cron()
    cron.start()
    atexit.register(lambda: cron.shutdown())

    app.run(host='0.0.0.0', port='9000')


