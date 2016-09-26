import csv
import time
import datetime

import linecache


start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

count = 0

header = ""


A = {}
for x in xrange(0,46):
	A[x] = []

with open(DATAPATH+'/original/interactions.csv','rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
			#write file
		elif count>1:
			# temp = datetime.datetime.fromtimestamp(float(row[3])).strftime('%Y-%m-%d')
			temp = datetime.datetime.fromtimestamp(float(row[3])).strftime('%W')
			A[int(temp)].append("\t".join(row))

		count += 1

arr_tmp = A[34]
with open(DATAPATH+'/interactions/week'+str(34)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")


arr_tmp = A[35]
with open(DATAPATH+'/interactions/week'+str(35)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[36]
with open(DATAPATH+'/interactions/week'+str(36)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[37]
with open(DATAPATH+'/interactions/week'+str(37)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[38]
with open(DATAPATH+'/interactions/week'+str(38)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[39]
with open(DATAPATH+'/interactions/week'+str(39)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[40]
with open(DATAPATH+'/interactions/week'+str(40)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[41]
with open(DATAPATH+'/interactions/week'+str(41)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[42]
with open(DATAPATH+'/interactions/week'+str(42)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[43]
with open(DATAPATH+'/interactions/week'+str(43)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[44]
with open(DATAPATH+'/interactions/week'+str(44)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

arr_tmp = A[45]
with open(DATAPATH+'/interactions/week'+str(45)+'.csv', 'w') as f:
	f.write(str(header)+"\n")
	for row in arr_tmp:
		f.write(str(row)+"\n")

print("--- %s seconds ---" % (time.time() - start_time))