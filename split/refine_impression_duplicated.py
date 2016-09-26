import csv
import time
import datetime
import os
import sys

csv.field_size_limit(sys.maxsize)
start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


header = ""
# week = 41


B = []

count = 0
path_input = DATAPATH+'/impressions/week41b.csv'
print path_input
with open(path_input, 'rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
		elif count>1:
			items = row[3].split(",")
			setOfItems = set(items)
			row[3] = ','.join(setOfItems)
			B.append("\t".join(row))
			# sys.exit()
		count += 1

count = 0
path_input = DATAPATH+'/impressions/week42b.csv'
print path_input
with open(path_input, 'rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count>1:
			items = row[3].split(",")
			setOfItems = set(items)
			row[3] = ','.join(setOfItems)
			B.append("\t".join(row))
			# sys.exit()
		count += 1

count = 0
path_input = DATAPATH+'/impressions/week43b.csv'
print path_input
with open(path_input, 'rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count>1:
			items = row[3].split(",")
			setOfItems = set(items)
			row[3] = ','.join(setOfItems)
			B.append("\t".join(row))
			# sys.exit()
		count += 1

count = 0
path_input = DATAPATH+'/impressions/week44b.csv'
print path_input
with open(path_input, 'rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count>1:
			items = row[3].split(",")
			setOfItems = set(items)
			row[3] = ','.join(setOfItems)
			B.append("\t".join(row))
			# sys.exit()
		count += 1


print 'writing ...'


with open(DATAPATH+'/impressions/week-41-42-43-44c.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in B:
		f.write(str(row)+"\n")

print("--- %s seconds ---" % (time.time() - start_time))