from src.utils.tag_containers import *


class Scenario:
    def user_tag_container(self):
        pass

    def question_tag_container(self):
        pass

    def id(self) -> str:
        pass

    def name(self):
        return 'Scenario ' + self.id()

    def r_ut_table(self):
        return files.r_ut_table_scenario[self.id()]

    @staticmethod
    def all_scenarios():
        return [ScenarioA(), ScenarioB(), ScenarioC(), ScenarioD()]


class ScenarioA(Scenario):

    def user_tag_container(self):
        return UserRATagsContainer()

    def question_tag_container(self):
        return QuestionRATagsContainer()

    def r_ut_table(self):
        return files.r_ut_table_scenario['A']

    def id(self):
        return 'A'


class ScenarioB(Scenario):

    def user_tag_container(self):
        return UserRATagsContainer()

    def question_tag_container(self):
        return QuestionExtendedTagsContainer()

    def r_ut_table(self):
        return files.r_ut_table_scenario['B']

    def id(self):
        return 'B'


class ScenarioC(Scenario):

    def user_tag_container(self):
        return UserExtendedTagsContainer()

    def question_tag_container(self):
        return QuestionRATagsContainer()

    def r_ut_table(self):
        return files.r_ut_table_scenario['C']

    def id(self):
        return 'C'


class ScenarioD(Scenario):

    def user_tag_container(self):
        return UserExtendedTagsContainer()

    def question_tag_container(self):
        return QuestionExtendedTagsContainer()

    def r_ut_table(self):
        return files.r_ut_table_scenario['D']

    def id(self):
        return 'D'
