import csv
import time
import os


# ------- functions -----------

def getProfileByUserID(userid):
	linecount = 0
	user = {}
	with open(DATAPATH+'/users.csv','r') as f:
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
			
def getSpecificActiveItem(itemid):
	linecount =0
	# with open(DATAPATH+'/active_items.csv','r') as f:
	with open(DATAPATH+'/active_items.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		tmpItem = {}
		for row in reader:	
			if linecount > 0:
				
				tmpitemID = row[0]
				
				if int(itemid) == int(tmpitemID):
					print tmpitemID,' ',itemid

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
					# break
			linecount += 1
	return tmpItem


in_path = os.path.realpath(__file__).split('/')[:-1]
DATAPATH = '/'.join(in_path) + '/data'



start_time = time.time()


# test a specific item
aUser = getProfileByUserID(24800)
anItem = getSpecificActiveItem(1978491)
# anItem = getSpecificActiveItem(2835127)



print aUser
print anItem
# test a specific user

print("--- %s seconds ---" % (time.time() - start_time))

