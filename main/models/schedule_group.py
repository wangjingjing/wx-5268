#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from ..consts imort Constant
from .baseModel import BaseModel
from .schedule import Schedule

class ScheduleGroup(BaseModel):
    
    __tablename__ = 'SCHEDULE_GROUP'

    scheduleId = db.Column(db.String(32), name='SCHEDULE_ID', nullable=False)
    groupId = db.Column(db.String(32), name='GROUP_ID', nullable=False)

    def __init__(self, scheduleId, groupId):
        self.scheduleId = scheduleId
        self.groupId = groupId

    def __repr__(self):
        return '<ID %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

def getGroupSchedule(groupId):
    return db.session.query(Schedule).join(ScheduleGroup, 
        Schedule.id == ScheduleGroup.scheduleId).filter(
        ScheduleGroup.groupId == groupId, 
        ScheduleGroup.useState == Constant.USE_STATE_YES).all()