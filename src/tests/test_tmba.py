import unittest

import src.utils.data_files as files
from src.algorithms.scenarios import Scenario
from src.algorithms.tag_map_based_algorithm import TMBAlgorithm


class TestTMBAr (unittest.TestCase):

    # TODO: la r_uq esta para todas las preguntas?
    def test_basic(self):
        """
        "9033": [
          {
             "u": 2,
             "r": 0.25
          },
          {
             "u": 3,
             "r": 0.25
          },
          {
             "u": 11,
             "r": 0.25
          },
          {
             "u": 139,
             "r": 0.25
          }
       ],"""
        tmba = TMBAlgorithm (Scenario.all_scenarios ()[0])
        table = files.get_data (files.r_uq_table)

        question_id = 9033
        self.assertEqual (table[str (question_id)]['2'], tmba.r_uq (2, question_id))
        self.assertEqual (table[str (question_id)]['3'], tmba.r_uq (3, question_id))
        self.assertEqual (table[str (question_id)]['11'], tmba.r_uq (11, question_id))
        self.assertEqual (table[str (question_id)]['139'], tmba.r_uq (139, question_id))

        question_id = 192086
        self.assertEqual (table[str (question_id)]['9486'], tmba.r_uq (9486, question_id))
        self.assertEqual (table[str (question_id)]['20121'], tmba.r_uq (20121, question_id))
        self.assertEqual (table[str (question_id)]['28560'], tmba.r_uq (28560, question_id))

        question_id = 297087

        self.assertEqual (table[str (question_id)]['2575'], tmba.r_uq (2575, question_id))
        self.assertEqual (table[str (question_id)]['19307'], tmba.r_uq (19307, question_id))
        self.assertEqual (table[str (question_id)]['30400'], tmba.r_uq (30400, question_id))


if __name__ == '__main__':
    unittest.main ()
