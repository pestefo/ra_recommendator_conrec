'''
Data of ros_user_tag.csv, ros_tag.csv and ros_question_tag.csv
were extracted from with simple SELECT * FROM table queries

'''
import csv
import json
"""
From
2,3,5
2,4,6
3,1,2
4,5,6
4,6,7

To:
2: [(3,5),(4,6)], 
3:[2,1], 
4:[(5,6).(6,7)],...
"""

tag_dict = None

# Input files
ros_user_tag_csv = 'data/ros_user_tag.csv'
ros_question_tag_csv = 'data/ros_question_tag.csv'
ros_tag_csv = 'data/ros_tag.csv'

# Output files
ros_user_tag_json = 'data/ros_user_tag.json'
ros_question_tag_json = 'data/ros_question_tag.json'
ros_tag_json = 'data/ros_tag.json'

def generate_list_of_tags_per_user():
    with open(ros_user_tag_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__()   # skip header
        user_tags = {}
        for u, t, c in reader:

            try:
                user_tags[u].append({'tag': t, 'count': c})
            except KeyError:
                user_tags[u] = [{'tag': t, 'count': c}]

        return user_tags


'''
Output example:
"35923": [{"tag": "165", "count": "4"}, {"tag": "886", "count": "4"},
{"tag": "2182", "count": "4"}],
"35924": [{"tag": "815", "count": "2"}, {"tag": "2933", "count": "2"}]
'''


def generate_list_of_tags_per_question():
    with open(ros_question_tag_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__()   # skip header
        question_tags = {}
        for q, t in reader:

            try:
                question_tags[q].append(t)
            except KeyError:
                question_tags[q] = [t]

        return question_tags


def generate_tag_name_dictionary():
    with open(ros_tag_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__()
        tag_dict = {tag_id: tag_name for tag_id, tag_name in reader}

    return tag_dict


def main():
    u = generate_list_of_tags_per_user()
    q = generate_list_of_tags_per_question()
    tag_dict = generate_tag_name_dictionary()

    with open(ros_user_tag_json, 'w') as outfile:
        json.dump(u, outfile)
        print('ros_user_tag.json DONE')

    with open(ros_question_tag_json, 'w') as outfile:
        json.dump(q, outfile)
        print('ros_question_tag.json DONE')

    with open(ros_tag_json, 'w') as outfile:
        json.dump(tag_dict, outfile)
        print('ros_tag.json DONE')
    # print(q)
    # '296861': ['63', '1465', '66', '5392'],
    # print("'296861': ['63', '1465', '66', '5392'],")
    # print(tag_dict['63'] + ', ' + tag_dict['1465'] +
    # ', ' + tag_dict['66'] + ', ' + tag_dict['5392'])
    # Should say: kinetic, offline, install, dvd


if __name__ == '__main__':
    main()
