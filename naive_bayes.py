1import csv
import random
import math

def loadCsv(filename):
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		dataset = list(reader)
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
		if x[4] == data[4]:
			x[data[0]] += 1
			found = 1
		if found:
			break
	if !found:
		row = [0, 0, 0, data[4]]
		row[data[0]] += 1
		summary.append(row)

def summarizeAuthor(data, summary):
	found = 0
	for x in summary:
		if x[3] == data[3]:
			x[data[0]] += 1
			found = 1
		if found:
			break
	if !found:
		row = [0, 0, 0, data[3]]
		row[data[0]] += 1
		summary.append(row)


def summarizeTitleLength(data, summary):
	length = len(data[2])
	if length not in summary:
		summary[length] = [0, 0, 0, length]
		summary[length[data[0]]] += 1
	else:
		summary[length[data[0]]] += 1


def summarizeAll(dataset):
	summarySub = {}
	summaryAuthor = {}
	summaryTitle = {}
	for x in dataset:
		summarizeSubreddit(x, summarySub)
		summarizeAuthor(x, summaryAuthor)
		summarizeTitleLength(x, summaryTitle)






