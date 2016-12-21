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
import random
import operator
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




# create solution file process
# -------------------------------------
# result_file = 'solution_svm.csv'
# header = "user_id\titems"
# with open(DATAPATH+'/solution/'+result_file, 'w') as f:
# 	f.write(str(header)+"\n")


# loading process
# -------------------------------------



with open(DATAPATH+"/datafeatureid.json") as data_file:    
    set_ID = json.load(data_file)
# dic = json.loads(DATAPATH+"/datafeatureid.json")

# sys.exit()


itemset,itemset_active = loadItems(DATAPATH)

print 'items loaded ... '

# userset = loadTargetUsersWithProfile(DATAPATH)
# print 'target users loaded ... '

# target_user_ids = loadTargetUserIDs('target/target_users_small.csv')
target_user_ids = loadTargetUserIDs('target/target_users_1000.csv',DATAPATH)
# target_user_ids = loadTargetUserIDs('target/target_users.csv')

print 'user ids loaded ...'

dic_interactions = loadInteractionsByWeeks([40,41,42,43],DATAPATH)

print 'weekly interactions loaded'


dic_impressions = loadImpressionsDictByFilename("week-40-41-42-43c.csv",DATAPATH)

print "weekly impressions loaded"

output = []
maincounter = 0
for user in target_user_ids:

	print 'processing user ', user

	interactions = {}
	impressions = []

	
	if user in dic_interactions:
		interactions = dic_interactions[user]

	if user in dic_impressions:
		impressions =  dic_impressions[user]
	

	# print interactions


	# Normalization process
	# ===============================

	# # interactions

	checker_imp = False
	checker_itr = False
	training_data = []
	items_itr = []
	for key, value in interactions.items():
		key = str(key)
		value = int(value)
		if key not in itemset:
			continue
		item = itemset[key]
		items_itr.append(key)
		value = interactionVal(value)
		# print 'a',key
		line = featureToLine(item,value,set_ID,key)
		training_data.append(line)
		checker_itr = True
		# print line

	# # impressions

	impressions = list(set(impressions))
	impressions_reduced = list(set(impressions) - set(items_itr))

	for key in impressions_reduced:

		key = str(key)
		if key not in itemset:
			continue
		item = itemset[key]
		value = 1

		# print 'b',key
		line = featureToLine(item,value,set_ID,key)
		training_data.append(line)
		checker_imp = True
		# print line

	# print 'finised training'


	# print len(itemset_active),' ',len(itemset)
	train_file = str(user)+"_train.dat"
	with open(DATAPATH+'/traindata/'+train_file, 'w') as f:
		for line in training_data:
			f.write(str(line)+"\n")
	# 	# print len(X),' ',len(Y), ' ',len(x)

	# 	svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
	# 	y = svr_rbf.fit(X, Y).predict(x)
	# 	y = y.tolist()


	# 	# making pair - heavy

	# 	itemscore = []
	# 	for i in xrange(0,len(x)):
	# 		itemscore.append([x_ids[i],y[i]])
			
	# 	itemscore_sorted = sorted(itemscore,key=lambda x: x[1], reverse=True)

	# 	# result chopping

	# 	recommended_itemsSet = itemscore_sorted[:31]
	# 	recommended_items = []
	# 	for tmpItem in recommended_itemsSet:
	# 		recommended_items.append(tmpItem[0])

	# 	# result stringfying

	# 	yy = ",".join(recommended_items)
	# 	outputline = str(user)+"\t"+yy
	# 	output.append(outputline)


	# 	# chunck output

	# 	maincounter += 1
	# 	if maincounter % 10 == 0:
	# 		with open(DATAPATH+'/solution/'+result_file, 'a') as f:
	# 			for line in output:
	# 				f.write(str(line)+"\n")

	# 		output = []
	# 		print str(maincounter),' of ',len(target_user_ids),' processed ...'



# write final solutions
# ------------

# with open(DATAPATH+'/solution/'+result_file, 'a') as f:
# 	# f.write("userid\titems\n")
# 	for line in output:
# 		f.write(str(line)+"\n")

print "all processes terminated ..."
print("--- %s seconds ---" % (time.time() - start_time))