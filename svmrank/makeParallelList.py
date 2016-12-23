'''
For parallel exec
'''
import csv
import time
import datetime
import os

from func import *


start_time = time.time()
in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


target_user_ids = loadTargetUserIDs('target/target_users_1000.csv',DATAPATH)

print len(target_user_ids)


with open(DATAPATH+'/parallel.txt', 'w') as f:
	for line in target_user_ids:
		f.write(str(line)+"\n")

print("--- %s seconds ---" % (time.time() - start_time))