'run this script then refine_impressions.py for duplication elimination'

import csv
import time
import datetime
import os
import linecache
import sys

csv.field_size_limit(sys.maxsize)
start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

count = 0

header = ""

week = 40

B = []
with open(DATAPATH+'/original/impressions.csv','rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
			#write file
		elif count>1:
			if int(row[2]) == week:
				B.append("\t".join(row))
		count += 1

with open(DATAPATH+'/impressions/week'+str(week)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in B:
		f.write(str(row)+"\n")


print("--- %s seconds ---" % (time.time() - start_time))