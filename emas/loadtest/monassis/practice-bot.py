#!bin/python
import funkload
import getpass

grade = 11
chapterId = 104 # The available chapter ids for a grade can be extracted from the dashboard view
numberOfExercisesToDo = 10

username = raw_input('Username: ')
password = getpass.getpass('Password: ')

session = funkload.emas_login(username, password)
print 'Logged in.'
funkload.clear_all_caches()
print 'Cleared caches.'
funkload.select_grade(session, grade)
print 'Grade selected.'
funkload.select_chapter(session, chapterId)
print 'Chapter selected.'
questionCount = 0
while questionCount < numberOfExercisesToDo:
    templateId, randomSeed, subQuestionIndex, expectedResponseCount = funkload.get_question(session)
    if subQuestionIndex is not None:
        print 'Got a question and submitting answer.'
        correctResponses = funkload.ask_oracle(session, templateId, randomSeed)
        funkload.submit_response(session, correctResponses, subQuestionIndex)
    else:
        print 'Have reached end of question, requesting next question.'
        questionCount += 1
        funkload.next_question(session)
print 'Done.'
