#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from ..consts import Constant
from .baseModel import BaseModel
from .schedule import Schedule


class ScheduleGroup(BaseModel):
    
    __tablename__ = 'SCHEDULE_GROUP'

    schedule_id = db.Column(db.String(32), name='SCHEDULE_ID', nullable=False)
    group_id = db.Column(db.String(32), name='GROUP_ID', nullable=False)

    def __init__(self, schedule_id, group_id):
        self.schedule_id = schedule_id
        self.group_id = group_id

    def __repr__(self):
        return 'ScheduleGroup<ID %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self


def get_scheduleid_of_group(group_id, current_time):
    return db.session.query(Schedule.id).join(ScheduleGroup, 
        Schedule.id == ScheduleGroup.schedule_id).filter(
        ScheduleGroup.group_id == group_id, 
        ScheduleGroup.use_state == Constant.USE_STATE_YES, 
        Schedule.plan_date > current_time).all()