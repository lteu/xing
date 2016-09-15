import csv
import time
import operator
import numpy as np 

start_time = time.time()


arr_merged = {"345512":5,"8812":4,"63412":1,"512":7,"45512":8}


sorted_arr_merged = sorted(arr_merged.items(), key=operator.itemgetter(1)) 
# arr = sorted_arr_merged[:,0]
arr = np.array(sorted_arr_merged)[:,0]
print arr

outputLine = ",".join(arr)

print outputLine

# def overlapping(set1,set2):
	
# 	set1 = set1.strip()
# 	set2 = set2.strip()
# 	if set1 == "" or set2 == "":
# 		return 0
	
# 	piece1 = set1.split(",")
# 	piece2 = set2.split(",")

# 	return len(set(piece1) & set(piece2))




# s1 = '3,5,8,12,93,1'
# s2 = '93,5,6,1,12,3'

# print overlapping(s1,s2)

print("--- %s seconds ---" % (time.time() - start_time))



