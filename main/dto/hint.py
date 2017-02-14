#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Hint():

    def __init__(self, label, value):
        self.label = label
        self.value = value

    def __repr__(self):
        return '<Hint %r>' % self.label

    def serialize(self):
        return {
            'label': self.label, 
            'value': self.value
        }
