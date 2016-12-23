'''
Definition of a proposed intuitive metric 'cover'
and the official metric 'score'
'''

import csv
import time
import os


# =============================================================
# =============================================================
# - OFFICIAL METRICS -
# =============================================================
# =============================================================


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
# - COVER -
# =============================================================
# =============================================================

# the coverage of recommended items and ground items
def score_simple(S, T):
	score = 0.0
	count = 0
	total = 0
	execount = 0

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
				# print 'user ',u,' intsct ',num_intersected,' ground',num_ground,' percentage ', percentage
				total += percentage

				# if percentage < 0.3:
				# 	print '---------------------'
				# 	print 'recommended ', set(r)
				# 	print 'ground ', set(t)
				# 	print 'intersected ',intersectedItems
				# 	print '---------------------'

				count += 1
		# execount = execount + 1

	return total/count

