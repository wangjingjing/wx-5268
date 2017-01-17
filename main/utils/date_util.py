#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time


def get_current_time_minute():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())


def get_timestamp_float(timeStr, format='%Y-%m-%d %H:%M:%S'):
    return time.mktime(time.strptime(timeStr, format))

