#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel

class ScheduleUser(BaseModel):
    
    __tablename__ = 'SCHEDULE_USER'

    scheduleId = db.Column(db.String(32), name='SCHEDULE_ID', nullable=False)
    userId = db.Column(db.String(32), name='USER_ID', nullable=False)

    def __init__(self, scheduleId, userId):
        self.scheduleId = scheduleId
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
