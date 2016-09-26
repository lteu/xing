#
#
# COMMENT zip approach for a fast file access has been proven not efficient
#
#


# import csv, io, sys, zipfile

# zip_file    = zipfile.ZipFile(sys.argv[1])
# items_file  = zip_file.open('data/items.csv', 'rU')
# # items_file.readable = lambda: True
# # items_file.writable = lambda: False
# # items_file.seekable = lambda: False
# # items_file.read1 = items_file.read
# items_file  = io.TextIOWrapper(items_file)

# for idx, row in enumerate(csv.DictReader(items_file)):
#     print('Processing row {0} -- row = {1}'.format(idx, row))


import glob
import os
import csv
import zipfile
import StringIO
import time

# for name in glob.glob('data/*.zip'):
#     base = os.path.basename(name)
#     filename = os.path.splitext(base)[0]


    # datadirectory = 'C:/Projects/abase/'
    # dataFile = filename
    # archive = '.'.join([dataFile, 'zip'])
    # fullpath = ''.join([datadirectory, archive])
    # csv_file = '.'.join([dataFile, 'csv']) #all fixed

start_time = time.time()

fullpath = "data/interactions.csv.zip"

filehandle = open(fullpath, 'rb')
zfile = zipfile.ZipFile(filehandle)
data = StringIO.StringIO(zfile.read('interactions.csv')) #don't forget this line!
reader = csv.reader(data)

count = 0
for row in reader:
	count += 1
    # print row

print count,' records'

print("--- %s seconds ---" % (time.time() - start_time))