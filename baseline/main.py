import csv
import time
import os
import sys
import random

import linecache


def getProfileFromUserID(userid):
	linecount = 0
	user = {}
	with open(DATAPATH+'/users.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:

			if linecount > 0:
				if int(row[0]) == int(userid):
					print row
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
					break
			
			linecount += 1

	return user
			


def loadActiveItems():
	# get relevant items
	linecount =0
	# liveItemCount = 0
	items = {}
	with open(DATAPATH+'/active_items.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:	
			if linecount > 0:
				if int(row[12]) == 1:
					tmpItem = {}

					itemID = row[0]
					tmpItem['id'] = row[0]
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
					tmpItem['created_at'] = row[11]
					tmpItem['active_during_test'] = row[12]

					items[itemID] = tmpItem
					# items.append(tmpItem)

					# liveItemCount += 1

			linecount += 1
	return items

#-------------------------
#	evaluation func
#-------------------------

def overlapping(set1,set2):
	
	set1 = set1.strip()
	set2 = set2.strip()
	if set1 == "" or set2 == "":
		return 0
	
	piece1 = set1.split(",")
	piece2 = set2.split(",")

	counter = 0
	for i in piece1:
		if i in piece2:
			counter += 1

	# if counter != 0:
	# 	print set1,' ',set2
	# 	print counter

	return counter


def evaluateOverlap(arr,usertext,itemtext,itemid,weight):
	arraySize = 100
	hasAdded = False
	score = weight * overlapping(usertext,itemtext)
	if score >0:
		jobItem = {"id":itemid,"score":score}

		if not arr or len(arr) < arraySize:
			
			arr.append(jobItem)
			hasAdded = True
		else:
			counter = 0
			for job in arr:
				if job["score"] < score:
					arr.insert(counter, jobItem)
					hasAdded = True
					if len(arr) >= arraySize:
						arr = arr[:-1]

				break
				counter += 1
			
			if not hasAdded and len(arr) < arraySize:
				arr.append(jobItem)

			
	return arr

def evaluateMatching(arr,itemid,weight):
	arraySize = 100
	hasAdded = False

	jobItem = {"id":itemid,"score":weight}
	if not arr:
		arr.append(jobItem)
		hasAdded = True
	else:
		for job in arr:
			if job['id'] == itemid:
					return arr # already inserted

	if not hasAdded and len(arr) < arraySize:
		arr.append(jobItem)

	return arr




def mergeResult(arr_x_based, user, items, arr_merged):
	for x in arr_x_based:
		tmpId = x['id']
		tmpScore = int(x['score'])

		item = items[tmpId]
		userCareerLevel = user['career_level']

		if userCareerLevel == "0" or userCareerLevel == "NULL":
			userCareerLevel = "3"

		if userCareerLevel == item['career_level']:
			if tmpId in arr_merged:
				arr_merged[tmpId] = tmpScore + arr_merged[tmpId]
			else:
				arr_merged[tmpId] = tmpScore
	return arr_merged

def filterJobsWithDiscipline(items,discipline,region):
	filtered_items = []
	for key, item in items.iteritems():
		if item['discipline_id'] == discipline and item['region'] == region:
			filtered_items.append(item)
	return filtered_items

def filterJobsWithIndu(items,indu,region):
	filtered_items = []
	for key, item in items.iteritems():
		if item['industry_id'] == indu and item['region'] == region:
			filtered_items.append(item)
	return filtered_items

# =============================================================
# - MAIN -
# =============================================================

start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

# ---------------
# LOADING : get test user
# ---------------


linecount = 0
users = []
with open(DATAPATH+'/test/target_users.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if linecount > 0:
			users.append(row[0])

		if linecount >10: #testing 10 users only
			break

		linecount += 1


print "test users loaded ..."
# print users

items = loadActiveItems()

print "items loaded ...", len(items)
# learn and predict

maincounter = 0
for userid in users:
	# get user profile
	print 'user: ' + userid
	user = getProfileFromUserID(userid)
	print user

	arr_role_based =[]
	arr_tag_based = []
	arr_disp_based = []
	arr_indu_based = []

	# job role based 
	if user['jobroles'] != "0":
	
		# job role title based
		# for key, item in items.iteritems():
		# 	usertext = user['jobroles']
		# 	itemtext = item['title']
		# 	itemid = item['id']
		# 	weight = 3
		# 	arr_role_based = evaluateOverlap(arr_role_based,usertext,itemtext,itemid,weight)

		# print len(arr_role_based)
		# print ''
		print ''
	

		# job role tags based
		# for key, item in items.iteritems():
		# 	usertext = user['jobroles']
		# 	itemtext = item['tags']
		# 	itemid = item['id']
		# 	weight = 2
		# 	arr_tag_based = evaluateOverlap(arr_tag_based,usertext,itemtext,itemid,weight)

	# 	# print arr_tag_based

	# # discipline and region based
	# if user['discipline_id'] != "0":
		
	# 	discipline = user['discipline_id']
	# 	region = user['region']
	# 	filtered_items = filterJobsWithDiscipline(items,discipline,region)
	# 	while len(arr_disp_based) < 100 and len(filtered_items)>0:
	# 		item = random.choice(filtered_items)
	# 		itemid = item['id']
	# 		weight = 2
	# 		arr_disp_based = evaluateMatching(arr_disp_based,itemid,weight)
	# 		filtered_items.remove(item)
			# print 'arrlen: ',len(arr_disp_based), ' itemid:', itemid


	# # industry and region based
	if user['industry_id'] != "0":

		industry_id = user['industry_id']
		region = user['region']
		filtered_items = filterJobsWithIndu(items,industry_id,region)
		while len(arr_indu_based) < 100 and len(filtered_items)>0:
			item = random.choice(filtered_items)
			itemid = item['id']
			weight = 1
			arr_indu_based = evaluateMatching(arr_indu_based,itemid,weight)
			filtered_items.remove(item)

			print 'arrlen: ',len(arr_indu_based), ' itemid:', itemid


	# # score aggregation
	print arr_indu_based
	arr_merged = {}
	arr_merged = mergeResult(arr_role_based, user, items, arr_merged)
	arr_merged = mergeResult(arr_tag_based, user, items, arr_merged)
	arr_merged = mergeResult(arr_disp_based, user, items, arr_merged)
	arr_merged = mergeResult(arr_indu_based, user, items, arr_merged)

	maincounter += 1

	print arr_merged

	print ' '

	# if maincounter == 20:
	# 	break # testing 1 user

# print ct,' records'

# lines=[1000235]
# i=0
# f=open('data/interactions.csv')
# for line in f:
#     if i in lines:
#         print line
#     i+=1

# x = linecache.getline('data/interactions.csv', 1000235)

# print x


# for n,line in enumerate(open("data/interactions.csv")):
#     if n+1 in [1000235]: # or n in [25,29] 
#        print line.rstrip()
       
print("--- %s seconds ---" % (time.time() - start_time))




# #Import Library
# from sklearn import svm
# #Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# # Create SVM classification object 
# model = svm.SVC(kernel='linear', c=1, gamma=1) 
# # there is various option associated with it, like changing kernel, gamma and C value. Will discuss more # about it in next section.Train the model using the training sets and check score
# model.fit(X, y)
# model.score(X, y)
# #Predict Output
# predicted= model.predict(x_test)