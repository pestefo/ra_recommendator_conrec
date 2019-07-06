import unittest
from src.utils.extended_tag_extractor import QuestionTagsContainer
import src.utils.data_files as files


class TestExtendedTagExtractor(unittest.TestCase):

    e = QuestionTagsContainer()
    tags = files.tag_data_for_testing
    questions = list(tags.keys())

    def tags_for(self, question_id):
        return self.tags[question_id]['tags']

    def extended_tags_for(self, question_id):
        return list(set(self.tags_for(question_id) + self.tags[question_id]['extended-tags']))

    def question_has_extended_tags(self, question_id):
        return self.tags[question_id]['to-test']

    def test_question_to_tag_mapping(self):
        for q_id in self.questions:
            with self.subTest(q_id=q_id):
                self.assertEqual(set(self.tags_for(q_id)), set(self.e.ros_answers_tag_names_for_question(q_id)), "Tags should be the same")

    def test_question_to_extended_tag_mapping(self):
        for q_id in self.questions:
            if self.question_has_extended_tags(q_id):
                with self.subTest(q_id=q_id):
                    print("From JSON:\t {}".format(sorted(self.extended_tags_for(q_id))))
                    print("")
                    print("From DB:\t {}".format(sorted(self.e.extracted_tags_for(q_id))))
                    print("")

                    self.assertEqual(set(self.extended_tags_for(q_id)), set(self.e.extracted_tags_for(q_id)),
                                     "Tags should be the same")


if __name__ == '__main__':
    unittest.main()
