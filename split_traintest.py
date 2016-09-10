import csv
import time
import datetime

import linecache


start_time = time.time()

count = 0
arr = []

arr_train = []
arr_test = []

header = ""


# with open("data/interactions.csv", "r") as ins:
#     array = []
#     for line in ins:
#     	if count==0:
#     		header = line

#         array.append(line)

#         count += 1

#         if count == 100:
#         	break


# with open('data/interactions.csv','rb') as f:
with open('data/train/some.csv','rb') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if count==0:
			header = "\t".join(row)
			#write file
		elif count>1:
			# temp = datetime.datetime.fromtimestamp(float(row[3])).strftime('%Y-%m-%d')
			temp = datetime.datetime.fromtimestamp(float(row[3])).strftime('%m')
			# print temp
			if temp not in arr:
				arr.append(temp)

			if int(temp) == 11:
				arr_test.append("\t".join(row))
			else:
				arr_train.append("\t".join(row))

		# if count == 100:
		# 	break

		count += 1
		
print arr



# with open('data/test/some.csv', 'w') as f:
#     f.write(str(header)+"\n")
#     for row in arr_test:
#     	f.write(str(row)+"\n")


# with open('data/train/some.csv', 'w') as f:
#     f.write(str(header)+"\n")
#     for row in arr_train:
#     	f.write(str(row)+"\n")


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