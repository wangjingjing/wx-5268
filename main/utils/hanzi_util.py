#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


HANZI_RE = ur'[\u2E80-\u9FFF]'

STOP_HANZI_SET = set(u'''的 啊'''.split())


def tokenize(content):
    hanzi_set = set()
    for match in re.finditer(HANZI_RE, content):
        hanzi = match.group()
        hanzi_set.add(hanzi)

    return hanzi_set - STOP_HANZI_SET

