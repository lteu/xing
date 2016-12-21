'''


This checks effectively how the recommendation is going on
for a specific user


'''

import csv
import time
import os


def loadItems():
	itemset ={}
	count= 0
	# with open(DATAPATH+'/target/active_items.csv','rb') as f:
	with open(DATAPATH+'/original/items.csv','rb') as f:

		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
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
				tmpItem['active'] = row[12]
				itemset[str(row[0])] = tmpItem
			count += 1
	return itemset

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

# =============================================================
# =============================================================
# - MAIN -
# =============================================================
# =============================================================


start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

itemset = loadItems()
users = loadTargetUsersWithProfile()

user = 131843


# loading I
# =============================================================
I = []
linecount = 0
with open(DATAPATH+'/interactions/week43b.csv','rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0 and int(row[0]) == user:
			itemid = row[1]
			interaction = row[2]
			if int(interaction) == 1 or int(interaction) == 2 or int(interaction) == 3:
				I.append(itemid)
		linecount += 1

linecount = 0
with open(DATAPATH+'/interactions/week42b.csv','rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0 and int(row[0]) == user:
			itemid = row[1]
			interaction = row[2]
			if int(interaction) == 1 or int(interaction) == 2 or int(interaction) == 3:
				I.append(itemid)
		linecount += 1

linecount = 0
with open(DATAPATH+'/interactions/week41b.csv','rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0 and int(row[0]) == user:
			itemid = row[1]
			interaction = row[2]
			if int(interaction) == 1 or int(interaction) == 2 or int(interaction) == 3:
				I.append(itemid)
		linecount += 1


# loading S
# =============================================================
S=[]
linecount = 0
# with open(DATAPATH+'/solution/solution_file_example.csv','rb') as f:
with open(DATAPATH+'/solution/solution_svm.csv','rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0 and int(row[0]) == user:
			S = row[1].split(",")
			break
		linecount += 1

# loading T
# =============================================================
T = []
linecount = 0
with open(DATAPATH+'/ground/interactions_week44.csv','rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0 and int(row[0]) == user:
			itemid = row[1]
			interaction = row[2]
			if int(interaction) == 1 or int(interaction) == 2 or int(interaction) == 3:
				T.append(itemid)
		linecount += 1



print len(T)

output_i = ""
output_t = ""
output_s = ""
for x in xrange(0,15):
	if x < len(I) -1:
		i = I[x]
		if i in itemset:
			output_i += str(itemset[i])+"\n"

	if x < len(T) -1:
		t = T[x]
		if t in itemset:
			output_t += str(itemset[t])+"\n"
	
	if x < len(S) -1  and t in itemset:
		s = S[x]
		if s in itemset:
			output_s += str(itemset[s])+"\n"


print 'user info'
print users[str(user)]

print 'interaction'
print output_i

print 'solution'
print output_s

print 'ground'
print output_t
# compute score
# =============================================================

# val = score(S, T)

# val = score_simple(S, T)
# print 'val finale:',val


print("--- %s seconds ---" % (time.time() - start_time))

