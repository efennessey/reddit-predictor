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
		totSub = float(summarySub[s][0] + summarySub[s][1] +summarySub[s][2])
		probSub = [summarySub[s][0]/totSub, summarySub[s][1]/totSub, summarySub[s][2]/totSub]

	#Find author and probabilities
	a = findData(data, 3, summaryAuthor)
	if a == -1:
		probAuth = [1, 0, 0]
	else:
		totAuth = float(summaryAuthor[a][0] + summaryAuthor[a][1] +summaryAuthor[a][2])
		probAuth = [summaryAuthor[a][0]/totAuth, summaryAuthor[a][2]/totAuth, summaryAuthor[a][2]/totAuth]

	#Find title length and probabilities
	l = findData(data, 2, summaryTitle)
	if l == -1:
		probLen = [1, 0, 0]
	else:
		totLen = float(summaryTitle[l][0] + summaryTitle[l][1] + summaryTitle[l][2])
		probLen = [summaryTitle[l][0]/totLen, summaryTitle[l][1]/totLen, summaryTitle[l][2]/totLen]


	unsuccessful = float(probSub[0] + probAuth[0] + probLen[0])/3
	moderate = float(probSub[1] + probAuth[1] + probLen[1])/3
	successful = float(probSub[2] + probAuth[2] + probLen[2])/3

	if unsuccessful < 0.7:
		print 'Override: predicted 2'
		return 2
	elif unsuccessful < 0.75:
		print'Override: predicted 1'
		return 1
	elif max([unsuccessful, moderate, successful]) == unsuccessful:
		print '0 Probability: ' + str(unsuccessful)
		print '1 Probability: ' + str(moderate)
		print '2 Probability: ' + str(successful)
		return 0
	elif max([unsuccessful, moderate, successful]) == moderate:
		print 'Moderate Probability: ' + str(moderate)
		return 1
	else:
		print 'Successful Probability: ' + str(successful)
		return 2

def main():
	filename = 'lotsadata.csv'
	splitRatio = 0.9
	dataset = loadCsv(filename)
	trainSet, testSet = splitDataset(dataset, splitRatio)
	
	summarySub = []
	summaryAuthor = []
	summaryTitle = []

	summarizeAll(trainSet, summarySub, summaryAuthor, summaryTitle)

	predictions = [0, 0, 0]
	correct = [0, 0, 0, 0]
	totals = [0, 0, 0]

	for x in testSet:
		p = predict(x, summarySub, summaryAuthor, summaryTitle)
		predictions[p] += 1
		totals[x[0]] += 1
		if p == x[0]:
			correct[p] += 1
			correct[3] += 1
		print 'Prediction: ' + str(p) + ', Actual: ' + str(x[0])
		print ''

	print ''
	print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainSet), len(testSet))
	print 'Unsuccessful Predicted: ' + str(predictions[0]) + ', Actual: ' + str(totals[0]) + ', Correct: ' + str(correct[0])
	print 'Moderately Successful Predicted: ' + str(predictions[1]) + ', Actual: ' + str(totals[1]) + ', Correct: ' + str(correct[1])
	print 'Successful Predicted: ' + str(predictions[2]) + ', Actual: ' + str(totals[2]) + ', Correct: ' + str(correct[2])
	print ''
	print 'Unsuccessful accuracy: ' + str(float(correct[0])/totals[0])
	print 'Moderately Successful accuracy: ' + str(float(correct[1])/totals[1])
	print 'Successful accuracy: ' + str(float(correct[2])/totals[2])
	print 'Total accuracy: ' + str(float(correct[3])/len(testSet))

main()









