# -*- coding: utf-8 -*-
from fcloud_api import db
import datetime

class History(db.Model):
    __tablename__ = 'history'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    action = db.Column(db.String(80))
    action_object = db.Column(db.String(80))
    object_id = db.Column(db.String(80))
    result = db.Column(db.String(80))
    detail = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<History %s>' % self.id


class Flavor(db.Model):
    __tablename__ = 'flavor'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cpu = db.Column(db.Integer)
    mem = db.Column(db.Integer)
    disk = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '%sCPU_%sGRAM_%sGDISK' % (self.cpu, self.mem, self.disk)



"""
class Apps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(80), unique=True)
    tasks = db.relationship('Tasks', backref='apps',
                                lazy='dynamic')
    create_by = db.Column(db.String(80))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<App %s>' % self.app_id
"""


if __name__ == '__main__':
    db.create_all()