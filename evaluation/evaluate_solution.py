'''
Evaluate a solution by intuitive metric 'cover'
and the official metric 'score'
'''

import csv
import time
import os

from metrics import *
# =============================================================
# =============================================================
# - MAIN -
# =============================================================
# =============================================================


start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'

solution_file_name = 'solution_svmrank_130.csv'
solution_file_path = DATAPATH+'/solution/'+solution_file_name

ground_file_path = DATAPATH+'/ground/interactions_week44.csv'

# loading S
# =============================================================
S={}
linecount = 0
with open(solution_file_path,'rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0:
			S[row[0]] = row[1].split(",")
		linecount += 1

print 'solution loaded file: ',solution_file_path

# loading T
# =============================================================
T_dic = {}
linecount = 0
with open(ground_file_path,'rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0:
			userid = row[0]
			itemid = row[1]
			interaction = row[2]
			if int(interaction) == 1 or int(interaction) == 2 or int(interaction) == 3:
				if not  userid in T_dic or T_dic[userid] == None:
					T_dic[userid] = [itemid]
				else:
					tmpArr = T_dic[userid]
					tmpArr.append(itemid)
					T_dic[userid] = tmpArr
		linecount += 1
T = []
for userid, items in T_dic.iteritems():
	T.append([userid,items])

print 'ground loaded', ground_file_path

# compute score
# =============================================================

val = score(S, T)
print 'solution score:',val

val = score_simple(S, T)
print 'solution cover:',val



print("--- %s seconds ---" % (time.time() - start_time))

