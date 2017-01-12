#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool


pool = ConnectionPool(host=app.config['REDIS_SERVER'], port=6379)
redis = Redis(connection_pool=pool)