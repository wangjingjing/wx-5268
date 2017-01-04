#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from .baseModel import BaseModel

class Schedule(BaseModel):
    
    __tablename__ = 'SCHEDULE'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(1), nullable=False)
    planDate = db.Column(db.String(16), name='PLAN_DATE', nullable=True)
    addressId = db.Column(db.String(32), name='ADDRESS_ID', nullable=True)
    opponentId = db.Column(db.String(32), name='OPPONENT_ID', nullable=True)
    remark = db.Column(db.Text, nullable=True)

    def __init__(self, type, planDate=None, addressId=None, 
        opponentId=None, remark=None):
        self.type = type
        self.planDate = planDate
        self.addressId = addressId
        self.opponentId = opponentId
        self.remark = remark

    def __repr__(self):
        return '<ID %d>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
