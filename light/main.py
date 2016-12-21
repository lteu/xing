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
result_file = 'solution_svm.csv'
header = "user_id\titems"
with open(DATAPATH+'/solution/'+result_file, 'w') as f:
	f.write(str(header)+"\n")


# loading process
# -------------------------------------


itemset,itemset_active = loadItems(DATAPATH)

print 'items loaded ... '

userset = loadTargetUsersWithProfile(DATAPATH)

print 'target users loaded ... '

# target_user_ids = loadTargetUserIDs('target/target_users_small.csv')
target_user_ids = loadTargetUserIDs('target/target_users_one.csv',DATAPATH)
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
	

	# comparable data calculation
	# ----------------------------------


	# prepare for nomalization: reduction process
	# ----------------------------------

	# check all possible types
	# =======
	titles_collected = []
	tags_collected = []
	indu_collected = []
	discipline_id_collected = []
	title_collected = []
	country_collected = []
	region_collected = []



	for key, value in interactions.items():
		key = str(key)
		if key not in itemset:
			continue
		item = itemset[key]
		pieces_title = str(item['title']).split(",")
		titles_collected = titles_collected + pieces_title
		pieces_tags = str(item['tags']).split(",")
		tags_collected = tags_collected + pieces_tags
		indu_collected.append(item['industry_id'])
		discipline_id_collected.append(item['discipline_id'])
		country_collected.append(item['country'])
		region_collected.append(item['region'])

	for key in impressions:
		key = str(key)
		if key not in itemset:
			continue
		item = itemset[key]
		pieces_title = str(item['title']).split(",")
		titles_collected = titles_collected + pieces_title
		pieces_tags = str(item['tags']).split(",")
		tags_collected = tags_collected + pieces_tags
		indu_collected.append(item['industry_id'])
		discipline_id_collected.append(item['discipline_id'])
		country_collected.append(item['country'])
		region_collected.append(item['region'])

	set_pure = {}
	set_ID = {}
	titles_collected_set = set(titles_collected)
	tags_collected_set = set(tags_collected)
	indu_collected_set = set(indu_collected)
	discipline_id_collected_set  = set(discipline_id_collected)
	country_collected_set = set(country_collected)
	region_collected_set = set(region_collected)

	set_pure['title'] = titles_collected_set
	set_pure['tags'] = tags_collected_set
	set_pure['industry_id'] = indu_collected_set
	set_pure['discipline_id'] = discipline_id_collected_set
	set_pure['country'] = country_collected_set
	set_pure['region'] = region_collected_set


	# print len(titles_collected_set),' ',len(tags_collected_set),' ',len(indu_collected_set),' ',len(discipline_id_collected_set),' ',len(country_collected_set),' ',len(region_collected_set)
	# num_dynamic_feat = len(titles_collected_set) + len(tags_collected_set) + len(indu_collected_set) + len(discipline_id_collected_set) + len(country_collected_set) + len(region_collected_set)
	# print num_dynamic_feat

	counter = 3
	for key_pure, value_pure in set_pure.items():
		dic = {}
		for tmpEle in value_pure:
			dic[tmpEle] = counter
			counter = counter + 1
		set_ID[key_pure] = dic

	# print counter,'  ',set_ID['country']
	# sys.exit()

	print 'value map created, preparing training data'

	# Normalization process
	# ===============================

	# # interactions

	checker_imp = False
	checker_itr = False
	training_data = []
	items_itr = []
	test_data = []
	for key, value in interactions.items():
		key = str(key)
		value = int(value)
		if key not in itemset:
			continue
		item = itemset[key]
		items_itr.append(key)
		value = interactionVal(value)
		line = featureToLine(item,value,set_ID)
		training_data.append(line)
		checker_itr = True
		print line

	# # impressions

	impressions = list(set(impressions))
	impressions_reduced = list(set(impressions) - set(items_itr))

	for key in impressions_reduced:
		key = str(key)
		if key not in itemset:
			continue
		item = itemset[key]
		value = 1
		line = featureToLine(item,value,set_ID)
		training_data.append(line)
		checker_imp = True
		print line

	if not checker_imp and not checker_itr:
		print 'no impressions nor interactions for user ', user
	# 	# print Y
	elif not checker_imp:
		print 'impressions missing', user
	# 	# print Y
	elif not checker_itr:
		print 'interactions missing', user
	else:
		# preprocess items - heavy
		for activeItemID in itemset_active:
	# 		userinfo = userset[str(user)]
			tmpItem = itemset[activeItemID]
			value = 0
			line,output_dynam = featureToLine(tmpItem,value,set_ID)
			if output_dynam.strip() != "":
				test_data.append(line)

	print len(test_data),' ',len(itemset_active),' ',len(itemset)
	# test_file = str(user)+"_test.dat"
	# with open(DATAPATH+'/testdata/'+test_file, 'a') as f:
	# 	for line in test_data:
	# 		f.write(str(line)+"\n")

	# 	if len(x) == 0: #the case as interactions are missiong
	# 		continue
	# 	# SVM

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