#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from ..consts import Constant
import uuid
from datetime import datetime


def get_uuid():
    random_id = str(uuid.uuid1())
    return ''.join(random_id.split('-'))


class BaseModel(db.Model):

    __abstract__ = True

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.String(32), default=get_uuid(), primary_key=True, nullable=False)
    use_state = db.Column(db.String(1), default=Constant.USE_STATE_YES, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now) 
    create_user_id = db.Column(db.String(32))
    create_user_name = db.Column(db.String(32))
    update_date = db.Column(db.DateTime)
    update_user_id = db.Column(db.String(32))
    update_user_name = db.Column(db.String(32))

    @property
    def columns(self):
        return [column.name for column in self.__table__.columns]
 
    @property
    def columnitems(self):
        return dict([(column, getattr(self, column)) for column in self.columns])
 
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)
 
    def to_json(self):
        return self.columnitems
