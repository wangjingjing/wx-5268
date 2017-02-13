#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from . import app, redis
from .consts import Constant
from utils import hanzi_util
from utils.date_util import *
from models import *


def get_scheduleid_of_group(group_id):
    '''
    获取指定组可见的活动ID集合
    '''

    redis_group_schedule = redis.hget(Constant.REDIS_PREFIX_GROUP + group_id, 
        Constant.REDIS_PREFIX_GROUP_SCHEDULESET)

    if redis_group_schedule is None or not redis.exists(redis_group_schedule):

        redis_group_schedule = Constant.REDIS_PREFIX_GROUP_SCHEDULESET + str(time.time())

        group_schedules = schedule_group.get_scheduleid_of_group(group_id)

        if len(group_schedules) == 0:
            return []

        pipeline = redis.pipeline(True)
        for schedule_id, plan_date in group_schedules:
            pipeline.zadd(redis_group_schedule, schedule_id, 
                get_timestamp_float_minute(plan_date))

        expire_date = group_schedules[0][1]
        # 设置组可见活动ID列表的缓存过期时间为第一个活动预订时间的DELAY_TIME时长后
        expire_timestamp = int(get_timestamp_float_minute(expire_date
            )) + app.config['DELAY_TIME']*60

        pipeline.expireat(redis_group_schedule, expire_timestamp)

        pipeline.hset(Constant.REDIS_PREFIX_GROUP + group_id, 
            Constant.REDIS_PREFIX_GROUP_SCHEDULESET, redis_group_schedule)

        pipeline.execute()

    return redis.zrange(redis_group_schedule, 0, -1)

    
def get_next_schedule_id():
    '''
    使用redis的自增操作获取下一个活动ID
    '''

    if not redis.exists(Constant.SCHEDULE_ID_INCREMENT):

        max_schedule_id = get_max_schedule_id()
        redis.set(Constant.SCHEDULE_ID_INCREMENT, max_schedule_id)

    redis.incr(Constant.SCHEDULE_ID_INCREMENT)
    return redis.get(Constant.SCHEDULE_ID_INCREMENT)


def save_schedule_info(schedule, group_ids):
    '''
    保存活动信息，同时插入活动-组关系数据
    如果是新增地址，则插入地址信息
    '''

    try:
        if schedule.address_id:
            schedule.address_name = get_address_name(schedule.address_id)

        else:
            address_id = add_address_info(schedule.address_name)
            schedule.address_id = address_id

        db.session.add(schedule)

        save_schedule_groups(group_ids, schedule.id, schedule.plan_date)

        db.session.commit()

    except:
        db.session.rollback()
        raise


def add_address_info(addr_name):
    '''
    新增地址
    '''

    address = Address(addr_name)
    db.session.add(address)
    db.session.flush()

    create_address_name_index(addr_name, address.id)
    
    return address.id


def get_address_name(addr_id):
    '''

    '''
    pass


def create_address_name_index(addr_name, addr_id):
    '''
    对地址名进行汉字拆分，作为addr_id的索引
    '''

    hanzi_set = hanzi_util.tokenize(addr_name)

    pipeline = redis.pipeline(True)
    for hanzi in hanzi_set:
        pipeline.sadd(Constant.ALL_ADDRESS_NAME_HANZI, 
            Constant.REDIS_PREFIX_ADDRESSNAME_HANZI + hanzi)
        pipeline.sadd(Constant.REDIS_PREFIX_ADDRESSNAME_HANZI + hanzi, 
            addr_id)

    pipeline.execute()


def save_schedule_groups(groupids, schedule_id, schedule_plandate):
    '''
    插入活动-组关系数据，更新组可见活动集合缓存，如果新建活动是集合中日期最近的，
    则将新活动的时间更新为组可见活动集合的过期时间
    '''

    pipeline = redis.pipeline(True)

    for group_id in group_ids:
        schedule_group = ScheduleGroup(schedule.id, group_id)
        db.session.add(schedule_group)

        get_scheduleid_of_group(group_id)
        
        redis_group_schedule = redis.hget(
            Constant.REDIS_PREFIX_GROUP + group_id, 
            Constant.REDIS_PREFIX_GROUP_SCHEDULESET)

        if redis_group_schedule is None or not redis.exists(redis_group_schedule):
            redis_group_schedule = Constant.REDIS_PREFIX_GROUP_SCHEDULESET + str(time.time())
        
        pipeline.zadd(redis_group_schedule, schedule_id, 
            get_timestamp_float_minute(schedule_plandate))

        id, plan_date = redis.zrange(redis_group_schedule, 0, 1, withscores=True)

        # 如果新建活动的预计时间是组可见集合中最近的，
        # 则将新建活动的预计时间（加延长时间）设为缓存过期时间
        if(cmp(schedule_plandate, plan_date) <= 0):
            expire_timestamp = int(get_timestamp_float_minute(schedule_plandate
                )) + app.config['DELAY_TIME']*60
            pipeline.expireat(redis_group_schedule, expire_timestamp)

    pipeline.execute()


def get_all_group_id_name():
    '''
    获取全部分组的ID与组名
    '''

    if not redis.exists(Constant.ALL_GROUP_ID_NAME):

        group_id_name = group.get_all_group_id_name()

        pipeline = redis.pipeline(True)

        for gid, gname in group_id_name:
            pipeline.hset(Constant.ALL_GROUP_ID_NAME, gid, gname)

        pipeline.execute()

    return redis.hgetall(Constant.ALL_GROUP_ID_NAME)
