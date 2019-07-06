from src.utils.tag_containers import *


class Scenario:
    def user_tag_container(self):
        pass

    def question_tag_container(self):
        pass

    def r_ut_table(self):
        pass


class ScenarioA (Scenario):

    def user_tag_container(self):
        return UserRATagsContainer ()

    def question_tag_container(self):
        return QuestionRATagsContainer ()

    def r_ut_table(self):
        return files.r_ut_table_scenario['A']

    @staticmethod
    def name():
        return 'Scenario A'

class ScenarioB (Scenario):

    def user_tag_container(self):
        return UserRATagsContainer ()

    def question_tag_container(self):
        return QuestionExtendedTagsContainer ()

    def r_ut_table(self):
        return files.r_ut_table_scenario['B']

    @staticmethod
    def name():
        return 'Scenario B'

class ScenarioC (Scenario):

    def user_tag_container(self):
        return UserExtendedTagsContainer ()

    def question_tag_container(self):
        return QuestionRATagsContainer ()

    def r_ut_table(self):
        return files.r_ut_table_scenario['C']

    @staticmethod
    def name():
        return 'Scenario C'

class ScenarioD (Scenario):

    def user_tag_container(self):
        return UserExtendedTagsContainer ()

    def question_tag_container(self):
        return UserExtendedTagsContainer ()

    def r_ut_table(self):
        return files.r_ut_table_scenario['D']

    @staticmethod
    def name():
        return 'Scenario D'