import csv
import time
import datetime
import os
import random
import sys


start_time = time.time()


number_of_target_users = 500
if len(sys.argv) > 1: 
	arg = sys.argv[1]
	number_of_target_users = int(arg)
	number_of_target_users += 1


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


# load target users

linecount = 0
target_users_id = []
with open(DATAPATH+'/test/target_users.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if linecount > 0:
			target_users_id.append(row[0])
		linecount += 1

print 'target users loaded ... ', len(target_users_id)


small_userset = []
for i in xrange(1,number_of_target_users):
	userid = random.choice(target_users_id)
	small_userset.append(userid)
	target_users_id.remove(userid)

	# print userid, 'size',len(target_users_id)


with open(DATAPATH+'/test/target_users_small.csv', 'w') as f:
	f.write(str('user_id')+"\n")
	for row in small_userset:
		f.write(str(row)+"\n")


print 'done ',len(small_userset),' users written'




print("--- %s seconds ---" % (time.time() - start_time))