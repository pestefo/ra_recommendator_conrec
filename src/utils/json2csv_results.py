import csv
import json

path = '/home/pestefo/projects/experiment_1/data/wcfa_100q_5p_2nd_exp/'
questions = [9041, 9056, 9063, 9081, 9084, 9091, 9097, 9107, 9116, 9130, 9134, 9135, 9152, 9159, 9163, 9166, 9195, 9197, 9201, 9208, 9210, 9251, 9257, 9259, 9261, 9273, 9277, 9287, 9301, 9311, 9343, 9373, 9384, 9427, 9442, 9471, 9511, 9512, 9520, 9545, 9553, 9556, 9588, 9606, 9615, 9620, 9637, 9640, 9653, 9658, 9684, 9686,
             9693, 9702, 9750, 9766, 9768, 9796, 9807, 9815, 9902, 9917, 9922, 9942, 9943, 9977, 9987, 10006, 10013, 10020, 10026, 10027, 10038, 10047, 10072, 10080, 10105, 10110, 10120, 10130, 10143, 10145, 10149, 10166, 10187, 10222, 10235, 10238, 10245, 10280, 10284, 10313, 10323, 10329, 10332, 10335, 10338, 10342, 10343, 10356]


def file_path_for(question_id, extension):
    return path + 'results_for_' + str(question_id) + '.' + str(extension)


def main():

    for q in questions:
        with open(file_path_for(q, 'json'), 'rb') as jsonfile:
            data = json.load(jsonfile)
            with open(file_path_for(q, 'csv'), 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['uid', 'score_t'])
                for d in data:
                    writer.writerow(['user_' + str(d[0]), d[1]])


if __name__ == '__main__':
    main()
