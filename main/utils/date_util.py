#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time

def get_specific_time_minute(timestapmp=None):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestapmp))


def get_current_time_minute():
    return get_specific_time_minute()


def get_timestamp_float(timeStr, format='%Y-%m-%d %H:%M:%S'):
    return time.mktime(time.strptime(timeStr, format))


def get_timestamp_float_minute(timeStr):
    return get_timestamp_float(timeStr, '%Y-%m-%d %H:%M')