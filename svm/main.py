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


def loadInteractionsByUserAndWeek(userid,numWeek):
	arr = {}
	count = 0
	with open(DATAPATH+'/interactions/week'+str(numWeek)+'b.csv','rb') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				if int(userid) == int(row[0]):
					itemid = str(row[1])
					intype = row[2]
					arr[itemid]=intype
			count += 1
	return arr

def getItemInfoFromItemset(item):
	tmpItem ={}
	count= 0
	with open(DATAPATH+'/original/items.csv','rb') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				if int(item) == int(row[0]):
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
					break
			count += 1
	return tmpItem


def loadItems():
	itemset ={}
	count= 0
	with open(DATAPATH+'/original/items.csv','rb') as f:

		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				tmpItem = {}
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
			count += 1
	return itemset

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


def loadImpressions(userid,week):
	impressions_array = []
	count= 0
	with open(DATAPATH+'/impressions/week'+str(week)+'b.csv','rb') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				if int(userid) == int(row[0]):
					impressions_array += row[3].split(",")
					break
			count += 1
	return impressions_array

def loadImpressionsByUseridFilename(userid,filename):
	impressions_array = []
	count= 0
	with open(DATAPATH+'/impressions/'+filename,'rb') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				if int(userid) == int(row[0]):
					impressions_array += row[3].split(",")
					break
			count += 1
	return impressions_array

def normalizeItemFeatures(item,seenTitles,seenTags):
	career_level = 0
	if item['career_level'] != 'null' and item['career_level'] != 'NULL' and item['career_level'] != '':
		career_level = int(str(item['career_level']))
	
	feat_arr = []
	feat_arr.append(calSimScoreForLists(seenTitles,item['title'].split(",")))
	feat_arr.append(calSimScoreForLists(seenTags,item['tags'].split(",")))
	feat_arr.append(career_level)
	feat_arr.append(int(item['discipline_id']))
	feat_arr.append(int(item['industry_id']))
	feat_arr.append(convertCountryToCode(item['country']))
	feat_arr.append(int(item['region']))
	feat_arr.append(int(item['employment']))
	return feat_arr


# def preprocessActiveItems(userprofile):
# 	itemset = []
# 	count= 0
# 	with open(DATAPATH+'/active_items.csv','rb') as f:
# 		reader = csv.reader(f, delimiter='\t')
# 		for row in reader:
# 			if count>1:
# 				if str(userprofile['discipline_id']) == str(row[3]):
# 					tmpItem = {}
# 					tmpItem['title'] = row[1]
# 					tmpItem['career_level'] = row[2]
# 					tmpItem['discipline_id'] = row[3]
# 					tmpItem['industry_id'] = row[4]
# 					tmpItem['country'] = row[5]
# 					tmpItem['region'] = row[6]
# 					tmpItem['latitude'] = row[7]
# 					tmpItem['longitude'] = row[8]
# 					tmpItem['employment'] = row[9]
# 					tmpItem['tags'] = row[10]
# 					itemset.append(tmpItem)
# 			count += 1
# 	return impressions_array


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

def convertCountryToCode(country):
	if country == 'de':
		return 3
	elif country == 'at':
		return 2
	elif country == 'ch':
		return 1
	else:
		return 0


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


# =====================================
# MAIN PROCESS
# =====================================




# loading process
# -------------------------------------


itemset = loadItems()

print 'items loaded ... '

userset = loadTargetUsersWithProfile()

print 'target users loaded ... '

target_user_ids = loadTargetUserIDs('target/target_users_small.csv')
# target_user_ids = loadTargetUserIDs('target/target_users.csv')

print 'user ids loaded ...'

output = []
maincounter = 0
for user in target_user_ids:

	print 'processing user ', user

	# writing process
	interactions = {}
	interactions_tmp = loadInteractionsByUserAndWeek(user,41)
	interactions = dict(interactions.items() + interactions_tmp.items())

	interactions_tmp = loadInteractionsByUserAndWeek(user,42)
	interactions = dict(interactions.items() + interactions_tmp.items())

	interactions_tmp = loadInteractionsByUserAndWeek(user,43)
	interactions = dict(interactions.items() + interactions_tmp.items())

	interactions_tmp = loadInteractionsByUserAndWeek(user,44)
	interactions = dict(interactions.items() + interactions_tmp.items())

	print 'weekly interactions loaded'


	# impressions =  loadImpressions(user,41)
	# impressions +=  loadImpressions(user,42)
	# impressions +=  loadImpressions(user,43)
	# impressions +=  loadImpressions(user,44)

	impressions =  loadImpressionsByUseridFilename(user,'week-41-42-43-44c.csv')

	print "weekly impressions loaded"



