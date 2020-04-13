from main import db
from dictdiffer import diff

from models.assets.computer_items.cpu import Cpu
from models.assets.computer_items.misc import Misc
from models.assets.computer_items.platform import Platform
from models.assets.computer_items.ram import Ram
from models.assets.computer_items.storage import Storage
from models.assets.computer_items.video import Video
from models.assets.computer_items.network import Network
from models.changelog import Changelog

from flask import current_app


class Computer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(256), unique=True, nullable=False)
    inventory_id = db.Column(db.String(64), nullable=False)

    def __init__(self, hostname, inventory_id):
        self.hostname = hostname
        self.inventory_id = inventory_id

    @staticmethod
    def process_changes(ch, computer_id):
        path = ch[1].split('.')
        if ch[0] == 'change':
            f = {path[-1]: ch[2][0], 'linked_to': computer_id}  # creating query filter
            if path[0] == 'cpu':
                q = Cpu.query.filter_by(**f)
            elif path[0] == 'ram':
                q = Ram.query.filter_by(**f)
            elif path[0] == 'misc':
                q = Misc.query.filter_by(**f)
            elif path[0] == 'storage':
                q = Storage.query.filter_by(**f)
            elif path[0] == 'network':
                q = Network.query.filter_by(**f)
            elif path[0] == 'platform':
                q = Platform.query.filter_by(**f)
            elif path[0] == 'video':
                q = Video.query.filter_by(**f)
            q.update({path[-1]: ch[2][1]})
            log = Changelog(ch[0], "{}: {} to {}".format(path, ch[2][0], ch[2][1]), computer_id)
            
            db.session.add(log)
            db.session.commit()
            current_app.logger.info("UPDATED")
            return
        elif ch[0] == 'add':
            if path[0] == 'ram':
                q = Ram(ch[2][0][1]['manufacturer'], ch[2][0][1]['model'],
                        ch[2][0][1]['size'], ch[2][0][0], computer_id)
            elif path[0] == 'storage':
                q = Storage(ch[2][0][0], ch[2][0][1]['model'], ch[2][0][1]['size'], computer_id)
            elif path[0] == 'network':
                current_app.logger.info(ch[2][0][0])
                q = Network(ch[2][0][0], ch[2][0][1]['ip'], ch[2][0][1]['mac'], computer_id)
            
            db.session.add(q)
            log = Changelog(ch[0], "{}".format(ch[2][0]), computer_id)
            db.session.add(log)
            db.session.commit()
        elif ch[0] == 'remove':
            f = {'linked_to': computer_id}
            if path[0] == 'ram':
                f['slot'] = ch[2][0][0]
                q = Ram.query.filter_by(**f)
            # elif path[0] == 'misc':
            #     f['slot'] = ch[2][0]
            #     q = Misc.query.filter_by(**f)
            elif path[0] == 'storage':
                f['device_id'] = ch[2][0][0]
                q = Storage.query.filter_by(**f)
            elif path[0] == 'network':
                f['interface'] = ch[2][0][0]
                q = Network.query.filter_by(**f)
            q.delete()
            log = Changelog(ch[0], "{}".format(ch[2][0]), computer_id)
            
            db.session.add(log)
            db.session.commit()
            return

    @staticmethod
    def get_diff(new, old):
        return list(diff(old, new))

    @staticmethod
    def get_full_sql(computer_id=None, hostname=None):
        if hostname is not None:
            computer_id = Computer.query.filter_by(hostname=hostname).first().id
        cpu = Cpu.query.filter_by(linked_to=computer_id).all()
        misc = Misc.query.filter_by(linked_to=computer_id).all()
        ram = Ram.query.filter_by(linked_to=computer_id).all()
        platform = Platform.query.filter_by(linked_to=computer_id).all()
        storage = Storage.query.filter_by(linked_to=computer_id).all()
        video = Video.query.filter_by(linked_to=computer_id).all()
        network = Network.query.filter_by(linked_to=computer_id).all()

        return {'cpu': cpu, 'ram': ram, 'platform': platform, 'video': video,
                'misc': misc, 'storage': storage, 'network': network}

    @staticmethod
    def delete_all(computer_id=None, hostname=None):
        if hostname is not None:
            computer_id = Computer.query.filter_by(hostname=hostname).first().id
        Cpu.query.filter_by(linked_to=computer_id).delete()
        Misc.query.filter_by(linked_to=computer_id).delete()
        Ram.query.filter_by(linked_to=computer_id).delete()
        Platform.query.filter_by(linked_to=computer_id).delete()
        Storage.query.filter_by(linked_to=computer_id).delete()
        Video.query.filter_by(linked_to=computer_id).delete()
        Network.query.filter_by(linked_to=computer_id).delete()
        Changelog.query.filter_by(linked_to=computer_id).delete()
        Computer.query.filter_by(id=computer_id).delete()

    @staticmethod
    def get_full_dict(computer_id):
        old = {}
        data = Computer.get_full_sql(computer_id=computer_id)
        for k, v in data.items():
            if isinstance(v, list):
                old[k] = {}
                for i in v:
                    for k1, v1 in i.to_dict().items():
                        old[k][k1] = v1
            else:
                old[k] = v.to_dict()
        return old
