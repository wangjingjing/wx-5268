#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import RotatingFileHandler
from redis import Redis, ConnectionPool


app = Flask(__name__, instance_relative_config=True)

Bootstrap(app)

# 加载配置
app.config.from_object('config')
app.config.from_pyfile('config.py')

# 记录日志
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)

# redis
pool = ConnectionPool(host=app.config['REDIS_SERVER'], port=6379)
redis = Redis(connection_pool=pool)

# 路由
from .routes import *
