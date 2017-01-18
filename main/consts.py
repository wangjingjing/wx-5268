#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Constant():
    '''
    常量类
    '''

    USE_STATE_YES = '1'
    USE_STATE_NO = '0'

    REDIS_PREFIX_USER = 'user:'
    REDIS_PREFIX_USER_GROUPSET = 'groupset_'
    REDIS_PREFIX_USER_APPLYZSET = 'applyzset_'
    REDIS_PREFIX_USER_ATTENDZSET = 'attendzset_'

    REDIS_PREFIX_GROUP = 'group:'
    REDIS_PREFIX_GROUP_SCHEDULESET = 'scheduleset_'

    REDIS_PREFIX_SCHEDULE = 'schedule:'
    REDIS_PREFIX_SCHEDULE_INFO = 'scheduleinfo_'
