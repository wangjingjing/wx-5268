#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel

class Register(BaseModel):
    
    __tablename__ = 'REGISTER_INFO'

    openId = db.Column(db.String(32), name='OPEN_ID', nullable=False)
    name = db.Column(db.String(32), nullable=True)
    mobileNo = db.Column(db.String(15), name='MOBILE_NO', nullable=True)

    def __init__(self, openId, name=None, mobileNo=None):
        self.openId = openId
        self.name = name
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
