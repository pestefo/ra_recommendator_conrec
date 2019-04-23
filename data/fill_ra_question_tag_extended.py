#!/usr/bin/env python
# coding: utf-8
import json
with open('ros_question_tag_extended.json', 'r') as fp:
    data = json.load(fp)

for question in data:
    for tag in data[question]:
        print('{}\t{}'.format(question, tag))
