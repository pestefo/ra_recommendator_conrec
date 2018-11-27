#!/usr/bin/env python
# coding: utf-8
import json
import csv


rutdata = 'data/r_ut.csv'
path_to_results = 'data/'


def normalize(data):
    max_r = -1
    for d in data:
        if max_r < float(d[2]):
            max_r = float(d[2])

    d_norm = list()
    for d in data:
        value = float(d[2]) / max_r
        d_norm.append([d[0], d[1], value])

    return d_norm


def main():
    users = set()
    tags = set()
    rut = list()
    data = dict()
    data['nodes'] = list()
    data['links'] = list()

    with open(rutdata, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader, None)
        for row in reader:
            users.add(row[0])
            tags.add(row[1])
            rut.append([row[0], row[1], row[2]])
    rut_normalizado = normalize(rut)

    threshold = 0.5
    for row in rut_normalizado:
        if row[2] >= threshold:
            data['links'].append(
                {'source': row[0], 'target': row[1], 'value': row[2]})

        for user in users:
            data['nodes'].append({'id': user, 'group': 1})

        for tag in tags:
            data['nodes'].append({'id': tag, 'group': 2})
    # Read results, get coverage and print it
    with open(path_to_results + 'rut_procesado_50percent.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    main()
