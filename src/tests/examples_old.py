'''
    def example(self):

        # Tests for activity_ans_comm
        # print("\nTests: activity_ans_comm")
        # print("-----")
        # print(activity_ans_comm(0,9045) == 0)
        # print(activity_ans_comm(3,9045) == 1)
        # print(activity_ans_comm(23668,9045) == 2)
            # Tests for activity_task
        # print("\nTests: activity_task")
        # print("-----")
        # print("activity_ask(7,9045) == 1\t"+str(activity_ask(7,9045) == 1)) # True
        # print("activity_ask(3,9045) == 0\t"+str(activity_ask(3,9045) == 0)) # True
        # print("activity_ask(23668,9045) == 0\t"+str(activity_ask(23668,9045) == 0)) # True
            # Tests for question_activities
        # print("\nTests: question_activities")
        # print("-----")
        # print("question_activities(9033) == 4\t\t"+str(question_activities(9033) == 4)) # True
        # print("question_activities(9190) == 14\t\t"+str(question_activities(9190) == 14)) # True
        # print("question_activities(236154) == 9\t"+str(question_activities(236154) == 9)) # True
            # print("Question ID: 9045")
        # print("-----------------")
        # print("Asker ID = 7, Answers/Commenters = 3, 5184, 23668")
        # print(participants_of_question(9045))

        # List of questions in which a user participates - Q_{u}

            # print("")
        # print("# Questions for user 7\t\t: "+str(len(questions_for_user(7)))) # participated: 2520,
        # print("# Questions for user 3\t\t: "+str(len(questions_for_user(3))))
        # print("# Questions for user 5184\t: "+str(len(questions_for_user(5184))))
        # print("Users 3, 5184, 23668 and 7 participated in Q 9045 --> "+str(set(questions_for_user(23668)) & set(questions_for_user(5184)) & set(questions_for_user(3)) & set(questions_for_user(7))))
        # print("Users 3, 5184, 23668 and 7 participated in Q 9045 --> "+str(questions_in_common([3, 5184, 23668, 7])))
        # print("Users 3, and 7 --> "+str(questions_in_common([3, 7])))
            # print(" ")
        print("Relation user-question (r_uq)")
        print("Asker\t\t:\tr_uq(7,9045)= " + str(self.r_uq(7, 9045)))
        print("Answerer\t:\tr_uq(3,9045)= " + str(self.r_uq(3, 9045)) +
              " (provides the accepted answer)")
        print("Participant\t:\tr_uq(5184,9045)= " +
              str(self.r_uq(5184, 9045)) + " (participated twice)")
        # print(" ")
        print("Relation user-user (r_uu)")
        print("Asker-Answerer\t\t:\tr_uu(7,3)= " + str(self.r_uu(7, 3)))
        print("Asker-Participant\t:\tr_uu(7,5184)= " + str(self.r_uu(7, 5184)))
        print("Answerer-Participant\t:\tr_uu(3,5184)= " +
              str(self.r_uu(5184, 3)))

        # -----
        show_tests = True

        if show_tests:
            print(" ")
            print("Results for Q_id=9045")
            print("Asker\t\t:\tresult(7,9045)= " + str(self.result(7, 9045)))
            print("Answerer\t:\tresult(3,9045)= " +
                  str(self.result(3, 9045)) +
                  " (provides the accepted answer)")
            print("Participant\t:\tresult(5184,9045)= " +
                  str(self.result(5184, 9045)) + " (participated twice)")

            # -----
        show_ranking = True

        if show_ranking:
            print(" ")
            print("Ranking for q=9045")
            print("------------------")
            ranking = self.ranking_for_question(9045)
            print(str(ranking))
            for result in ranking:
                print(str(result[0]) + " - " + str(result[1]))
'''
