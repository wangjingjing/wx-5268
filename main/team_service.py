#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import app, redis
from .consts import Constant
from utils import hanzi_util
from models import *


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

    '''

    try:
        if schedule.address_id:
            schedule.address_name = get_address_name(schedule.address_id)

        else:
            address_id = add_address_info(schedule.address_name)
            schedule.address_id = address_id

        db.session.add(schedule)

        for group_id in group_ids:
            schedule_group = ScheduleGroup(schedule.id, group_id)
            db.session.add(schedule_group)

            #TODO 更新组可见活动集合

        db.session.commit()

    except:
        db.session.rollback()
        raise


def add_address_info(addr_name):
    '''
    '''

    address = Address(addr_name)
    db.session.add(address)
    db.session.flush()

    create_address_name_index(addr_name, address.id)
    
    return address.id


def create_address_name_index(addr_name, addr_id):
    '''

    '''

    hanzi_set = hanzi_util.tokenize(addr_name)

    pipeline = redis.pipeline(True)
    for hanzi in hanzi_set:
        pipeline.sadd(Constant.ALL_ADDRESS_NAME_HANZI, 
            Constant.REDIS_PREFIX_ADDRESSNAME_HANZI + hanzi)
        pipeline.sadd(Constant.REDIS_PREFIX_ADDRESSNAME_HANZI + hanzi, 
            addr_id)

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
