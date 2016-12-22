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
	line = featureToLine(tmpItem,value,set_ID,activeItemID)
	test_data.append(line)



with open(DATAPATH+'/datafeatureid.json', 'w') as fp:
    json.dump(set_ID, fp)

# test_file = str(user)+"_test_reduce.dat"
with open(DATAPATH+'/testdata/testset.dat', 'w') as f:
	for line in test_data:
		f.write(str(line)+"\n")
	

print 'actitems ',len(itemset_active),' testdata ',len(test_data)



print("--- %s seconds ---" % (time.time() - start_time))