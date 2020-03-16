from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from logging.config import dictConfig
import atexit


app = Flask(__name__)
app.config.from_object(Config)
app.config.update(
    {'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://{}:{}@mariadb/inventory_app'.
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


if __name__ == '__main__':
    create_logger()

    create_api()

    from cron import create_cron
    cron = create_cron()
    cron.start()
    atexit.register(lambda: cron.shutdown())

    app.run(host='0.0.0.0', port='9000')


