# simple prediction, source: http://stackoverflow.com/questions/24517858/time-series-forecasting-with-support-vector-regression

'''
svmrank generated results to solution file
'''

import csv
import time
import os
import sys
import datetime
import os.path
import itertools

import numpy as np

# from collections import Counter


from func import *



# =====================================
# - - - MAIN - - - 
# =====================================

start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'
result_out_file ='solution_svmrank_srn0.01.csv'
result_in_path =  DATAPATH+"/result0.01/"

target_user_ids = loadTargetUserIDs('target/target_users_1000.csv',DATAPATH)

output = []

# load test file
testfile_path = DATAPATH+"/testdata/testset.dat"
testlines = [line.rstrip('\n') for line in open(testfile_path)]


for user in target_user_ids:
	arr = []
	
	resfile_path = result_in_path+str(user)+"_result.dat"
	if os.path.exists(resfile_path):
		# load results
		reslines = [line.rstrip('\n') for line in open(resfile_path)]

		# make pairs
		for idx in xrange(0,len(testlines)):
			testln = testlines[idx]
			pieces = testln.split("#")
			dataid = pieces[1].strip()
			datascore = reslines[idx]
			tmpPair = [dataid,float(datascore)]
			arr.append(tmpPair)

		# sort pairs
		arr.sort(key=lambda x: x[1],reverse=True)

		# take first 30 items
		a = np.array(arr)
		top30 = a[:30,0]

		# save solution
		yy = ",".join(top30)
		outputline = str(user)+"\t"+yy
		output.append(outputline)

		print user

# write solution file
with open(DATAPATH+'/solution/'+result_out_file, 'w') as f:
	f.write("userid\titems\n")
	for line in output:
		f.write(str(line)+"\n")
	


print "all processes terminated ..."
print("--- %s seconds ---" % (time.time() - start_time))