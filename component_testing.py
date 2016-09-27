import csv
import time
import os
import sys
import random
import operator
import datetime

import json
import numpy as np 

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

start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-1]
DATAPATH = '/'.join(in_path) + '/data'


# dic = loadImpressionsDictByFilename('week-40-41-42-43c.csv')


dic = loadInteractionsByWeeks([40,41,42,43])


print len(dic.keys())

print dic['131843']




# arr_merged = {"345512":5,"8812":4,"63412":1,"512":7,"45512":8}


# sorted_arr_merged = sorted(arr_merged.items(), key=operator.itemgetter(1)) 
# # arr = sorted_arr_merged[:,0]
# arr = np.array(sorted_arr_merged)[:,0]
# print arr

# outputLine = ",".join(arr)

# print outputLine

# def overlapping(set1,set2):
	
# 	set1 = set1.strip()
# 	set2 = set2.strip()
# 	if set1 == "" or set2 == "":
# 		return 0
	
# 	piece1 = set1.split(",")
# 	piece2 = set2.split(",")

# 	return len(set(piece1) & set(piece2))




# s1 = '3,5,8,12,93,1'
# s2 = '93,5,6,1,12,3'

# print overlapping(s1,s2)

print("--- %s seconds ---" % (time.time() - start_time))



