import csv
import time
import datetime
import os

start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


# load target users
linecount = 0
filename = "target/target_users_1000.csv"
target_users_id = []
with open(DATAPATH+'/'+filename,'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if linecount > 0:
			target_users_id.append(row[0])
		linecount += 1


numberofuser = 1
with open(DATAPATH+'/target/target_users_'+str(numberofuser)+'.csv', 'w') as f:
	f.write(str('user_id')+"\n")
	count = 1
	for row in target_users_id:
		f.write(str(row)+"\n")
		if count == numberofuser:
			break
		count = count + 1



print("--- %s seconds ---" % (time.time() - start_time))