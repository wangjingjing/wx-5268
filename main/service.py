#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
from redis import Redis, ConnectionPool
from . import app
from .consts import Constant
from models import *
from models.schedule import Schedule


pool = ConnectionPool(host=app.config['REDIS_SERVER'], port=6379)
redis = Redis(connection_pool=pool)


def get_available_schedules_of_user(user_id):

    user_groupids = get_groupid_of_user(user_id)

    scheduleids = set()
    for group_id in user_groupids:
        scheduleids = scheduleids.union(get_scheduleid_of_group(group_id))

    schedules = []
    for schedule_id in scheduleids:
        #schedules.append(get_schedule_by_id(schedule_id))
        schedules.append(get_object_by_id(Schedule, schedule_id))

    return sorted(schedules, key = lambda schedule: schedule.plan_date)
    

def get_groupid_of_user(user_id):

    cached = redis.hexists(Constant.REDIS_PREFIX_USER + user_id, 
        Constant.REDIS_PREFIX_USER_GROUPSET)

    if cached:
        redis_user_group = redis.hget(Constant.REDIS_PREFIX_USER + user_id, 
            Constant.REDIS_PREFIX_USER_GROUPSET)

    else:
        redis_user_group = Constant.REDIS_PREFIX_USER_GROUPSET + str(time.time())

        # sqlalchemy's rerurn value is turple
        user_groupids = group_user.get_groupid_of_user(user_id)
        
        for group_id, in user_groupids:
            redis.sadd(redis_user_group, group_id)

        redis.hset(Constant.REDIS_PREFIX_USER + user_id, 
            Constant.REDIS_PREFIX_USER_GROUPSET, redis_user_group)

    return redis.smembers(redis_user_group)


def get_scheduleid_of_group(group_id):

    cached = redis.hexists(Constant.REDIS_PREFIX_GROUP + group_id, 
        Constant.REDIS_PREFIX_GROUP_SCHEDULESET)

    if cached:
        redis_group_schedule = redis.hget(Constant.REDIS_PREFIX_GROUP + group_id, 
            Constant.REDIS_PREFIX_GROUP_SCHEDULESET)

    else:
        redis_group_schedule = Constant.REDIS_PREFIX_GROUP_SCHEDULESET + str(time.time())

        current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())

        group_schedules = schedule_group.get_scheduleid_of_group(group_id, current_time)

        for schedule_id, in group_schedules:
            redis.sadd(redis_group_schedule, schedule_id)

        redis.hset(Constant.REDIS_PREFIX_GROUP + group_id, 
            Constant.REDIS_PREFIX_GROUP_SCHEDULESET, redis_group_schedule)

    return redis.smembers(redis_group_schedule)


def get_schedule_by_id(schedule_id):

    cached = redis.hexists(Constant.REDIS_PREFIX_SCHEDULE + schedule_id, 
        Constant.REDIS_PREFIX_SCHEDULE_INFO)

    if cached:
        redis_schedule = redis.hget(Constant.REDIS_PREFIX_SCHEDULE + schedule_id, 
            Constant.REDIS_PREFIX_SCHEDULE_INFO)

        return json.loads(redis.get(redis_schedule))

    else:
        redis_schedule = Constant.REDIS_PREFIX_SCHEDULE_INFO + str(time.time())

        schedule_info = get_object_by_id(Schedule, schedule_id)

        # TODO json序列化
        redis.set(redis_schedule, json.dumps(schedule_info))

        return schedule_info