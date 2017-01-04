#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel

class User(BaseModel):
    
    __tablename__ = 'USER_INFO'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openId = db.Column(db.String(32), name='OPEN_ID', index=True, unique=True, nullable=False)
    nickName = db.Column(db.String(64), name='NICK_NAME', nullable=True)
    realName = db.Column(db.String(32), name='REAL_NAME', nullable=True)
    mobileNo = db.Column(db.String(15), name='MOBILE_NO', nullable=True)

    def __init__(self, openId, nickName=None, realName=None, mobileNo=None):
        self.openId = openId
        self.nickName = nickName
        self.realName = realName
        self.mobileNo = mobileNo

    def __repr__(self):
        return '<openId %r>' % self.openId

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
