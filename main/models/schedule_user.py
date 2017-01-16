#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from ..consts import Constant
from .baseModel import BaseModel
from .schedule import Schedule


class ScheduleUser(BaseModel):
    
    __tablename__ = 'SCHEDULE_USER'

    schedule_d = db.Column(db.String(32), nullable=False)
    user_d = db.Column(db.String(32), nullable=False)

    def __init__(self, schedule_id, user_id):
        self.schedule_id = schedule_id
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self


def getFutureSchedulesOfUser(user_id, current_time):
    return db.session.query(Schedule).join(ScheduleUser, 
        Schedule.id == ScheduleUser.schedule_id).filter(
        ScheduleUser.user_id == user_id, 
        ScheduleUser.use_state == Constant.USE_STATE_YES,
        Schedule.plan_date > current_time).order_by(Schedule.plan_date).all()


def getPastSchedulesOfUser(user_id, current_time):
    return db.session.query(Schedule).join(ScheduleUser, 
        Schedule.id == ScheduleUser.schedule_id).filter(
        ScheduleUser.user_id == user_id, 
        ScheduleUser.use_state == Constant.USE_STATE_YES,
        Schedule.plan_date <= current_time).order_by(Schedule.plan_date.desc()).all()