#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from ..consts import Constant
import uuid
from datetime import datetime


class BaseModel(db.Model):

    __abstract__ = True

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.String(32), name='ID', default=uuid.uuid1(), primary_key=True, nullable=False)
    use_state = db.Column(db.String(1), name='USE_STATE', 
        default=Constant.USE_STATE_YES, nullable=False)
    create_date = db.Column(db.DateTime, name='CREATE_DATE', default=datetime.now) 
    create_user_id = db.Column(db.String(32), name='CREATE_USER_ID')
    create_user_name = db.Column(db.String(32), name='CREATE_USER_NAME')
    update_date = db.Column(db.DateTime, name='UPDATE_DATE')
    update_user_id = db.Column(db.String(32), name='UPDATE_USER_ID')
    update_user_name = db.Column(db.String(32), name='UPDATE_USER_NAME')