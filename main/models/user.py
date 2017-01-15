#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel


class User(BaseModel):
    
    __tablename__ = 'USER_INFO'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(32), name='OPEN_ID', index=True, unique=True, nullable=False)
    nick_name = db.Column(db.String(64), name='NICK_NAME', nullable=True)
    real_name = db.Column(db.String(32), name='REAL_NAME', nullable=True)
    mobile_no = db.Column(db.String(15), name='MOBILE_NO', nullable=True)

    def __init__(self, open_id, nick_name=None, real_name=None, mobile_no=None):
        self.open_id = open_id
        self.nick_name = nick_name
        self.real_name = real_name
        self.mobile_no = mobile_no

    def __repr__(self):
        return 'User<open_id %r>' % self.open_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
