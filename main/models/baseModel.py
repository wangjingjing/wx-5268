#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
import uuid
from datetime import datetime

class BaseModel(db.Model):

    __abstract__ = True

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.String(32), default=uuid.uuid1(), primary_key=True, nullable=False)
    useState = db.Column(db.String(1), name='USE_STATE', default='1', nullable=False)
    createDate = db.Column(db.DateTime, name='CREATE_DATE', default=datetime.now) 
    createUserId = db.Column(db.String(32), name='CREATE_USER_ID')
    createUserName = db.Column(db.String(32), name='CREATE_USER_NAME')
    updateDate = db.Column(db.DateTime, name='UPDATE_DATE')
    updateUserId = db.Column(db.String(32), name='UPDATE_USER_ID')
    updateUserName = db.Column(db.String(32), name='UPDATE_USER_NAME')