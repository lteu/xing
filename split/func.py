import csv
import time
import os
import sys
import random
import operator
import datetime

import json


import numpy as np

from collections import Counter
from matplotlib import pyplot as plt
from sklearn.svm import SVR
from sklearn.svm import SVC



def featureToLine(tmpItem,value,set_ID):
	arr_all = []

	title = tmpItem['title']
	arr = mapPairArray(title,set_ID,'title')
	if arr is not None:
		arr_all = arr_all + arr

	discipline_id = tmpItem['discipline_id']
	element = mapPairOne(discipline_id,set_ID,'discipline_id')
	if element is not None:
		arr_all.append(element)

	country = tmpItem['country']
	element = mapPairOne(country,set_ID,'country')
	if element is not None:
		arr_all.append(element)

	region = tmpItem['region']
	element = mapPairOne(region,set_ID,'region')
	if element is not None:
		arr_all.append(element)

	tags = tmpItem['tags']
	arr = mapPairArray(tags,set_ID,'tags')
	if arr is not None:
		arr_all = arr_all + arr


	arr_all.sort(key=lambda x: x[0])

	output_dynam = arrayToStr(arr_all)
	# career_level = tmpItem['career_level']
	career_level = tmpItem['career_level'] if tmpItem['career_level'].strip() != ""  else '0'
	employment = tmpItem['employment'] if tmpItem['employment'].strip() != ""   else '0'
	rlt = str(value)+" qid:1 1:"+career_level+" 2:"+employment+output_dynam
	# print rlt
	return rlt,output_dynam


def arrayToStr(arr_all):
	output = ""
	for arr in arr_all:
		a = arr[0]
		b = arr[1]
		output = output+" "+str(a)+":"+str(b)
	return output
def mapPairOne(tmpstr,dicAll,arg):
	dic = dicAll[arg]
	if tmpstr in dic:
		tmpid = dic[tmpstr]
		return [tmpid,1]

	return None

def mapPairArray(tmpstr,dicAll,arg):
	arr = []
	dic = dicAll[arg]
	pieces = str(tmpstr).split(",")
	for tmpKey in pieces:
		if tmpKey in dic:
			tmpid = dic[tmpKey]
			arr.append([tmpid,1])
	if len(arr) != 0:
		return arr

	return None

def interactionVal(value):
	if value == 4:
		value = 0
	elif value == 3:
		value = 9
	elif value == 2:
		value = 8
	elif value == 1:
		value = 7
	return value

def loadItems(DATAPATH):
	itemset ={}
	itemset_active = []
	count= 0
	with open(DATAPATH+'/original/items.csv','rb') as f:

		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				tmpItem = {}
				tmpItemID = row[0]
				tmpItem['title'] = row[1]
				tmpItem['career_level'] = row[2]
				tmpItem['discipline_id'] = row[3]
				tmpItem['industry_id'] = row[4]
				tmpItem['country'] = row[5]
				tmpItem['region'] = row[6]
				tmpItem['latitude'] = row[7]
				tmpItem['longitude'] = row[8]
				tmpItem['employment'] = row[9]
				tmpItem['tags'] = row[10]
				
				itemset[str(row[0])] = tmpItem
				if int(row[12]) == 1:
					itemset_active.append(tmpItemID)
			count += 1
	return itemset,itemset_active

# instead of loading unnecessary 150.000.000 users
def loadTargetUsersWithProfile(DATAPATH):
	linecount =0
	users = {}
	with open(DATAPATH+'/target/target_users_profile.csv','r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:	
			if linecount > 0:
				user = {}
				userid = row[0]
				user['id'] = row[0]
				user['jobroles'] = row[1]
				user['career_level'] = row[2]
				user['discipline_id'] = row[3]
				user['industry_id'] = row[4]
				user['country'] = row[5]
				user['region'] = row[6]
				user['experience_n_entries_class'] = row[7]
				user['experience_years_experience'] = row[8]
				user['experience_years_in_current'] = row[9]
				user['edu_degree'] = row[10]
				user['edu_fieldofstudies'] = row[11]
				users[userid] = user
			linecount += 1
	return users

def loadTargetUserIDs(filename,DATAPATH):
	linecount = 0
	target_users_id = []
	with open(DATAPATH+'/'+filename,'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if linecount > 0:
				target_users_id.append(row[0])
			linecount += 1

	return target_users_id

def loadImpressionsDictByFilename(filename,DATAPATH):
	impressions = {}
	count= 0
	with open(DATAPATH+'/impressions/'+filename,'rb') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if count>1:
				tmpID = row[0]
				if tmpID not in impressions:
					impressions[tmpID] = row[3].split(",")
				else:
					impressions[tmpID] += row[3].split(",")
			count += 1
	return impressions

def loadInteractionsByWeeks(weeks,DATAPATH):
	dic = {}
	for week in weeks:
		count = 0
		with open(DATAPATH+'/interactions/week'+str(week)+'b.csv','rb') as f:
			reader = csv.reader(f, delimiter='\t')
			for row in reader:
				if count>1:
					userid = row[0]
					itemid = row[1]
					intype = row[2]
					if userid not in dic:
						dic[userid] = {}
					dic[userid][itemid]=intype
				count += 1
	return dic

def normalizeItemFeatures(item,titles_base,tags_base,indu_base):
	career_level = 0
	if item['career_level'] != 'null' and item['career_level'] != 'NULL' and item['career_level'] != '':
		career_level = int(str(item['career_level']))
	
	feat_arr = []
	feat_arr.append(calSimScoreForLists(titles_base,item['title'].split(",")))
	feat_arr.append(calSimScoreForLists(tags_base,item['tags'].split(",")))
	feat_arr.append(career_level)
	feat_arr.append(int(item['discipline_id']))

	# item_ind_id = item['industry_id']
	# item_ind_id_arr = [item_ind_id]
	# feat_arr.append(calSimScoreForListsSoft(indu_base,item_ind_id_arr))
	feat_arr.append(int(item['industry_id']))
	
	feat_arr.append(convertCountryToCode(item['country']))
	feat_arr.append(int(item['region']))
	feat_arr.append(int(item['employment']))
	return feat_arr



def calOccurenceRank(disorderList):
	counted_dic =  Counter(disorderList)
	tupleWithOccurences = counted_dic.items() 
	tuple_sorted = sorted(tupleWithOccurences,key=lambda x: x[1], reverse=True)
	ranked_array = []
	for x in tuple_sorted:
		ranked_array.append(x[0])
	return ranked_array

def calSimScoreForLists(passtset,newset):
	if len(set(passtset[:1]).intersection(set(newset))):
		return 9
	elif len(set(passtset[:4]).intersection(set(newset))):
		return 4
	elif len(set(passtset).intersection(set(newset))):
		return 1
	else:
		return 0

def calSimScoreForListsSoft(passtset,newset):
	if len(set(passtset[:1]).intersection(set(newset))):
		return 5
	elif len(set(passtset[:4]).intersection(set(newset))):
		return 4
	elif len(set(passtset).intersection(set(newset))):
		return 3
	else:
		return 0


def convertCountryToCode(country):
	if country == 'de':
		return 3
	elif country == 'at':
		return 2
	elif country == 'ch':
		return 1
	else:
		return 0


