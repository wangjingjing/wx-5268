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


@app.route("/applied-schedules")
def get_applied_schedules():

    schedules = service.get_applied_schedules_of_user('12345678901234567890123456789000')
    return render_template("schedule_detailed_list.html", 
        schedules=schedules, label=u'已报名活动')


@app.route("/available-schedules")
def get_available_schedules():

    schedules = service.get_available_schedules_of_user('12345678901234567890123456789000')
    return render_template("schedule_detailed_list.html", 
        schedules=schedules, label=u'球队活动')


@app.route("/schedule/<int:schedule_id>")
def get_schedule_info(schedule_id):

    schedule = service.get_schedule_by_id(schedule_id)
    return render_template("schedule_info.html", schedule=schedule)

