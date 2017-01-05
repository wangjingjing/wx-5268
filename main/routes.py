#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from . import app


@app.route("/")
def main():
	'''

	'''
	return render_template("main.html")

@app.route("/schedules")
def getAvailableSchedule():

	return render_template("schedule-detailed-list.html")
