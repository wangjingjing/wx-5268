#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel


class User(BaseModel):
    
    __tablename__ = 'USER_INFO'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(32), index=True, unique=True, nullable=False)
    nick_name = db.Column(db.String(64))
    real_name = db.Column(db.String(32), nullable=False)
    mobile_no = db.Column(db.String(15), nullable=True)

    def __init__(self, open_id, nick_name=None, real_name=None, mobile_no=None):
        self.open_id = open_id
        self.nick_name = nick_name
        self.real_name = real_name
        self.mobile_no = mobile_no

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
