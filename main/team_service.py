#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import redis
from .consts import Constant


def get_next_schedule_id():
    '''
    使用redis的自增操作获取下一个活动ID
    '''

    if not redis.exists(Constant.SCHEDULE_ID_INCREMENT):

        max_schedule_id = get_max_schedule_id()
        redis.set(Constant.SCHEDULE_ID_INCREMENT, max_schedule_id)

    redis.incr(Constant.SCHEDULE_ID_INCREMENT)
    return redis.get(Constant.SCHEDULE_ID_INCREMENT)


def save_schedule_info(schedule):
    pass
