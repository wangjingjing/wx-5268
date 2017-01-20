#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from . import app
import service


@app.route('/')
def main():
    '''

    '''
    return render_template('main.html')


@app.route('/user/applied-schedules')
def get_applied_schedules():

    schedules = service.get_applied_schedules_of_user('12345678901234567890123456789000')
    return render_template('schedule_detailed_list.html', 
        schedules=schedules, label=u'已报名活动')

@app.route('/user/attended-schedules')
def get_attended_schedules():

    schedules = service.get_attended_schedules_of_user('12345678901234567890123456789000')
    return render_template('schedule_detailed_list.html', 
        schedules=schedules, label=u'已参加活动')

@app.route('/user/available-schedules')
def get_available_schedules():

    schedules = service.get_available_schedules_of_user('12345678901234567890123456789000')
    return render_template('schedule_detailed_list.html', 
        schedules=schedules, label=u'球队活动')


@app.route('/user/future-schedule/<int:schedule_id>')
def get_schedule_future(schedule_id):

    schedule = service.get_future_schedule('12345678901234567890123456789000', schedule_id)

    return render_template('schedule_info_future.html', schedule=schedule)


@app.route('/user/applied-schedule/<int:schedule_id>')
def apply_schedule(schedule_id):

    service.apply_schedule(schedule_id, '12345678901234567890123456789000')

    success_msg = u'您已报名编号' + str(schedule_id) + u'的活动'
    return render_template('success.html', success_msg=success_msg)


@app.route('/user/cancel-schedule/<int:schedule_id>')
def cancel_schedule(schedule_id):

    schedule_status = service.cancel_schedule(schedule_id, '12345678901234567890123456789000')

    if schedule_status is None:
        success_msg = u'您已取消编号' + str(schedule_id) + u'的活动'
        return render_template('success.html', success_msg=success_msg)
    elif schedule_status == '1':
        error_msg = u'编号' + str(schedule_id) + u'的活动正在进行中，不能取消报名'
    elif schedule_status == '2':
        error_msg = u'编号' + str(schedule_id) + u'的活动已经结束，不能取消报名'
    elif schedule_status == '3':
        error_msg = u'编号' + str(schedule_id) + u'的活动即将开始，不能取消报名'
        
    return render_template('error.html', error_msg=error_msg)
