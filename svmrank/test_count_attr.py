'''
Personal test file, not relevant
'''
import csv
import time
import datetime
import os

import linecache


start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data/original'

arr_activeItems = []
arr_disactiveItems = []

header = ""

count = 0
itemcount = 0
titles = {}
tags = {}
with open(DATAPATH+'/items.csv','r') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
			#write file
		elif count>1:
			tmpTitle = row[1]
			titleset = tmpTitle.split(",")
			for aTitle in titleset:
				titles[aTitle] = 1
				

			tmpTag = row[10]
			tagset = tmpTag.split(",")
			for aTag in tagset:
				tags[aTag] = 1

			# 	itemcount += 1
		count += 1

print "total items: ", itemcount, 'titles: ',len(titles),' tages:', len(tags)



print("--- %s seconds ---" % (time.time() - start_time))