import csv
import time
import datetime
import os
import sys

start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


header = ""
week = 40


# load target users

linecount = 0
target_users_id = {}
with open(DATAPATH+'/target/target_users.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if linecount > 0:
			target_users_id[str(row[0])] = 1
		linecount += 1


print 'target users loaded ...'

B = []

count = 0

print DATAPATH+'/interactions/week'+str(week)+'.csv'
with open(DATAPATH+'/interactions/week'+str(week)+'.csv', 'rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		# print  'hello'
		if count==0:

			header = "\t".join(row)
			#write file
		elif count>1:
			# print  'hello'
			if str(row[0]) in target_users_id:
				B.append("\t".join(row))

		if count%100000 == 0:
			print count, 'lines processed ...'
			# if count != 0:
			# 	break
		count += 1


print 'writing ...'


with open(DATAPATH+'/interactions/week'+str(week)+'b.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in B:
		f.write(str(row)+"\n")


print("--- %s seconds ---" % (time.time() - start_time))