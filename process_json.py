import json

with open('r_uq.json') as json_data:
    data = json.load(json_data)


questions = data.keys()
new_dict = {}
for q in questions:
	new_dict[q] = {}
	for el in data[q]:
		new_dict[q][el['u']] = el['r']

with open("r_uq_2.json", "w") as write_file:
    json.dump(new_dict, write_file)