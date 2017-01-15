#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from .. import app


db = SQLAlchemy(app)


def get_object_by_id(clazz, id):
    return db.session.query(clazz).filter(clazz.id == id).one()
