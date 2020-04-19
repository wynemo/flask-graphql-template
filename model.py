# coding: utf-8

from db import db


class SimpleRecord(db.Model):
    __tablename__ = 'simple_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(64))
    port = db.Column(db.Integer)
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))

    def to_dict(self):
        return dict(
            id=self.id,
            ip=self.ip,
            port=self.port,
            username=self.username,
            password=self.password
        )
