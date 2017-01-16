#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel


class Group(BaseModel):
    
    __tablename__ = 'GROUP_INFO'

    name = db.Column(db.String(32), nullable=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
