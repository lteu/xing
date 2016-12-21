import csv
import time
import datetime
import os
import linecache
import json

from func import *
start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

arr_activeItems = []
arr_disactiveItems = []

header = ""

count = 0
itemcount = 0
# with open(DATAPATH+'/original/items.csv','r') as f:
# 	reader = csv.reader(f, delimiter='\t')
# 	for row in reader:
# 		if count==0:
# 			header = "\t".join(row)
# 			#write file
# 		elif count>1:
# 			active_during_test = row[12]

# 			if int(active_during_test) == 1:
# 				arr_activeItems.append("\t".join(row))
# 				itemcount += 1
# 			elif int(active_during_test) == 0:
# 				arr_disactiveItems.append("\t".join(row))
# 				itemcount += 1
# 		count += 1

# print "total items: ", itemcount

itemset,itemset_active = loadItems(DATAPATH)

print 'item loaded'

userset = loadTargetUsersWithProfile(DATAPATH)

print 'target users loaded ... '

# target_user_ids = loadTargetUserIDs('target/target_users_small.csv')
target_user_ids = loadTargetUserIDs('target/target_users_1000.csv',DATAPATH)
# target_user_ids = loadTargetUserIDs('target/target_users.csv')

print 'user ids loaded ...'

dic_interactions = loadInteractionsByWeeks([40,41,42,43],DATAPATH)

print 'weekly interactions loaded'


dic_impressions = loadImpressionsDictByFilename("week-40-41-42-43c.csv",DATAPATH)

print "weekly impressions loaded"


#======= loaded =======


titles_collected = []
tags_collected = []
indu_collected = []
discipline_id_collected = []
title_collected = []
country_collected = []
region_collected = []

ucount = 0
for user in target_user_ids:
	interactions = {}
	impressions = []
	ucount = ucount + 1
	if ucount %20 == 0:
		print ucount
	
	if user in dic_interactions:
		interactions = dic_interactions[user]

	if user in dic_impressions:
		impressions =  dic_impressions[user]

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

print 'item features collected'

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


counter = 3
for key_pure, value_pure in set_pure.items():
	dic = {}
	for tmpEle in value_pure:
		dic[tmpEle] = counter
		counter = counter + 1
	set_ID[key_pure] = dic

print 'item features numbered'



test_data = []
active_count = 0
for activeItemID in itemset_active:
	tmpItem = itemset[activeItemID]
	value = 0
	line,output_dynam = featureToLine(tmpItem,value,set_ID)
	if output_dynam.strip() != "":
		test_data.append(line)
		active_count = active_count +1



with open(DATAPATH+'/datafeatureid.json', 'w') as fp:
    json.dump(set_ID, fp)

test_file = str(user)+"_test_reduce.dat"
with open(DATAPATH+'/testdata/'+test_file, 'w') as f:
	for line in test_data:
		f.write(str(line)+"\n")
	

print 'actitems ',len(itemset_active),' testdata ',len(test_data)

# count1 = 0
# with open(DATAPATH+'/active_items_sub.csv', 'w') as f:
#     f.write(str(header)+"\n")
#     for row in arr_activeItems:
#     	f.write(str(row)+"\n")
#     	count1 += 1
# print "active items : ", count1



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