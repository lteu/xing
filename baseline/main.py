import csv
import time
import os

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
	liveItemCount = 0
	items = []
	with open(DATAPATH+'/active_items.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:	
			if linecount > 0:
				if int(row[12]) == 1:
					tmpItem = {}

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
					items.append(tmpItem)

					liveItemCount += 1

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

def roleBasedEvaluation(user,item,arr):
	weight = 3
	arraySize = 100
	userjobroles = user['jobroles']
	itemtitles = item['title']
	overlapScore = weight * overlapping(userjobroles,itemtitles)
	if not arr:
		jobItem = {"id":item['id'],"score":overlapScore}
		arr.append(jobItem)
	else:
		counter = 0
		for job in arr:
			if job["score"] < overlapScore:

				jobItem = {"id":item['id'],"score":overlapScore}
				arr.insert(counter, jobItem)
				if len(arr) >= arraySize:
					arr = arr[:-1]

				break
			
			counter += 1
	
	return arr


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

		if linecount >100:
			break

		linecount += 1


print "users loaded ..."
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
	# no jobrole
	if int(user['jobroles']) != 0:
		for item in items:
			arr_role_based = roleBasedEvaluation(user,item,arr_role_based)

	#job role based 

	#job robe tags based

	#discipline and region based

	# industry and region based

	#score aggregation




	maincounter += 1
	# print liveItemCount
	if maincounter == 5:
		break # testing 1 user

	print user['jobroles']
	print arr_role_based
	print ' '
	





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