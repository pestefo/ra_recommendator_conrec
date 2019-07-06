import json

import src.utils.data_files as files
from src.utils.db import Database


class TagsContainer:
    def tag_ids_for(self, an_id):
        pass

    def tag_names_for(self, an_id):
        pass


class QuestionRATagsContainer (TagsContainer):
    def __init__(self):
        self.db = Database ()

    def tag_ids_for(self, question_id):
        return self.db.ros_answers_tag_ids_for_question (question_id)

    def tag_names_for(self, question_id):
        return self.db.tag_ids_to_names (self.tag_ids_for (question_id))

    def questions_with_tag(self, tag_id):
        return self.db.questions_described_using_the_ros_answers_tag_id (tag_id)


class QuestionExtendedTagsContainer (TagsContainer):
    def __init__(self):
        self.question_extended_tags = self.__initialize_question_extended_tags ()
        self.extended_tags_to_questions = self.__initialize_extended_tags_to_questions ()
        self.db = Database ()

    def __initialize_question_extended_tags(self):
        with open (files.question_full_extended_tags, 'r') as fp:
            return json.load (fp)

    def __initialize_extended_tags_to_questions(self):
        with open (files.full_extended_tags_to_questions, 'r') as fp:
            return json.load (fp)

    def tag_ids_for(self, question_id):
        return self.question_extended_tags[question_id]

    def tag_names_for(self, question_id):
        return self.db.tag_ids_to_names (self.tag_ids_for (question_id))

    def questions_with_tag(tag_id):
        return self.extended_tags_to_questions[tag_id]


class UserRATagsContainer (TagsContainer):

    def __init__(self):
        self.db = Database ()

    def tag_ids_for(self, user_id):
        return self.db.ros_answers_tag_ids_for_user (user_id)

    def tag_names_for(self, user_id):
        return self.db.ros_answers_tag_names_for_user (user_id)


class UserExtendedTagsContainer (TagsContainer):

    def __init__(self):
        self.user_extended_tags = self.__initialize_user_extended_tags ()
        self.db = Database ()

    def __initialize_user_extended_tags(self):
        with open (files.user_full_extended_tags, 'r') as fp:
            return json.load (fp)

    def tag_ids_for(self, user_id):
        """
        It returns a list with the ids
        :param user_id: the id of the user
        :type int
        :return: a list of all tags of the user
        :type list of int
        """
        return self.user_extended_tags[user_id]

    def tag_names_for(self, user_id):
        return self.db.tag_ids_to_names (self.tag_ids_for (user_id))
