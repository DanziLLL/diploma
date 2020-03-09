from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import yaml
import inv_auth
from json import dumps
#from flask.ext.jsonpify import jsonify


app = Flask(__name__)
api = Api(app)



def load_config():
    with open('config.yml') as f:
        yaml_data = f.read()
    f.close()
    return yaml.safe_load(yaml_data)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("")
        return {'employees': [i[0] for i in query.cursor.fetchall()]}


if __name__ == '__main__':
    conf = load_config()
    db_connect = create_engine("mysql+pymysql://{}:{}@mariadb:3306/".format(conf['mysql_user'], conf['mysql_password']))
    app.run(port='9000')
