#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Constant():
    '''
    常量类
    '''

    USE_STATE_YES = '1'
    USE_STATE_NO = '0'

    SCHEDULE_STATUS_DEFAULT = '0' # 未开始
    SCHEDULE_STATUS_ON = '1' # 进行中
    SCHEDULE_STATUS_OFF = '2' # 已结束
    SCHEDULE_STATUS_NEAR = '3' # 即将开始

    REDIS_PREFIX_USER = 'user:'
    REDIS_PREFIX_USER_GROUPSET = 'groupset_'
    REDIS_PREFIX_USER_APPLYZSET = 'applyzset_'
    REDIS_PREFIX_USER_ATTENDZSET = 'attendzset_'

    REDIS_PREFIX_GROUP = 'group:'
    REDIS_PREFIX_GROUP_SCHEDULESET = 'schedulezset_'

    REDIS_PREFIX_SCHEDULE = 'schedule:'
    REDIS_PREFIX_SCHEDULE_INFO = 'scheduleinfo_'

    SCHEDULE_ID_INCREMENT = 'schedule_id_incr'

    ALL_ADDRESS_ID_NAME = 'all_addr_id_name'
    ALL_ADDRESS_NAME_HANZI = 'all_addr_name_hanzi'
    REDIS_PREFIX_ADDRESSNAME_HANZI = 'addr_name:'

    ALL_GROUP_ID_NAME = 'all_group_id_name'
