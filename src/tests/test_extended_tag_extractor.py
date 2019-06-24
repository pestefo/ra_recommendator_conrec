import unittest
import json
from src.utils.extended_tag_extractor import ExtendedTagExtractor


class TestExtendedTagExtractor(unittest.TestCase):

    e = ExtendedTagExtractor()
    with open('src/tests/tags_data.json', 'r') as fp:
        tags = json.load(fp)
    questions = tags.keys()

    def tags_for(self, question_id):
        return self.tags[question_id]['tags']

    def extended_tags_for(self, question_id):
        return self.tags[question_id]['extended-tags']

    def test_tags_for(self):
        q_id = self.questions[0]

        self.assertEquals(self.tags_for(q_id), self.e.tags_for(q_id))


if __name__ == '__main__':
    unittest.main()
