#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import datetime


class JsonEncoderUtil(json.JSONEncoder):

    def default(self, obj):

        #convert object to a dict
        if isinstance(obj, datetime.date):
            return obj.isoformat()
 
        try:
            return obj.to_json()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)


def dict_to_object(d):
    '''
    convert dict to object
    '''
    
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
        
    else:
        inst = d

    return inst