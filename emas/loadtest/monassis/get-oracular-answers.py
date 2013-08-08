#!bin/python

import funkload
import cPickle

print 'Getting all answers from the oracle. This might take some time...'
answers = funkload.get_all_answers_from_oracle()
with open('oracular-answers.pickle','wb') as fp:
    cPickle.dump(answers, fp, protocol=2)
print 'Done.'
