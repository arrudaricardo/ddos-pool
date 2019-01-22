from app import db
from datetime import datetime


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    target_address = db.Column(db.String(128), index=True, unique=True)
    attack_type = db.Column(db.String(64), index=True, unique=False)
    transport_layer = db.Column(db.String(128), index=True, unique=True)
    port = db.Column(db.Integer(), index=True, unique=False)
    attack_message = db.Column(db.String(128), index=True, unique=True, default=None)
    comment = db.Column(db.String(140), index=True, unique=False)
    rpm = db.Column(db.Integer(), index=True, unique=False, default=None)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    number_attackers = db.Column(db.Integer(), index=True, unique=False, default=None)

    def __repr__(self):
        return f'{self.id}, {self.name}'


def init_test():
    db.create_all()
    u = Pool(name='DDos google', target_address='http://www.google.com',
     port=80, transport_layer='TCP', attack_type='DDOS', comment='Lets DDos google',
     attack_message='test')
    db.session.add(u)
    db.session.commit()

    u = Pool(name='DDos yahoo', target_address='http://www.yahoo.com',
     port=80, transport_layer='TCP', attack_type='DDOS', comment='Lets DDos yahoo',
     attack_message='test')
    db.session.add(u)
    db.session.commit()
