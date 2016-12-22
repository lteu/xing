import csv
import time
import datetime

import linecache


start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

arr_activeItems = []
arr_disactiveItems = []

header = ""

count = 0
itemcount = 0
with open(DATAPATH+'/items.csv','r') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
			#write file
		elif count>1:
			active_during_test = row[12]

			if int(active_during_test) == 1:
				arr_activeItems.append("\t".join(row))
				itemcount += 1
			elif int(active_during_test) == 0:
				arr_disactiveItems.append("\t".join(row))
				itemcount += 1
		count += 1

print "total items: ", itemcount


count1 = 0
with open(DATAPATH+'/active_items.csv', 'w') as f:
    f.write(str(header)+"\n")
    for row in arr_activeItems:
    	f.write(str(row)+"\n")
    	count1 += 1
print "active items : ", count1


count2 = 0
with open(DATAPATH+'/disactive_items.csv', 'w') as f:
    f.write(str(header)+"\n")
    for row in arr_disactiveItems:
    	f.write(str(row)+"\n")
    	count2 += 1
print "disactive items : ", count2



print("--- %s seconds ---" % (time.time() - start_time))

