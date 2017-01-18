#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
from redis import Redis, ConnectionPool
from . import app
from .consts import Constant
from utils.json_util import *
from utils.date_util import *
from models import *


pool = ConnectionPool(host=app.config['REDIS_SERVER'], port=6379)
redis = Redis(connection_pool=pool)


def get_available_schedules_of_user(user_id):
    '''
    获取用户可见的活动列表
    '''

    # 用户的全部组ID
    user_groupids = get_groupid_of_user(user_id)

    # 各组可见的活动ID做并集
    scheduleids = set()
    for group_id in user_groupids:
        scheduleids = scheduleids.union(get_scheduleid_of_group(group_id))

    # 用户已报名活动ID列表
    apply_scheduleids = get_applied_scheduleids_of_user(user_id)

    schedules = []
    for schedule_id in scheduleids:
        schedule = get_schedule_by_id(schedule_id)

        if schedule_id in apply_scheduleids:
            schedule['apply_flag'] = '1'

        # 活动在预订时间后的一段时间(DELAY_TIME)内仍然可见
        if get_timestamp_float_minute(schedule['plan_date']) < time.time():
            schedule['underway_flag'] = '1'


        schedules.append(schedule)

    # 根据活动的预订时间排序
    return sorted(schedules, key = lambda schedule: schedule['plan_date'])


def get_groupid_of_user(user_id):
    '''
    获取用户所在的分组ID集合
    '''

    redis_user_group = redis.hget(Constant.REDIS_PREFIX_USER + user_id, 
        Constant.REDIS_PREFIX_USER_GROUPSET)

    if redis_user_group is None:

        redis_user_group = Constant.REDIS_PREFIX_USER_GROUPSET + str(time.time())

        # sqlalchemy's rerurn value is turple
        user_groupids = group_user.get_groupid_of_user(user_id)

        for group_id, in user_groupids:
            redis.sadd(redis_user_group, group_id)

        redis.hset(Constant.REDIS_PREFIX_USER + user_id, 
            Constant.REDIS_PREFIX_USER_GROUPSET, redis_user_group)

    return redis.smembers(redis_user_group)


def get_scheduleid_of_group(group_id):
    '''
    获取指定组可见的活动ID集合
    '''

    redis_group_schedule = redis.hget(Constant.REDIS_PREFIX_GROUP + group_id, 
        Constant.REDIS_PREFIX_GROUP_SCHEDULESET)

    if redis_group_schedule is None or not redis.exists(redis_group_schedule):

        redis_group_schedule = Constant.REDIS_PREFIX_GROUP_SCHEDULESET + str(time.time())

         # 当前时间的DELAY_TIME时长内视为正在进行的活动
        current_delay_time = time.time() + app.config['DELAY_TIME']*60

        group_schedules = schedule_group.get_scheduleid_of_group(
            group_id, get_specific_time_minute(current_delay_time))

        if len(group_schedules) == 0:
            return []

        for schedule_id, plan_date in group_schedules:
            redis.sadd(redis_group_schedule, schedule_id)

        expire_date = group_schedules[0][1]
        # 设置组可见活动ID列表的缓存过期时间为第一个活动预订时间的DELAY_TIME时长后
        expire_timestamp = int(get_timestamp_float_minute(expire_date
            )) + app.config['DELAY_TIME']*60

        redis.expireat(redis_group_schedule, expire_timestamp)

        redis.hset(Constant.REDIS_PREFIX_GROUP + group_id, 
            Constant.REDIS_PREFIX_GROUP_SCHEDULESET, redis_group_schedule)

    return redis.smembers(redis_group_schedule)


def get_schedule_by_id(schedule_id):
    '''
    获取指定活动的全部数据
    '''

    schedule_id_str = str(schedule_id)

    redis_schedule = redis.hget(Constant.REDIS_PREFIX_SCHEDULE + schedule_id_str, 
        Constant.REDIS_PREFIX_SCHEDULE_INFO)

    if redis_schedule is None:

        redis_schedule = Constant.REDIS_PREFIX_SCHEDULE_INFO + str(time.time())

        schedule_info = get_object_by_id(Schedule, schedule_id)

        if schedule_info is None:
            return

        # 将活动对象序列化为json串，保存至redis中
        redis.set(redis_schedule, json.dumps(schedule_info, cls=JsonEncoderUtil))

        redis.hset(Constant.REDIS_PREFIX_SCHEDULE + schedule_id_str, 
            Constant.REDIS_PREFIX_SCHEDULE_INFO, redis_schedule)

    # 从缓存中取得活动的json串，返回反序列化的json对象（一个散列）
    return json.loads(redis.get(redis_schedule), object_hook=dict_to_object)


