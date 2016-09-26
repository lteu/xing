import csv
import time
import os

# main scoring function: 
def score(S, T):
	score = 0.0
	count = 0
	total = 0


	for a in T:
		u = str(a[0])
		t = set(a[1])
		if u in S:
			r = S[u] #//r = ordered list of recommended items for user u


			# print 
			intersectedItems = set(r).intersection(t)
			num_intersected = float(len(intersectedItems))
			num_ground = float(len(t))
			# print intersectedItems
			if len(t) != 0 :
				percentage = round(num_intersected / num_ground,2)
				# print 'intsct ',num_intersected,' ground',num_ground,' percentage ', percentage
				total += percentage

				# if percentage != 1.0:
				# 	print set(t)
				# 	print t
				# 	print intersectedItems

				count += 1
	return total/count

def score_simple(S, T):
	score = 0.0
	count = 0
	total = 0


	for a in T:
		u = str(a[0])
		t = set(a[1])
		if u in S:
			r = S[u] #//r = ordered list of recommended items for user u


			# print u
			intersectedItems = set(r).intersection(t)
			num_intersected = float(len(intersectedItems))
			num_ground = float(len(t))
			# print intersectedItems
			if len(t) != 0 :
				percentage = round(num_intersected / num_ground,2)
				# print 'intsct ',num_intersected,' ground',num_ground,' percentage ', percentage
				total += percentage

			# 	# if percentage != 1.0:
			# 	# 	print set(t)
			# 	# 	print t
			# 	# 	print intersectedItems

				count += 1
	return total/count
	# return 5

# =============================================================
# =============================================================
# - MAIN -
# =============================================================
# =============================================================


start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


# loading S
# =============================================================
S={}
linecount = 0
# with open(DATAPATH+'/solution/solution_file_example.csv','rb') as f:
with open(DATAPATH+'/solution/solution_svm.csv','rb') as f:
	reader = csv.reader(f,delimiter='\t')
	for row in reader:
		if linecount > 0:
			S[row[0]] = row[1].split(",")
		linecount += 1

# S['1115833'] = ['1119495','2791339','343377']


# loading T
# =============================================================
T_dic = {}
linecount = 0
with open(DATAPATH+'/ground/interactions_week45.csv','rb') as f:

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


# compute score
# =============================================================

# val = score(S, T)

val = score_simple(S, T)
print 'val finale:',val


print("--- %s seconds ---" % (time.time() - start_time))

