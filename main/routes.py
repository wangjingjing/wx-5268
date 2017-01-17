#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from . import app
import service


@app.route("/")
def main():
    '''

    '''
    return render_template("main.html")


@app.route("/user/applied_schedules")
def get_applied_schedules():

    schedules = service.get_applied_schedules_of_user('12345678901234567890123456789000')
    return render_template("schedule_detailed_list.html", 
        schedules=schedules, label=u'已报名活动')


@app.route("/user/available_schedules")
def get_available_schedules():

    schedules = service.get_available_schedules_of_user('12345678901234567890123456789000')
    return render_template("schedule_detailed_list.html", 
        schedules=schedules, label=u'球队活动')


@app.route("/user/future_schedule/<int:schedule_id>")
def get_schedule_future(schedule_id):

    schedule = service.get_future_schedule('12345678901234567890123456789000', schedule_id)
    
    return render_template("schedule_info_future.html", schedule=schedule)

