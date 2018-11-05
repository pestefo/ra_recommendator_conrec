'''
Data of ros_user_tag.csv, ros_tag.csv and ros_question_tag.csv
were extracted from with simple SELECT * FROM table queries

'''
import csv

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


def generate_list_of_tags_per_user():
    with open('ros_user_tag.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__()   # skip header
        user_tags = {}
        for u, t, c in reader:

            try:
                user_tags[u].append((t, c))
            except KeyError:
                user_tags[u] = [(t, c)]

        return user_tags


def main():
    u = generate_list_of_tags_per_user()
    print(u.keys())


if __name__ == '__main__':
    main()
