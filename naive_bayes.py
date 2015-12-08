import csv
import random
import math

def loadCsv(filename):
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		dataset = list(reader)
		for x in range(len(dataset)):
			dataset[x][0] = int(dataset[x][0])
		return dataset
	"""
	May have to convert dataset[i][0] (score) to int here?
	Possibly word count if we choose to use this 
	"""


def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]


def separatedByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[0] not in separated):
			separated[vector[0]] = []
		separated[vector[0]].append(vector)
	return separated

# Helper summary methods for each attribute
def summarizeSubreddit(data, summary):
	found = 0
	for x in summary:
		if x[3] == data[4]:
			x[data[0]] += 1
			found = 1
		if found:
			break
	if found == 0:
		row = [0, 0, 0, data[4]]
		row[data[0]] += 1
		summary.append(row)

def summarizeAuthor(data, summary):
	found = 0
	for x in summary:
		if x[3] == data[3]:
			x[data[0]] += 1
			found = 1
		if found == 1:
			break
	if found == 0:
		row = [0, 0, 0, data[3]]
		row[data[0]] += 1
		summary.append(row)


def summarizeTitleLength(data, summary):
	length = len(data[2])
	found = 0
	for x in summary:
		if x[3] == length:
			x[data[0]] += 1
			found = 1
		if found == 1:
			break
	if found == 0:
		row = [0, 0, 0, length]
		row[data[0]] += 1
		summary.append(row)


def summarizeAll(dataset, summarySub, summaryAuthor, summaryTitle):
	for x in dataset:
		summarizeSubreddit(x, summarySub)
		summarizeAuthor(x, summaryAuthor)
		summarizeTitleLength(x, summaryTitle)

def findData(data, col, summary):
	found = 0
	location = 0
	for x in summary:
		if (data[col] == x[3]):
			found = 1
			break
		else:
			location += 1
	if found == 0:
		return -1
	else:
		return location


def predict(data, summarySub, summaryAuthor, summaryTitle):
	#Find subreddit and probabilities
	s = findData(data, 4, summarySub)
	if s == -1:
		probSub = [1, 0, 0]
	else:
		totSub = summarySub[s][0] + summarySub[s][1] +summarySub[s][2]
		probSub = [summarySub[s][0]/totSub, summarySub[s][1]/totSub, summarySub[s][2]/totSub]

	#Find author
	a = findData(data, 3, summaryAuthor)
	if a == -1:
		probAuth = [1, 0, 0]
	else:
		totAuth = summaryAuthor[a][0] + summaryAuthor[a][1] +summaryAuthor[a][2]
		probAuth = [summaryAuthor[a][0]/totAuth, summaryAuthor[a][2]/totAuth, summaryAuthor[a][2]/totAuth]

	#(Title length is just at that location in the array)
	l = findData(data, 2, summaryTitle)
	if l == -1:
		probLen = [1, 0, 0]
	else:
		totLen = summaryTitle[l][0] + summaryTitle[l][1] + summaryTitle[l][2]
		probLen = [summarySub[l][0]/totLen, summarySub[l][1]/totLen, summarySub[l][2]/totLen]


	unsuccessful = (probSub[0] + probAuth[0] + probLen[0])/3
	moderate = (probSub[1] + probAuth[1] + probLen[1])/3
	successful = (probSub[2] + probAuth[2] + probLen[2])/3

	if max([unsuccessful, moderate, successful]) == unsuccessful:
		return 0
	elif max([unsuccessful, moderate, successful]) == moderate:
		return 1
	else:
		return 2

def main():
	filename = 'lotsadata.csv'
	splitRatio = 0.9
	dataset = loadCsv(filename)
	trainSet, testSet = splitDataset(dataset, splitRatio)
	print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainSet), len(testSet))
	
	summarySub = []
	summaryAuthor = []
	summaryTitle = []

	summarizeAll(trainSet, summarySub, summaryAuthor, summaryTitle)

	for x in testSet:
		p = predict(x, summarySub, summaryAuthor, summaryTitle)
		print 'Prediction: ' + str(p) + ', Actual: ' + str(x[0])

main()









