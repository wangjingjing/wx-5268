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


@app.route("/schedules")
def get_available_schedule():

    schedules = service.get_available_schedules_of_user('12345678901234567890123456789000')
    return render_template("schedule_detailed_list.html", schedules=schedules)


@app.route("/schedule/<int:schedule_id>")
def get_schedule_info(schedule_id):

    schedule = service.get_schedule_by_id(schedule_id)
    return render_template("schedule_info.html", schedule=schedule)
