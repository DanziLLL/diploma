from main import db


def create_db():
    from models.assets.computer import Computer
    from models.assets.computer_items.cpu import Cpu
    from models.assets.computer_items.misc import Misc
    from models.assets.computer_items.platform import Platform
    from models.assets.computer_items.ram import Ram
    from models.assets.computer_items.storage import Storage
    from models.assets.computer_items.video import Video
    from models.assets.computer_items.network import Network
    from models.changelog import Changelog
    db.create_all()
    db.session.commit()
