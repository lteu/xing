import csv
import time


import linecache


start_time = time.time()

# main scoring function: 
def score(S, T):
  score = 0.0
  for u,t in T: #//t = set of relevant items for user u
    r = S(u) #//r = ordered list of recommended items for user u
    score +=   20 * (precisionAtK(r, t, 2) + precisionAtK(r, t, 4) + recall(r, t) + userSuccess(r, t)) 
             + 10 * (precisionAtK(r, t, 6) + precisionAtK(r, t, 20))

  return score

#//precision within the first top k items: 
def precisionAtK(recommendedItems, relevantItem, k):
  topK = recommendedItems[:k] #//takes first k items from the list of reccommendedItems
  intersectedItems = set(topK).intersection(relevantItems)
  return len(intersectedItems) / k


#//recall = fraction of relevant, retrieved items (30 items 
#//are allowed to be submitted at maximum per user): 
def recall(recommendedItems, relevantItem):
	if len(relevantItems) > 0:
  		top30 = recommendedItems[:30]
  		intersectedItems = set(top30).intersection(relevantItems)
    	return len(intersectedItems) / len(relevantItems)
  	else 
    	return 0.0


#//user success = was at least one relevant item recommended for a given user?
def userSuccess(recommendedItems, relevantItem):
	top30 = recommendedItems[:30]
	intersectedItems = set(top30).intersection(relevantItems)
	if (len(intersectedItems) > 0)
    	return 1.0
 	else 
    	return 0.0


       
print("--- %s seconds ---" % (time.time() - start_time))

