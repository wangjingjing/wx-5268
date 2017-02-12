#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel
from ..consts import Constant


class Group(BaseModel):
    
    __tablename__ = 'GROUP_INFO'

    name = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(1), nullable=False)

    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

def get_all_group_id_name():
    return db.session.query(Group.id, Group.name).filter(
        Group.use_state == Constant.USE_STATE_YES).all()
