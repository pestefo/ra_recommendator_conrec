import src.utils.data_files as files
from src.utils.db import Database


class Sample:
    def __init__(self, nb_of_participants=None):
        self.db = Database()
        self.__nb_of_participants = nb_of_participants
        self.__questions = None

    def nb_of_participants(self):
        return self.__nb_of_participants

    def size(self):
        """

        :return: total number of questions, the size of the sample
        :rtype: int
        """
        return len(self.questions())

    def questions(self):
        """

        :return: all the questions in the sample
        :rtype: list[int]
        """
        if not self.__questions:
            self.__questions = self.db.questions_with_n_participants(self.nb_of_participants())

        return self.__questions


class P5(Sample):

    def nb_of_participants(self):
        return 5


class P6(Sample):

    def nb_of_participants(self):
        return 6

class P7(Sample):

    def nb_of_participants(self):
        return 7

class P8(Sample):

    def nb_of_participants(self):
        return 8

class P9(Sample):

    def nb_of_participants(self):
        return 9

class P10(Sample):

    def nb_of_participants(self):
        return 10

class P2(Sample):

    def nb_of_participants(self):
        return 2

class P3(Sample):

    def nb_of_participants(self):
        return 3

class P4(Sample):

    def nb_of_participants(self):
        return 4

class Q100P5(P5):
    """
    Special sample that i've been using for testing the algorithms
    There are 100 questions with 5 participants (1 asker + 4 answerers
    or commenters

    """

    def questions(self):
        return files.get_data(files.questions_sample_100q_5p)[:100]