# # saving pre-compiled data for a fast experiment
# # -------------

# # generate impression itemset
# itemset_reduced = {}
# for item in impressions:
# 	itemset_reduced[item] = itemset[item] 

# for key, value in interactions.items():
# 	itemset_reduced[key] = itemset[key] 

# print "itemset_imp generated"

# dic_ai ={"int":interactions,"imp":impressions,"user":user,"items":itemset_reduced}
# with open(DATAPATH+'/testing_someItems.json', 'w') as fp:
#     json.dump(dic_ai, fp)

# print 'yes'

# sys.exit()


# # loading pre-compiled data for a fast experiment 
# # -------------
# with open(DATAPATH+"/testing_someItems.json") as f:
# 	content = f.read()
# 	arr_json = json.loads(content)
# 	interactions = arr_json['int']
# 	impressions = arr_json['imp']
# 	user = arr_json['user']
# 	itemset = arr_json['items']



	# comparable data calculation
	# ----------------------------------


	# prepare for nomalization: reduction process
	# ----------------------------------
	title_cluster = []
	tag_cluster = []


	for key, value in interactions.items():
		key = str(key)
		if int(value) != 4: #relevant item id
			if key not in itemset:
				continue
			item = itemset[key]
			pieces_title = str(item['title']).split(",")
			title_cluster = title_cluster + pieces_title

			pieces_tags = str(item['title']).split(",")
			tag_cluster = tag_cluster + pieces_tags



	seenTitles = calOccurenceRank(title_cluster)
	seenTags = calOccurenceRank(tag_cluster)



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
		feat_arr = normalizeItemFeatures(item,seenTitles,seenTags)
		X.append(feat_arr)
		items_int.append(key)
		if value == 4:
			value = 0
		elif value == 3:
			value = 9
		elif value == 2:
			value = 8
		elif value == 1:
			value = 6
		Y.append(value)

	# impressions

	impressions = list(set(impressions))
	impressions_reduced = list(set(impressions) - set(items_int))

	for key in impressions_reduced:
		
		if key not in itemset:
			continue

		item = itemset[key]
		feat_arr = normalizeItemFeatures(item,seenTitles,seenTags)
		X.append(feat_arr)
		Y.append(1)


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
		# preprocess items 
		x = []
		x_ids = []
		count= 0
		with open(DATAPATH+'/active_items.csv','rb') as f:
			reader = csv.reader(f, delimiter='\t')
			for row in reader:
				if count>1:
					userinfo = userset[str(user)]
					# simple filtering condition
					# if str(userinfo['discipline_id']) == str(row[3]):
					tmpItem = {}
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
					feat_arr = normalizeItemFeatures(tmpItem,seenTitles,seenTags)
					x.append(feat_arr)
					x_ids.append(row[0])
				count += 1

		# SVM

		svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
		y = svr_rbf.fit(X, Y).predict(x)
		y = y.tolist()

		# making pair
		itemscore = []
		for i in xrange(0,len(x)):
			itemscore.append([x_ids[i],y[i]])
			
		itemscore_sorted = sorted(itemscore,key=lambda x: x[1], reverse=True)


		recommended_itemsSet = itemscore_sorted[:31]
		recommended_items = []
		for tmpItem in recommended_itemsSet:
			recommended_items.append(tmpItem[0])

		

		yy = ",".join(recommended_items)
		outputline = str(user)+"\t"+yy
		output.append(outputline)



		maincounter += 1
		if maincounter % 10 == 0:
			with open(DATAPATH+'/solution_svm.csv', 'a') as f:
				for line in output:
					f.write(str(line)+"\n")

			output = []
			print str(maincounter),' of ',len(target_user_ids),' processed ...'



# write final solutions
# ------------

with open(DATAPATH+'/solution_svm.csv', 'a') as f:
	# f.write("userid\titems\n")
	for line in output:
		f.write(str(line)+"\n")

print "all processes terminated ..."