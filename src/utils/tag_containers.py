import src.utils.data_files as files
from src.utils.db import Database


class TagsContainer:
    def tag_ids_for(self, an_id):
        pass

    def tag_names_for(self, an_id):
        pass


class QuestionRATagsContainer(TagsContainer):
    def __init__(self):
        self.db = Database()

    def tag_ids_for(self, question_id):
        return self.db.ros_answers_tag_ids_for_question(question_id)

    def tag_names_for(self, question_id):
        return self.db.tag_ids_to_names(self.tag_ids_for(question_id))

    def questions_with_tag(self, tag_id):
        return self.db.questions_described_using_the_ros_answers_tag_id(tag_id)


class QuestionExtendedTagsContainer(TagsContainer):
    def __init__(self):
        self.__initialize_question_extended_tags()
        self.__initialize_extended_tags_to_questions()
        self.db = Database()

    def __initialize_question_extended_tags(self):
        self.question_extended_tags = files.get_data(files.question_full_extended_tags)

    def __initialize_extended_tags_to_questions(self):
        self.extended_tags_to_questions = files.get_data(files.full_extended_tags_to_questions)

    def tag_ids_for(self, question_id):
        """

        :param question_id: id of a question
        :type question_id: int
        :return: the list of extended tags for that question
        :rtype: str
        """
        try:
            return self.question_extended_tags[str(question_id)]
        except KeyError:
            return []

    def tag_names_for(self, question_id):
        return self.db.tag_ids_to_names(self.tag_ids_for(question_id))

    def questions_with_tag(self, tag_id):
        """

        :param tag_id: the id of the tag
        :type tag_id: int
        :return: list of questions described by that tag
        :rtype: str
        """
        try:
            return self.extended_tags_to_questions[str(tag_id)]
        except KeyError:
            return []


class UserRATagsContainer(TagsContainer):

    def __init__(self):
        self.db = Database()

    def tag_ids_for(self, user_id):
        return self.db.ros_answers_tag_ids_for_user(user_id)

    def tag_names_for(self, user_id):
        return self.db.ros_answers_tag_names_for_user(user_id)


class UserExtendedTagsContainer(TagsContainer):

    def __init__(self):
        self.__initialize_user_extended_tags()
        self.db = Database()

    def __initialize_user_extended_tags(self):
        self.user_extended_tags = files.get_data(files.user_full_extended_tags)

    def tag_ids_for(self, user_id):
        """
        It returns a list with the ids
        :param user_id: the id of the user
        :type user_id: int
        :return: a list of all tags of the user
        :rtype list[int]
        """
        try:
            return self.user_extended_tags[str(user_id)]
        except KeyError:
            return []

    def tag_names_for(self, user_id):
        return self.db.tag_ids_to_names(self.tag_ids_for(user_id))
