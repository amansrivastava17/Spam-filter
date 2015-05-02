import svm
from svmutil import *
import re
import argparse

def file_read_set(filename):
	f=open(filename,'r')
	read_set=set(f.read().split('\n'))
	f.close()
	return read_set
def file_read(filename):
 	f=open(filename,'r')
 	read=f.read()
	f.close()
	return read

def remove_special_char(text):
	return re.sub(r'[~!@#$%^&*()_+=-\[\]\\|\}\{;\":,/<>?]+',' ',text)

WORDS_RE=re.compile("[a-z]{2,}")
def tokenize(content):
	stopwords= file_read_set('stopwords.txt')
	words=set()
	new_content=remove_special_char(content.lower())
	for match in WORDS_RE.finditer(new_content):
		word=match.group().strip(" ")
		if len(word)>=2:
			words.add(word)
	#return words
	return words-stopwords

def feature_dict(text):
	feature_dict={}
	text = list(tokenize(text))
	for index,value in enumerate(text):
		feature_dict[value]=index+1
	return feature_dict
def crete_features():
	spam_read=file_read('spam.txt')
	normal_read=file_read('normal.txt')
	features=feature_dict(spam_read+"\n"+normal_read)
	return features

def train_data():
	spam_set=file_read_set('spam.txt')
	normal_set=file_read_set('normal.txt')
	label_set=[]
	feature_set=[]
	features=crete_features()
	b={}
	for items in spam_set:
		b={}
		for item in tokenize(items):
			index=features.get(item,0)
			if index !=0:
				b[index]=1
		label_set.append(0)
		feature_set.append(b)
	for items in normal_set:
		b={}
		for item in tokenize(items):
			index=features.get(item,0)
			if index !=0:
				b[index]=1
		label_set.append(1)
		feature_set.append(b)
	prob = svm_problem(label_set,feature_set)
	param = svm_parameter()
	param.kernal_type=LINEAR
	param.C=10
	model=svm_train(prob,param)
	return model

def spam_detect(test):
	model=train_data()
	test_cases=[]
	test_set=tokenize(test)
	#print test_set
	b={}
	features=crete_features()
	#print features
	for item in test_set:
		#print "hello"
		index=features.get(item,0)
		#print "hello"
		if index !=0:
			b[index]=1
	test_cases.append(b)
	print test_cases
	label,a,b=svm_predict([0]*len(test_cases),test_cases,model)
	return label



def Main():
	parser=argparse.ArgumentParser()
	parser.add_argument("test_text",help="Enter test cases for spam detection ",type=str)
	args=parser.parse_args()
	result=spam_detect(args.test_text)
	if(result[0]==0.0):
		print ">>>>Spam detected<<<<"
	else:
		print ">>>>No Spam detected<<<<"

if __name__=='__main__':
	Main()
