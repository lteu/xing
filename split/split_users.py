import csv
import time
import datetime
import os

start_time = time.time()


in_path = os.path.realpath(__file__).split('/')[:-2]
DATAPATH = '/'.join(in_path) + '/data'


# load target users

linecount = 0
target_users_id = []
with open(DATAPATH+'/test/target_users.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if linecount > 0:
			target_users_id.append(row[0])
		linecount += 1

print 'target users loaded ... '

# users

linecount = 0
usersline = []
header = ""
usercount = 0
with open(DATAPATH+'/users.csv','r') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		if linecount == 0:
			header = "\t".join(row)
		else:
			userid = row[0]
			if userid in target_users_id:
				usersline.append("\t".join(row))
				usercount += 1
		linecount += 1
		if linecount % 1000 == 0:
			print 'running users canning... ',linecount

print "file users.csv read, target users found ", usercount ,' ....'

# writing

count2 = 0
with open('data/target_users_profile.csv', 'w') as f:
    f.write(str(header)+"\n")
    for row in usersline:
    	f.write(str(row)+"\n")
    	count2 += 1
    	if count2 % 1000 == 0:
			print 'running users writing... '
print "writing count : ", count2 , ' ....'



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