import unittest
from src.algorithms.tag_map_based_algorithm import TMBAlgorithm
import src.utils.data_files as files
from src.algorithms.scenarios import Scenario


class TestTMBAr(unittest.TestCase):

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
        tmba = TMBAlgorithm(Scenario.all_scenarios()[0])
        table = files.get_data(files.r_uq_table)
        question_id = 9033
        print(table['9033'][2])
        self.assertEqual(tmba.r_uq(2, question_id), table['9033'][2])


if __name__ == '__main__':
    unittest.main()
