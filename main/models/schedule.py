#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel


class Schedule(BaseModel):
    
    __tablename__ = 'SCHEDULE'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    type = db.Column(db.String(1), nullable=False)
    plan_date = db.Column(db.String(16))
    address_id = db.Column(db.String(32))
    address_name = db.Column(db.String(64))
    opponent_id = db.Column(db.String(32))
    opponent_name = db.Column(db.String(64))
    remark = db.Column(db.Text)

    def __init__(self, type, plan_date=None, address_id=None, 
        opponent_id=None, remark=None):
        self.type = type
        self.plan_date = plan_date
        self.address_id = address_id
        self.opponent_id = opponent_id
        self.remark = remark

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
