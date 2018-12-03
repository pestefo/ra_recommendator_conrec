#!/usr/bin/env python
# coding: utf-8
import json
import csv
from math import sqrt


rutdata = 'data/r_ut.csv'
path_to_results = 'data/'


def passes_threshold(value):
    upper_threshold = 0.8
    lower_threshold = 0.2

    return lower_threshold <= value <= upper_threshold


def normalize(data):
    max_r = -1
    for d in data:
        if max_r < float(d[2]):
            max_r = float(d[2])

    d_norm = list()
    for d in data:
        value = sqrt(float(d[2]) / max_r)

        d_norm.append([d[0], d[1], value])

    return d_norm


def get_tag_table():
    with open('data/ros_tag.csv') as csvfile:
        tag_table = dict()
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skipping header
        for row in reader:
            print(row)
            tag_table[row[0]] = row[1]
    return tag_table


def main():
    users = set()
    tags = set()
    rut = list()
    tag_names = get_tag_table()

    with open(rutdata, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader, None)  # skipping header
        for row in reader:
            users.add(row[0])
            tags.add(row[1])
            rut.append([row[0], row[1], row[2]])
    rut_normalizado = normalize(rut)
    data = dict()

    # Links
    data['nodes'] = list()
    data['links'] = list()

    filtered_rut = list()

    for row in rut_normalizado:
        if passes_threshold(row[2]):
            print(str(row[2]) + " -- YES")
            filtered_rut.append(row)
        else:
            print(str(row[2]) + " -- NO")

    filtered_users = set()
    filtered_tags = set()

    for row in filtered_rut:
        filtered_users.add(row[0])
        filtered_tags.add(row[1])

    # Nodes
    for user in filtered_users:
        data['nodes'].append({'id': 'uid:' + str(user), 'group': 1})

    for tag in filtered_tags:
        data['nodes'].append({'id': tag_names[tag], 'group': 2})

    for row in filtered_rut:
        data['links'].append(
            {'source': 'uid:' + str(row[0]),
             'target': tag_names[row[1]],
             'value': row[2]})

    # Read results, get coverage and print it
    with open(path_to_results + 'rut_procesado_80_20.json', 'w'
              ) as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    main()
