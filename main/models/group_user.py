#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from ..consts import Constant
from .baseModel import BaseModel
from .group import Group


class GroupUser(BaseModel):
    
    __tablename__ = 'GROUP_USER'

    group_id = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.String(32), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self


def get_groupid_of_user(user_id):
    return db.session.query(Group.id).join(GroupUser, 
        GroupUser.group_id == Group.id).filter(GroupUser.user_id == user_id, 
        GroupUser.use_state == Constant.USE_STATE_YES).all()