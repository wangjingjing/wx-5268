#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel

class GroupUser(BaseModel):
    
    __tablename__ = 'GROUP_USER'

    groupId = db.Column(db.String(32), name='GROUP_ID', nullable=False)
    userId = db.Column(db.String(32), name='USER_ID', nullable=False)

    def __init__(self, groupId, userId):
        self.groupId = groupId
        self.userId = userId

    def __repr__(self):
        return '<ID %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
