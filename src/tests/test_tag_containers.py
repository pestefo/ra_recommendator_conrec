import unittest

from src.algorithms.scenarios import *


class TestExtendedTagExtractor(unittest.TestCase):

    def test_correct_use_of_tag_containers(self):
        scenarioA = ScenarioA()
        scenarioB = ScenarioB()
        scenarioC = ScenarioC()
        scenarioD = ScenarioD()

        self.assertIsInstance(scenarioA.question_tag_container(), QuestionRATagsContainer)
        self.assertIsInstance(scenarioA.user_tag_container(), UserRATagsContainer)

        self.assertIsInstance(scenarioB.question_tag_container(), QuestionExtendedTagsContainer)
        self.assertIsInstance(scenarioB.user_tag_container(), UserRATagsContainer)

        self.assertIsInstance(scenarioC.question_tag_container(), QuestionRATagsContainer)
        self.assertIsInstance(scenarioC.user_tag_container(), UserExtendedTagsContainer)

        self.assertIsInstance(scenarioD.question_tag_container(), QuestionExtendedTagsContainer)
        self.assertIsInstance(scenarioD.user_tag_container(), UserExtendedTagsContainer)


    def test_r_ut_scenario_A(self):
        """
        TODO:
        For a tag and a user, assess a correct R_ut
        """

    def test_score_scenario_A(self):
        """
        TODO:
        For a question and a user, assess a correct score
        """
        pass

if __name__ == '__main__':
    unittest.main()
