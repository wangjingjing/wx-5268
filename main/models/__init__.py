#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from .. import app
from ..consts import Constant


db = SQLAlchemy(app)


from .group import Group
from .group_user import GroupUser
from .register import Register
from .schedule import Schedule
from .schedule_group import ScheduleGroup
from .schedule_user import ScheduleUser
from .user import User
from .address import Address


def get_object_by_id(clazz, id):
    return db.session.query(clazz).filter(clazz.id == id).one()


def get_active_schedule_user(schedule_id, user_id):
    return db.session.query(ScheduleUser).filter(
        ScheduleUser.schedule_id == schedule_id,
        ScheduleUser.user_id == user_id, 
        ScheduleUser.use_state == Constant.USE_STATE_YES).one()


def get_max_schedule_id():
    max_id, = db.session.execute('select max(id) from SCHEDULE_INFO').first()
    return max_id


def get_all_address_id_name():
    return db.session.query(Address.id, Address.name).filter(
        Address.use_state == Constant.USE_STATE_YES).all()
