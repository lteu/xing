import csv
import time
import datetime
import os
import linecache
import sys

csv.field_size_limit(sys.maxsize)
start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-1]
DATAPATH = '/'.join(in_path) + '/data'

count = 0

header = ""

# week = 44

B = []
with open(DATAPATH+'/original/interactions.csv','rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count>1:
			week = datetime.datetime.fromtimestamp(float(row[3])).strftime('%W')
			if week not in B:
				B.append(week)
		count += 1

print B

print("--- %s seconds ---" % (time.time() - start_time))