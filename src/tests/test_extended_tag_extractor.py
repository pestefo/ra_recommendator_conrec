import unittest
from src.utils.extended_tag_extractor import ExtendedTagExtractor
import src.utils.data_files as files


class TestExtendedTagExtractor(unittest.TestCase):

    e = ExtendedTagExtractor()
    tags = files.tag_data_for_testing
    questions = list(tags.keys())

    def tags_for(self, question_id):
        return self.tags[question_id]['tags']

    def extended_tags_for(self, question_id):
        return self.tags[question_id]['extended-tags']

    def test_question_to_tag_mapping(self):
        for q_id in self.questions:
            with self.subTest(q_id=q_id):
                self.assertEqual(self.tags_for(q_id), self.e.tags_for(q_id), "Tags should be the same")

    def test_question_to_extended_tag_mapping(self):
        for q_id in self.questions:
            with self.subTest(q_id=q_id):
                self.assertEqual(self.extended_tags_for(q_id), self.e.extended_tags_for(q_id),
                                 "Tags should be the same")


if __name__ == '__main__':
    unittest.main()
