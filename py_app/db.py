from main import db
from config import Config
import hashlib


def create_db():
    salt = Config.MD5_SALT
    from models.users import Users
    from models.assets.computer import Computer
    from models.assets.computer_items.cpu import Cpu
    from models.assets.computer_items.misc import Misc
    from models.assets.computer_items.platform import Platform
    from models.assets.computer_items.ram import Ram
    from models.assets.computer_items.storage import Storage
    from models.assets.computer_items.video import Video
    from models.assets.computer_items.network import Network
    from models.tokens.registration_tokens import RegistrationTokens
    from models.tokens.session_tokens import SessionTokens
    from models.changelog import Changelog
    salted_pass = hashlib.md5((salt + "admin" + "admin").encode('utf-8')).hexdigest()
    db.create_all()
    db.session.commit()
    if Users.query.filter_by(login='admin').first() is None:
        usr = Users(login='admin', hashed_pass=salted_pass, access_level='admin')
        db.session.add(usr)
        db.session.commit()

