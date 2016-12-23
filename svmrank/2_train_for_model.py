# simple prediction, source: http://stackoverflow.com/questions/24517858/time-series-forecasting-with-support-vector-regression

'''
general idea: using SVM and last 2 weeks activities to predict next week activities (obviously filtered)
if user has not activites in last 2 weeks check if his profile is complete,
 if so, suggest activities of similar users
 otherwise, basline approach ...
'''

import csv
import time
import os
import sys
import datetime

import json
import numpy as np

from collections import Counter


from func import *


csv.field_size_limit(sys.maxsize)


# =====================================
# - - - MAIN - - - 
# =====================================

start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


target_user_ids = loadTargetUserIDs('target/target_users_1000.csv',DATAPATH)

for user in target_user_ids:
	# print user
	command = './svm_rank_learn -c 0.01 -v 0 '+DATAPATH+'/traindata/'+str(user)+'_train.dat '+DATAPATH+'/model0.01/'+str(user)+'_model.txt'

	print command
	os.system(command)
	# break

print "all processes terminated ..."
print("--- %s seconds ---" % (time.time() - start_time))