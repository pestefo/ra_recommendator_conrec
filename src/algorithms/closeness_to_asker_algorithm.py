from weighted_collaborative_filtering_algorithm import WCFAlgorithm
from math import sqrt


class C2AAlgorithm(WCFAlgorithm):

    def get_asker_of_question(self, question_id):
        asker = WCFAlgorithm.act_ask[
            (WCFAlgorithm.act_ask['q_id'] == question_id) &
            (WCFAlgorithm.act_ask['activity'] > 0)
        ]["u_id"].drop_duplicates()

        if len(asker) > 1:
            raise BaseException('More than one asker.')

        return list(asker)[0]

    # We return the asker only
    def participants_of_question(self, question_id):
        return list([self.get_asker_of_question(question_id)])

    def questions_for_user_except(self, user_id, question_id_to_ignore):
        return self.questions_for_user(user_id) - set([question_id_to_ignore])

    # R_uu - Relation between two users
    def r_uu(self, candidate, asker, target_question):
        q_in_common = self.questions_in_common([candidate, asker]) -\
            set([target_question])

        q_c = self.questions_for_user_except(candidate, target_question)
        q_a = self.questions_for_user(asker)

        a = sum(map(lambda q:
                    self.r_uq(candidate, q, target_question) *
                    self.r_uq(asker, q, target_question),
                    q_in_common))

        b = sqrt(sum(map(lambda q:
                         self.r_uq(candidate, q, target_question)**2,
                         q_c)) *
                 sum(map(lambda q:
                         self.r_uq(asker, q, target_question)**2,
                         q_a)))
        if a == 0:
            return 0
        return a / b

    # R_uq - Relation between a user and a question
    def r_uq(self, user_id, question_id, target_question):
        # In case of the target question,
        if question_id == target_question:
            # The only participant of it is the asker, whose R_uq = 1
            if self.get_asker_of_question(question_id) == user_id:
                return 1
            # if the user is not the asker, R_uq = 0
            return 0

        return super(WCFAlgorithm, self).r_uq(user_id, question_id)

    # score(c,q) = R_uu(c, asker(q))
    # Target question has only the asker as a participant
    def score(self, candidate, question):
        asker = self.get_asker_of_question(question)
        return candidate, self.r_uu(candidate, asker, question)
