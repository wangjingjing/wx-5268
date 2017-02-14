#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
from . import app
import time
import json
import user_service, team_service
from utils.date_util import *
from models import Schedule


@app.route('/')
def main():
    '''

    '''
    return render_template('main.html')


@app.route('/user/applied-schedules')
def get_applied_schedules():

    schedules = user_service.get_applied_schedules_of_user('12345678901234567890123456789000')
    return render_template('schedule_detailed_list.html', 
        schedules=schedules, label=u'已报名活动')

@app.route('/user/attended-schedules')
def get_attended_schedules():

    schedules = user_service.get_attended_schedules_of_user('12345678901234567890123456789000')
    return render_template('schedule_detailed_list.html', 
        schedules=schedules, label=u'已参加活动')

@app.route('/user/available-schedules')
def get_available_schedules():

    schedules = user_service.get_available_schedules_of_user('12345678901234567890123456789000')
    return render_template('schedule_detailed_list.html', 
        schedules=schedules, label=u'球队活动')


@app.route('/user/future-schedule/<int:schedule_id>')
def get_schedule_future(schedule_id):

    schedule = user_service.get_future_schedule('12345678901234567890123456789000', schedule_id)

    return render_template('schedule_info_future.html', schedule=schedule)


@app.route('/user/applied-schedule/<int:schedule_id>')
def apply_schedule(schedule_id):

    user_service.apply_schedule(schedule_id, '12345678901234567890123456789000')

    success_msg = u'您已报名编号' + str(schedule_id) + u'的活动'
    return render_template('success.html', success_msg=success_msg)


@app.route('/user/cancel-schedule/<int:schedule_id>')
def cancel_schedule(schedule_id):

    schedule_status = user_service.cancel_schedule(schedule_id, '12345678901234567890123456789000')

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


@app.route('/user-info')
def get_userinfo():

    return render_template('userinfo.html')


@app.route('/team/schedule/list')
def get_team_schedules():

    return render_template('team_schedule_list.html')


@app.route('/team/schedule/new')
def new_team_schedule():

    group_id_name = team_service.get_all_group_id_name()

    min_stamp = time.time() + + app.config['DELAY_TIME']*60
    min_time = get_specific_time_minute(min_stamp)

    return render_template('team_schedule_save.html', schedule=None, 
        group_id_name=group_id_name, min_time=min_time)


@app.route('/team/schedule/save', methods=['GET', 'POST'])
def save_team_schedule():

    id = request.form['id']

    if id:
        schedule = user_service.get_schedule_by_id(id)
    else:
        schedule_id = team_service.get_next_schedule_id()
        schedule = Schedule(schedule_id)
    
    schedule.plan_date = request.form['schedule_date']

    schedule.address_id = request.form['schedule_addr_id']
    schedule.address_name = request.form['schedule_addr']

    schedule.type = request.form['schedule_type']

    schedule.title = request.form.get('schedule_title')

    schedule.opponent_id = request.form.get('schedule_opp_id')
    schedule.opponent_name = request.form.get('schedule_opp')

    schedule.remark = request.form['schedule_remark']

    app.logger.debug(schedule)

    team_service.save_schedule_info(schedule, request.form.getlist('group_id'))
    
    success_msg = u'编号'
    return render_template('success.html', success_msg=success_msg)


@app.route('/team/address/hint')
def get_addressname_hint():
    
    term = request.args.get('term')
    
    hints = team_service.get_address_hints_by_index(term)

    return jsonify([hint.serialize() for hint in hints])

