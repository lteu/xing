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
from matplotlib import pyplot as plt
from sklearn.svm import SVR
from sklearn.svm import SVC


csv.field_size_limit(sys.maxsize)


def loadItems():
	itemset ={}
	itemset_active = []
	count= 0
	with open(DATAPATH+'/original/items.csv','rb') as f:

		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				tmpItem = {}
				tmpItemID = row[0]
				tmpItem['title'] = row[1]
				tmpItem['career_level'] = row[2]
				tmpItem['discipline_id'] = row[3]
				tmpItem['industry_id'] = row[4]
				tmpItem['country'] = row[5]
				tmpItem['region'] = row[6]
				tmpItem['latitude'] = row[7]
				tmpItem['longitude'] = row[8]
				tmpItem['employment'] = row[9]
				tmpItem['tags'] = row[10]
				
				itemset[str(row[0])] = tmpItem
				if int(row[12]) == 1:
					itemset_active.append(tmpItemID)
			count += 1
	return itemset,itemset_active

# instead of loading unnecessary 150.000.000 users
def loadTargetUsersWithProfile():
	linecount =0
	users = {}
	with open(DATAPATH+'/target/target_users_profile.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:	
			if linecount > 0:
				user = {}
				userid = row[0]
				user['id'] = row[0]
				user['jobroles'] = row[1]
				user['career_level'] = row[2]
				user['discipline_id'] = row[3]
				user['industry_id'] = row[4]
				user['country'] = row[5]
				user['region'] = row[6]
				user['experience_n_entries_class'] = row[7]
				user['experience_years_experience'] = row[8]
				user['experience_years_in_current'] = row[9]
				user['edu_degree'] = row[10]
				user['edu_fieldofstudies'] = row[11]
				users[userid] = user
			linecount += 1
	return users

def loadTargetUserIDs(filename):
	linecount = 0
	target_users_id = []
	with open(DATAPATH+'/'+filename,'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if linecount > 0:
				target_users_id.append(row[0])
			linecount += 1

	return target_users_id

def loadImpressionsDictByFilename(filename):
	impressions = {}
	count= 0
	with open(DATAPATH+'/impressions/'+filename,'rb') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				tmpID = row[0]
				if tmpID not in impressions:
					impressions[tmpID] = row[3].split(",")
				else:
					impressions[tmpID] += row[3].split(",")
			count += 1
	return impressions

def loadInteractionsByWeeks(weeks):
	dic = {}
	for week in weeks:
		count = 0
		with open(DATAPATH+'/interactions/week'+str(week)+'b.csv','rb') as f:
			reader = csv.reader(f, delimiter='\t')
			for row in reader:
				if count>1:
					userid = row[0]
					itemid = row[1]
					intype = row[2]
					if userid not in dic:
						dic[userid] = {}
					dic[userid][itemid]=intype
				count += 1
	return dic

def normalizeItemFeatures(item,titles_base,tags_base,indu_base):
	career_level = 0
	if item['career_level'] != 'null' and item['career_level'] != 'NULL' and item['career_level'] != '':
		career_level = int(str(item['career_level']))
	
	feat_arr = []
	feat_arr.append(calSimScoreForLists(titles_base,item['title'].split(",")))
	feat_arr.append(calSimScoreForLists(tags_base,item['tags'].split(",")))
	feat_arr.append(career_level)
	feat_arr.append(int(item['discipline_id']))
	feat_arr.append(int(item['industry_id']))
	
	feat_arr.append(convertCountryToCode(item['country']))
	feat_arr.append(int(item['region']))
	feat_arr.append(int(item['employment']))
	return feat_arr



def calOccurenceRank(disorderList):
	counted_dic =  Counter(disorderList)
	tupleWithOccurences = counted_dic.items() 
	tuple_sorted = sorted(tupleWithOccurences,key=lambda x: x[1], reverse=True)
	ranked_array = []
	for x in tuple_sorted:
		ranked_array.append(x[0])
	return ranked_array

def calSimScoreForLists(passtset,newset):
	if len(set(passtset[:1]).intersection(set(newset))):
		return 9
	elif len(set(passtset[:4]).intersection(set(newset))):
		return 4
	elif len(set(passtset).intersection(set(newset))):
		return 1
	else:
		return 0

def calSimScoreForListsSoft(passtset,newset):
	if len(set(passtset[:1]).intersection(set(newset))):
		return 5
	elif len(set(passtset[:4]).intersection(set(newset))):
		return 4
	elif len(set(passtset).intersection(set(newset))):
		return 3
	else:
		return 0


def convertCountryToCode(country):
	if country == 'de':
		return 3
	elif country == 'at':
		return 2
	elif country == 'ch':
		return 1
	else:
		return 0





# =====================================
# - - - MAIN - - - 
# =====================================

start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


# create solution file process
# -------------------------------------
result_file = 'solution_scikit.csv'
header = "user_id\titems"
with open(DATAPATH+'/solution/'+result_file, 'w') as f:
	f.write(str(header)+"\n")


# loading process
# -------------------------------------


itemset,itemset_active = loadItems()

print 'items loaded ... '


target_user_ids = loadTargetUserIDs('target/target_users_1000.csv')
print 'user ids loaded ...'

dic_interactions = loadInteractionsByWeeks([40,41,42,43])

print 'weekly interactions loaded'


dic_impressions = loadImpressionsDictByFilename("week-40-41-42-43c.csv")

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
	titles_collected = []
	tags_collected = []
	indu_collected = []


	for key, value in interactions.items():
		key = str(key)
		if int(value) != 4: #relevant item id
			if key not in itemset:
				continue
			item = itemset[key]
			pieces_title = str(item['title']).split(",")
			titles_collected = titles_collected + pieces_title

			pieces_tags = str(item['tags']).split(",")
			tags_collected = tags_collected + pieces_tags

			# indu_collected.append(item['industry_id'])


	titles_tags = titles_collected+tags_collected


	titles_base = calOccurenceRank(titles_collected)
	tags_base = calOccurenceRank(tags_collected)
	indu_base = calOccurenceRank(indu_collected)

	# print 'nomalization prepared'

	# Normalization process
	# ===============================

	X = []
	Y = []


	# interactions

	items_int = []
	for key, value in interactions.items():
		value = int(value)
		if key not in itemset:
			continue
		item = itemset[key]
		feat_arr = normalizeItemFeatures(item,titles_base,tags_base,indu_base)
		X.append(feat_arr)
		items_int.append(key)
		if value == 4:
			value = -1
		elif value == 3:
			value = 6
		elif value == 2:
			value = 4
		elif value == 1:
			value = 2
		# if value == 4:
		# 	value = 0
		# elif value == 3:
		# 	value = 9
		# elif value == 2:
		# 	value = 8
		# elif value == 1:
		# 	value = 6
		Y.append(value)


	# impressions

	impressions = list(set(impressions))
	impressions_reduced = list(set(impressions) - set(items_int))

	for key in impressions_reduced:
		
		if key not in itemset:
			continue

		item = itemset[key]
		feat_arr = normalizeItemFeatures(item,titles_base,tags_base,indu_base)
		X.append(feat_arr)
		Y.append(0)
		# Y.append(1)


	if Y is None or len(set(Y)) == 0:
		print 'no impressions nor interactions for user ', user
		# print Y
	elif len(set(Y)) == 1 and 1 not in Y:
		print 'impressions missing', user
		# print Y
	elif len(set(Y)) == 1:
		print 'interactions missing', user
		# print Y
	else:
		# preprocess items - heavy
		x = []
		x_ids = []
		count= 0
		for activeItemID in itemset_active:
			tmpItem = itemset[activeItemID]

			tmpItemTags = tmpItem['tags'].split(",")
			tmpItemTitles = tmpItem['title'].split(",")
			b = tmpItemTags +tmpItemTitles
			if not set(titles_tags).isdisjoint(b):
				feat_arr = normalizeItemFeatures(tmpItem,titles_base,tags_base,indu_base)
				x.append(feat_arr)
				x_ids.append(activeItemID)


		if len(x) == 0: #the case as interactions are missiong
			continue
		# SVM

		# print len(X),' ',len(Y), ' ',len(x)

		svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
		y = svr_rbf.fit(X, Y).predict(x)
		y = y.tolist()


		# making pair - heavy

		itemscore = []
		for i in xrange(0,len(x)):
			itemscore.append([x_ids[i],y[i]])
			
		itemscore_sorted = sorted(itemscore,key=lambda x: x[1], reverse=True)

		# result chopping

		recommended_itemsSet = itemscore_sorted[:31]
		recommended_items = []
		for tmpItem in recommended_itemsSet:
			recommended_items.append(tmpItem[0])

		# result stringfying

		yy = ",".join(recommended_items)
		outputline = str(user)+"\t"+yy
		output.append(outputline)


		# chunck output

		maincounter += 1
		if maincounter % 10 == 0:
			with open(DATAPATH+'/solution/'+result_file, 'a') as f:
				for line in output:
					f.write(str(line)+"\n")

			output = []
			print str(maincounter),' of ',len(target_user_ids),' processed ...'



# write final solutions
# ------------

with open(DATAPATH+'/solution/'+result_file, 'a') as f:
	# f.write("userid\titems\n")
	for line in output:
		f.write(str(line)+"\n")

print "all processes terminated ..."
print("--- %s seconds ---" % (time.time() - start_time))