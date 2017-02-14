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
