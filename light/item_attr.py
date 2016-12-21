import csv
import time
import datetime
import os

import linecache


start_time = time.time()

in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data/original'

arr_activeItems = []
arr_disactiveItems = []

header = ""

count = 0
itemcount = 0
titles = {}
tags = {}
with open(DATAPATH+'/items.csv','r') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
			#write file
		elif count>1:
			tmpTitle = row[1]
			titleset = tmpTitle.split(",")
			for aTitle in titleset:
				titles[aTitle] = 1
				

			tmpTag = row[10]
			tagset = tmpTag.split(",")
			for aTag in tagset:
				tags[aTag] = 1

			# active_during_test = row[12]

			# if int(active_during_test) == 1:
			# 	arr_activeItems.append("\t".join(row))
			# 	itemcount += 1
			# elif int(active_during_test) == 0:
			# 	arr_disactiveItems.append("\t".join(row))
			# 	itemcount += 1
		count += 1

print "total items: ", itemcount, 'titles: ',len(titles),' tages:', len(tags)


# count1 = 0
# with open(DATAPATH+'/active_items.csv', 'w') as f:
#     f.write(str(header)+"\n")
#     for row in arr_activeItems:
#     	f.write(str(row)+"\n")
#     	count1 += 1
# print "active items : ", count1


# count2 = 0
# with open(DATAPATH+'/disactive_items.csv', 'w') as f:
#     f.write(str(header)+"\n")
#     for row in arr_disactiveItems:
#     	f.write(str(row)+"\n")
#     	count2 += 1
# print "disactive items : ", count2



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