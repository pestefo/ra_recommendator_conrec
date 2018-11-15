import unittest

from con_rec import *


class WCFAlgorithmNoMemoryTest(unittest.TestCase):
    def setUp(self):
        self.wcfa = WCFAlgorithm()
        self.wcfanm = WCFAlgorithmNoMemory()
        self.q = 9045
        self.asker = 7
        self.answerers = [3, 5184, 23668]

    def test(self):

        self.assertEqual(wcfanm.get_asker.of_question(q), self.asker)
        self.assertEqual(wcfanm.participants_of_question(q), [self.asker])

        self.assertEqual(wcfanm.r_uq(self.asker, q, q), 1)
        for answerer in answerers:
            self.assertEqual(wcfanm.r_uq(answerer, q, q), 0)
