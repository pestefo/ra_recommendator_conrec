import unittest

from con_rec import *
from math import sqrt


class WCFAlgorithmNoMemoryTest(unittest.TestCase):

    wcfa = None
    wcfanm = None

    def get_wcfa():
        if not WCFAlgorithmNoMemoryTest.wcfa:
            WCFAlgorithmNoMemoryTest.wcfa = WCFAlgorithm()
        return WCFAlgorithmNoMemoryTest.wcfa

    def get_wcfanm():
        if not WCFAlgorithmNoMemoryTest.wcfanm:
            WCFAlgorithmNoMemoryTest.wcfanm = WCFAlgorithmNoMemory()
        return WCFAlgorithmNoMemoryTest.wcfanm

    def setUp(self):

        self.wcfa = WCFAlgorithmNoMemoryTest.get_wcfa()
        self.wcfanm = WCFAlgorithmNoMemoryTest.get_wcfanm()
        self.target_question = 9045
        self.asker = 7
        self.answerers = [3, 5184, 23668]

    def test(self):

        self.assertEqual(self.wcfanm.get_asker_of_question(
            self.target_question), self.asker)
        self.assertEqual(
            self.wcfanm.participants_of_question(self.target_question),
            [self.asker])

        self.assertEqual(self.wcfanm.r_uq(
            self.asker, self.target_question, self.target_question), 1)
        for answerer in self.answerers:
            self.assertEqual(self.wcfanm.r_uq(
                answerer, self.target_question, self.target_question), 0)

    def test_questions_in_common(self):

        # From answerers, only 3 has questions in common with the asker (7)
        self.assertGreater(
            len(self.wcfanm.questions_in_common(
                [3, self.asker]) - set([self.target_question])),
            0)
        self.assertEqual(
            len(self.wcfanm.questions_in_common(
                [5184, self.asker]) - set([self.target_question])),
            0)
        self.assertEqual(
            len(self.wcfanm.questions_in_common(
                [23668, self.asker]) - set([self.target_question])),
            0)

    def test_score(self):

        questions_in_common = self.wcfanm.questions_in_common(
            [3, self.asker]) - set([9045])

        qs_of_asker = self.wcfanm.questions_for_user(self.asker)
        qs_of_three = self.wcfanm.questions_for_user_except(3, 9045)

        self.assertNotIn(self.target_question, questions_in_common)
        self.assertIn(self.target_question, qs_of_asker)
        self.assertNotIn(self.target_question, qs_of_three)

        num = sum(map(lambda q:
                      self.wcfa.r_uq(self.asker, q) *
                      self.wcfa.r_uq(3, q),
                      questions_in_common))

        # sum(map(lambda q: w.r_uq(7,q)**2, q_asker-set([9045])))
        # + 1 (r_uq in 9045)
        # = 4.132594898687973
        sum_asker = sum(map(lambda q:
                            self.wcfa.r_uq(
                                self.asker, q) ** 2,
                            qs_of_asker - set([9045]))) + 1

        sum_three = sum(map(lambda q:
                            self.wcfa.r_uq(3, q) ** 2,
                            qs_of_three))

        div = sqrt(sum_asker * sum_three)

        self.assertEqual(num, 2.3743067033976124)
        self.assertAlmostEqual(sum_asker, 4.132594898687973)
        self.assertEqual(sum_three, 297.3294433061163)
        self.assertEqual(div, 35.053418387321244)

        score = num / div

        self.assertEqual(score, 0.06773395613411543)


if __name__ == '__main__':
    unittest.main()
