
from src.utils.db import  Database
from src.utils.extended_tag_extractor import ExtendedTagExtractor
def main():
    db = Database()
    tag_extractor = ExtendedTagExtractor()
    user_tags = {}

    users = db.all_users()

    for user in users:
        user_tags[user] = []
        questions = db.questions_where_user_participated(user)
        for question in questions:
            user_tags[user].append(tag_extractor.full_extended_tags_for(question))
            # TODO: se trabaja con los strings o con IDs???

    # TODO: hacer un dump a un archivo


if __name__ == '__main__':
    main()
