import json

# r_ut.csv -> r_uq.json using 'CSV To Keyed JSON'
# http://www.convertcsv.com/csv-to-json.htm
with open('data/r_ut.json', 'r') as json_data:
    data = json.load(json_data)


questions = data.keys()
new_dict = {}
for q in questions:
    new_dict[q] = {}
    for el in data[q]:
        new_dict[q][el['t']] = el['r']

with open("data/r_ut_2.json", "w") as write_file:
    json.dump(new_dict, write_file)
