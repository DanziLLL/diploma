from main import db
from config import Config
import hashlib


def create_db():
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
    from models.tasks import Tasks
    db.create_all()
    db.session.commit()


def create_admin():
    from models.users import Users
    salt = Config.MD5_SALT
    if Users.query.filter_by(login='admin').first() is None:
        try:
            salted_pass = hashlib.md5((salt + "a" + "a").encode('utf-8')).hexdigest()
            usr = Users(login='a', hashed_pass=salted_pass, access_level='admin')
            db.session.add(usr)
            salted_pass = hashlib.md5((salt + "u" + "u").encode('utf-8')).hexdigest()
            usr = Users(login='user1', hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            usr = Users(login='user2', hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            usr = Users(login='user3', hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            usr = Users(login='user4', hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            usr = Users(login='user5', hashed_pass=salted_pass, access_level='user')
            db.session.add(usr)
            db.session.commit()
        except:
            db.session.rollback()

