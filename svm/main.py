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


csv.field_size_limit(sys.maxsize)


def getInteractionsByUserAndWeek(userid,numWeek):
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
	with open(DATAPATH+'/items.csv','rb') as f:

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
	with open(DATAPATH+'/items.csv','rb') as f:

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

def loadTargetUsersWithProfile():
	linecount =0
	users = {}
	with open(DATAPATH+'/target_users_profile.csv','r') as f:
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


def clusterToSortedList(cluster):
	title_cluster_dic =  Counter(cluster)
	arr_title = title_cluster_dic.items() 
	arr_title_sorted = sorted(arr_title,key=lambda x: x[1], reverse=True)
	arr_title = []
	for x in arr_title_sorted:
		arr_title.append(x[0])

	return arr_title

def estimateSimilarityScore(passtset,newset):
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


# itemset = loadItems()

# print 'items loaded'

# userset = loadTargetUsersWithProfile()

# print 'target users loaded'

# # for all users
# user = 2125784

# # writing process
# interactions = {}
# interactions_tmp = getInteractionsByUserAndWeek(user,41)
# interactions = dict(interactions.items() + interactions_tmp.items())

# interactions_tmp = getInteractionsByUserAndWeek(user,42)
# interactions = dict(interactions.items() + interactions_tmp.items())

# interactions_tmp = getInteractionsByUserAndWeek(user,43)
# interactions = dict(interactions.items() + interactions_tmp.items())

# interactions_tmp = getInteractionsByUserAndWeek(user,44)
# interactions = dict(interactions.items() + interactions_tmp.items())

# print 'weekly interactions loaded'


# impressions =  loadImpressions(user,41)
# impressions +=  loadImpressions(user,42)
# impressions +=  loadImpressions(user,43)
# impressions +=  loadImpressions(user,44)

# print "weekly impressions loaded"



# # generate pre-compiled data for a fast experimental access
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


with open(DATAPATH+"/testing_someItems.json") as f:
	content = f.read()
	arr_json = json.loads(content)
	interactions = arr_json['int']
	impressions = arr_json['imp']
	user = arr_json['user']
	itemset = arr_json['items']



# comparable data calculation
# ----------------------------------


# prepare for nomalization: reduction process
# ----------------------------------
title_cluster = []
tag_cluster = []


for key, value in interactions.items():
	key = str(key)
	if int(value) != 4: #relevant item id
		item = itemset[key]
		pieces_title = str(item['title']).split(",")
		title_cluster = title_cluster + pieces_title

		pieces_tags = str(item['title']).split(",")
		tag_cluster = tag_cluster + pieces_tags

	# 	tmp[] = item['career_level']
	# 	tmp[] = item['discipline_id']
	# 	tmp[] = item['industry_id']
	# 	tmp[] = item['country']
	# 	tmp[] = item['region']
	# 	tmp[] = item['latitude']
	# 	tmp[] = item['longitude'] 
	# 	tmp[] = item['employment']



	# 	tmp[] = item['tags'] #m



arr_title = clusterToSortedList(title_cluster)
arr_tags = clusterToSortedList(tag_cluster)

# training set normalization 
normalized_dic = {}


# print interactions
for key, value in interactions.items():
	item = itemset[key]

	feat_arr = []
	feat_arr.append(estimateSimilarityScore(arr_title,item['title'].split(",")))
	feat_arr.append(estimateSimilarityScore(arr_title,item['tags'].split(",")))
	feat_arr.append(int(item['career_level']))
	feat_arr.append(int(item['discipline_id']))
	feat_arr.append(int(item['industry_id']))
	feat_arr.append(convertCountryToCode(item['country']))
	feat_arr.append(int(item['region']))
	feat_arr.append(int(item['employment']))


	print feat_arr
	# row[2] = item['latitude']
	# row[2] = item['longitude']

	# sys.exit()
	
	# value normalization
	# result interpretation

normalized_features = []
normalized_results = []

# get not selected items ....


# for each week, associate user item entry and a label

# pass the data as training set

# predict user item of the next week



# X = np.arange(0,100)
# Y = np.sin(X)

# print X
# print Y

# a = 0
# b = 10
# x = []
# y = []
# while b <= 100:
#     x.append(Y[a:b])
#     a += 1
#     b += 1
# b = 10

# print x

# while b <= 90:
#     y.append(Y[b])
#     b += 1

# print y

# svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
# y_rbf = svr_rbf.fit(x[:81], y).predict(x)

# figure = plt.figure()
# tick_plot = figure.add_subplot(1, 1, 1)
# tick_plot.plot(X, Y, label='data', color='green', linestyle='-')
# tick_plot.axvline(x=X[-10], alpha=0.2, color='gray')
# tick_plot.plot(X[10:], y_rbf[:-1], label='data', color='blue', linestyle='--')
# plt.show()