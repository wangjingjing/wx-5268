#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel
from ..consts import Constant


class Address(BaseModel):
    
    __tablename__ = 'ADDRESS_INFO'

    name = db.Column(db.String(64), nullable=False)
    full_address = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self


def get_all_address_id_name():
    return db.session.query(Address.id, Address.name).filter(
        Address.use_state == Constant.USE_STATE_YES).all()
