#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel


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
