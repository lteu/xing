'''

This basline script unfortunately could have several bugs :(

'''
import csv
import time
import os
import sys
import random
import operator

import numpy as np

#---------------------------------------------------------------
#	Loading functions
#---------------------------------------------------------------



# get user profile from CSV database by his ID O(n)
# ---------------------------------------------------------------
def getProfileByUserID(userid):
	linecount = 0
	user = {}
	with open(DATAPATH+'/original/users.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if linecount > 0:
				if int(row[0]) == int(userid):
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
			

# function that loads all target users with his profile items
# ---------------------------------------------------------------
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

# function that loads active items (pre-filtered) into a dictionary
# ---------------------------------------------------------------
def loadActiveItems():
	linecount =0
	items = {}
	with open(DATAPATH+'/target/active_items.csv','r') as f:
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
			linecount += 1
	return items



#---------------------------------------------------------------
#	evaluating functions
#---------------------------------------------------------------


def overlapping(set1,set2):
	
	set1 = set1.strip()
	set2 = set2.strip()
	if set1 == "" or set2 == "":
		return 0
	
	piece1 = set1.split(",")
	piece2 = set2.split(",")

	return len(set(piece1) & set(piece2)) #interction
	# return len(set(a).intersection(set(b)))


# evaluate preference overlap
#---------------------------------------------------------------
def evaluateOverlap(arr,usertext,itemtext,itemid,weight):
	arraySize = 100
	hasAdded = False
	score = weight * overlapping(usertext,itemtext)
	if score >0:
		jobItem = {"id":itemid,"score":score}

		if not arr: # initial array
			arr.append(jobItem)
			hasAdded = True
		else: # insert
			counter = 0
			for job in arr:
				if job["score"] <= score:
					shouldAdd = True if (random.random() < 0.5) else False
					if job["score"] < score or shouldAdd:
						arr.insert(counter, jobItem)
						hasAdded = True
						if len(arr) >= arraySize:
							arr = arr[:-1]
						break
				counter += 1
			
		if not hasAdded and len(arr) < arraySize: # append
			arr.append(jobItem)
	return arr

# evaluate matching
#---------------------------------------------------------------

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


#	score aggregation functions
#---------------------------------------------------------------

def mergeResult(arr_x_based, user, items, arr_merged):

	for arr_item in arr_x_based:

		tmpId = arr_item['id']
		tmpScore = int(arr_item['score'])

		item = items[tmpId]
		userCareerLevel = user['career_level']

		if userCareerLevel == "0" or userCareerLevel == "NULL": # requested by specification
			userCareerLevel = "3"

		if userCareerLevel == item['career_level']:
			if not arr_merged:
				arr_merged.append([tmpId,tmpScore])
			else:
				hasUpdated = False
				# for item_merged in arr_merged:
				for idx, val in enumerate(arr_merged):
					if val[0] == tmpId:
						arr_merged[idx][1] =arr_merged[idx][1]+tmpScore
						hasUpdated = True
				if not hasUpdated:
					arr_merged.append([tmpId,tmpScore])


			# if tmpId in arr_merged:
			# 	arr_merged[tmpId] = tmpScore + arr_merged[tmpId]
			# else:
			# 	arr_merged[tmpId] = tmpScore

	return arr_merged


#	job items filtering functions
#---------------------------------------------------------------

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


def column(matrix, i):
    return [row[i] for row in matrix]


# =============================================================
# =============================================================
# - MAIN -
# =============================================================
# =============================================================



start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'




# loading ...
# =============================================================

linecount = 0
users = []
with open(DATAPATH+'/target/target_users.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if linecount > 0:
			users.append(row[0])
		linecount += 1

# users = [2400,3700,6400,7100,8600,11000,12300,12400,12900,14500,20400,21500,24800,25000,27000,31400]
# users = [24800]


# print "test users loaded ..."

items = loadActiveItems()

# print "items loaded ...", len(items)

userset = loadTargetUsersWithProfile()

print "users profile loaded"



# write output file header
# =============================================================

header = "user_id\titems"
with open(DATAPATH+'/solution/solution_baseline.csv', 'w') as f:
	f.write(str(header)+"\n")


# learn and predict
# =============================================================

maincounter = 0
arr_solution_lines = []
for userid in users:
	userid = str(userid)
	user = userset[userid]

	arr_role_based =[]
	arr_tag_based = []
	arr_disp_based = []
	arr_indu_based = []

	# job role based 
	if user['jobroles'] != "0":
	
		#  -- job role title based  --
		for key, item in items.iteritems():
			usertext = user['jobroles']
			itemtext = item['title']
			itemid = item['id']
			weight = 3
			arr_role_based = evaluateOverlap(arr_role_based,usertext,itemtext,itemid,weight)

		# print 'job role title based done'
	
		# -- job role tags based
		for key, item in items.iteritems():
			usertext = user['jobroles']
			itemtext = item['tags']
			itemid = item['id']
			weight = 2
			arr_tag_based = evaluateOverlap(arr_tag_based,usertext,itemtext,itemid,weight)

		# print 'job role tags based done'

	# -- discipline and region based --
	if user['discipline_id'] != "0":
		
		discipline = user['discipline_id']
		region = user['region']
		filtered_items = filterJobsWithDiscipline(items,discipline,region)
		while len(arr_disp_based) < 100 and len(filtered_items)>0:
			item = random.choice(filtered_items)
			itemid = item['id']
			weight = 2
			arr_disp_based = evaluateMatching(arr_disp_based,itemid,weight)
			filtered_items.remove(item)


	# -- industry and region based --
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

	# score aggregation process

	arr_merged = []
	arr_merged = mergeResult(arr_role_based, user, items, arr_merged)
	arr_merged = mergeResult(arr_tag_based, user, items, arr_merged)
	arr_merged = mergeResult(arr_disp_based, user, items, arr_merged)
	arr_merged = mergeResult(arr_indu_based, user, items, arr_merged)

	arr_merged = sorted(arr_merged,key=lambda x: x[1])

	arr = column(arr_merged,0) # take only the item id sorted
	arr = arr[:35] # take only the first 35 items

	outputLine = userid+"\t"+",".join(arr)

	arr_solution_lines.append(outputLine)

	maincounter += 1
	if maincounter % 50 == 0:
		with open(DATAPATH+'/solution/solution_baseline.csv', 'a') as f:
			for line in arr_solution_lines:
				f.write(str(line)+"\n")

			arr_solution_lines = []
			print str(maincounter),' of ',len(users),' processed ...'



# write the last results
if len(arr_solution_lines) > 0:
	with open(DATAPATH+'/solution/solution_baseline.csv', 'a') as f:
		for line in arr_solution_lines:
			f.write(str(line)+"\n")

	arr_solution_lines = []
	print 'rest of results written ...'

	


print 'operations completed ...'
print("--- %s seconds ---" % (time.time() - start_time))
