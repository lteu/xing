import csv
import time

import datetime
import linecache


start_time = time.time()


# array element test
#----------------------------------

# a = [1,3,5]
# b = [2,4,5]

# c = a+b
# print c
# print datetime.datetime.fromtimestamp(float(1446131843)).strftime('%W')


a = ["hello"]
# b = ["bello","hello"]
b = ["bello","hello"]

# print len(set(b).intersection(set(a)))

if not set(a).isdisjoint(b):
	print 'yes'
else:
	print 'no'

# ct = 0
# with open('data/impressions.csv','rb') as f:
# with open('data/interactions.csv','rb') as f:
# 	reader = csv.reader(f)
# 	for row in reader:
# 		# print row
# 		# ct += 1
# 		if line == 1000235:
# 			print row
# 		# if ct >100:
# 			# break

# print ct,' records'

# lines=[1000235]
# i=0
# f=open('data/original/interactions.csv')
# for line in f:
#     if i >0 :
#         print line
#     i+=1

# x = linecache.getline('data/interactions.csv', 1000235)

# arr  =  []
# arr = arr[:100]
# print arr

# for n,line in enumerate(open("data/interactions.csv")):
#     if n+1 in [1000235]: # or n in [25,29] 
#        print line.rstrip()
       
print("--- %s seconds ---" % (time.time() - start_time))



# #Import Library
# from sklearn import svm
# #Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# # Create SVM classification object 
# model = svm.SVC(kernel='linear', c=1, gamma=1) 
# # there is various option associated with it, like changing kernel, gamma and C value. Will discuss more # about it in next section.Train the model using the training sets and check score
# model.fit(X, y)
# model.score(X, y)
# #Predict Output
# predicted= model.predict(x_test)