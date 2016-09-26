import csv
import time
import os

# main scoring function: 
def score(S, T):
	score = 0.0
	count = 0
	for a in T:
		u = str(a[0])
		t = a[1]
		if u in S:
			r = S[u] #//r = ordered list of recommended items for user u
			tmpScore =   20 * (precisionAtK(r, t, 2) + precisionAtK(r, t, 4) + recall(r, t) + userSuccess(r, t)) + 10 * (precisionAtK(r, t, 6) + precisionAtK(r, t, 20))
			score += tmpScore
			# if tmpScore > 0:
			# 	print 'user:', u, ' t:', t, ' r:', r
		count += 1

	return score

#//precision within the first top k items: 
def precisionAtK(recommendedItems, relevantItems, k):
  topK = recommendedItems[:k] #//takes first k items from the list of reccommendedItems
  intersectedItems = set(topK).intersection(relevantItems)
  return len(intersectedItems) / k


#//recall = fraction of relevant, retrieved items (30 items 
#//are allowed to be submitted at maximum per user): 
def recall(recommendedItems, relevantItems):
	if len(relevantItems) > 0:
  		top30 = recommendedItems[:30]
  		intersectedItems = set(top30).intersection(relevantItems)
    	return len(intersectedItems) / len(relevantItems)
  	return 0.0


#//user success = was at least one relevant item recommended for a given user?
def userSuccess(recommendedItems, relevantItems):
	top30 = recommendedItems[:30]
	intersectedItems = set(top30).intersection(relevantItems)
	if len(intersectedItems) > 0:
		return 1.0 
	return 0.0



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
with open(DATAPATH+'/solution/solution_file_example.csv','rb') as f:
# with open(DATAPATH+'/solution/solution.csv','rb') as f:	
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

val = score(S, T)
print val


print("--- %s seconds ---" % (time.time() - start_time))

