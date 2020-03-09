from flask_restful import Resource

class Auth(Resource):
    def __init__(self, dbconn, conf):
        self.dbconn = dbconn
        self.md5_salt = conf['md5_salt']

    def post(self):