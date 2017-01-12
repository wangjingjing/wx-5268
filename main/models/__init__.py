#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from .. import app

db = SQLAlchemy(app)

def getObjectById(clazz, id):
    return db.session.query(clazz).filter(clazz.id == id).first()