def get_applied_scheduleids_of_user(user_id):
    '''
    获取用户已报名的活动ID列表
    '''

    redis_user_apply = redis.hget(Constant.REDIS_PREFIX_USER + user_id, 
        Constant.REDIS_PREFIX_USER_APPLYZSET)

    if redis_user_apply is None or not redis.exists(redis_user_apply):

        redis_user_apply = Constant.REDIS_PREFIX_USER_APPLYZSET + str(time.time())

        # 当前时间的DELAY_TIME时长内视为正在进行的活动
        current_delay_time = time.time() + app.config['DELAY_TIME']*60

        schedule_id_date = schedule_user.get_apply_schedules_of_user(
            user_id, get_specific_time_minute(current_delay_time))

        if len(schedule_id_date) == 0:
            return []

        for schedule_id, plan_date in schedule_id_date:

            # 用redis的有序集合保存活动ID，分值是活动的预订时间
            redis.zadd(redis_user_apply, schedule_id, 
                get_timestamp_float_minute(plan_date))

        expire_date = schedule_id_date[0][1]
        # 设置已报名列表的缓存过期时间为第一个活动预订时间的DELAY_TIME时长后
        expire_timestamp = int(get_timestamp_float_minute(expire_date
            )) + app.config['DELAY_TIME']*60

        redis.expireat(redis_user_apply, expire_timestamp)

        redis.hset(Constant.REDIS_PREFIX_USER + user_id, 
            Constant.REDIS_PREFIX_USER_APPLYZSET, redis_user_apply)

    return redis.zrange(redis_user_apply, 0, -1)


def get_applied_schedules_of_user(user_id):
    '''
    获取用户已报名的活动列表
    '''

    scheduleids = get_applied_scheduleids_of_user(user_id)

    # TODO 未来应增加分页查询
    schedules = []
    for schedule_id in scheduleids:
        schedule = get_schedule_by_id(schedule_id)

        # 活动在预订时间后的一段时间(DELAY_TIME)内标识为正在进行
        if get_timestamp_float_minute(schedule['plan_date']) < time.time():
            schedule['underway_flag'] = '1'

        schedules.append(schedule)

    return schedules


def get_future_schedule(user_id, schedule_id):

    schedule = get_schedule_by_id(schedule_id)

    apply_scheduleids = get_applied_scheduleids_of_user(user_id)

    schedule['apply_flag'] = '0'
    if str(schedule['id']) in apply_scheduleids:
        schedule['apply_flag'] = '1'

    return schedule


def get_attended_scheduleids_of_user(user_id):
    '''
    获取用户已参加的活动ID列表
    '''

    redis_user_attend = redis.hget(Constant.REDIS_PREFIX_USER + user_id, 
            Constant.REDIS_PREFIX_USER_ATTENDZSET)

    if redis_user_attend is None or not redis.exists(redis_user_attend):

        redis_user_attend = Constant.REDIS_PREFIX_USER_ATTENDZSET + str(time.time())

        # 当前时间的DELAY_TIME时长内视为正在进行的活动
        current_delay_time = time.time() + app.config['DELAY_TIME']*60

        schedule_id_date = schedule_user.get_attend_schedules_of_user(
            user_id, get_specific_time_minute(current_delay_time))

        if len(schedule_id_date) == 0:
            return []

        for schedule_id, plan_date in schedule_id_date:

            # 用redis的有序集合保存活动ID，分值是活动的预订时间
            redis.zadd(redis_user_attend, schedule_id,
                get_timestamp_float_minute(plan_date))

        expire_date = schedule_id_date[0][1]
        # 设置已报名列表的缓存过期时间为最近一个活动预订时间的DELAY_TIME时长后
        expire_timestamp = int(get_timestamp_float_minute(
            expire_date)) + app.config['DELAY_TIME']*60

        redis.expireat(redis_user_attend, expire_timestamp)

        redis.hset(Constant.REDIS_PREFIX_USER + user_id, 
            Constant.REDIS_PREFIX_USER_ATTENDZSET, redis_user_attend)

    return redis.zrange(redis_user_attend, 0, -1, desc=True)


def get_attended_schedules_of_user(user_id):
    '''
    获取用户已参加的活动列表
    '''

    scheduleids = get_attended_scheduleids_of_user(user_id)

    # TODO 未来应增加分页查询
    schedules = []
    for schedule_id in scheduleids:
        schedules.append(get_schedule_by_id(schedule_id))

    return schedules
