#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel


class Register(BaseModel):
    
    __tablename__ = 'REGISTER_INFO'

    open_id = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=True)
    mobile_no = db.Column(db.String(15), nullable=True)

    def __init__(self, open_id, name=None, mobile_no=None):
        self.open_id = open_id
        self.name = name
        self.mobile_no = mobile_no

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
