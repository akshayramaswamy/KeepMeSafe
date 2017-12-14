import csv
import math
import copy
from sklearn import linear_model
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
import numpy
import pandas
import random

class LocationGrid(object):

	MILES_PER_DEGREE = 69.0

	def __init__(self, mileBlockSize, topLeft, bottomRight, entry=0):
		# assert that coordinates make sense
		assert(topLeft[0] > bottomRight[0] and topLeft[1] < bottomRight[1])

		# store this for future usage
		self.topLeft = topLeft

		self.mileBlockSize = mileBlockSize
		self.degreeBlockSize = mileBlockSize / self.MILES_PER_DEGREE

		gridHeight = self.latToRow(bottomRight[0]) + 1
		gridWidth = self.longToCol(bottomRight[1]) + 1
		self.locationGrid = [[copy.deepcopy(entry) for j in range(gridWidth)] for i in range(gridHeight)]	


	def latToRow(self, latitude):
		return int( (self.topLeft[0] - latitude) / self.degreeBlockSize )

	def longToCol(self, longitude):
		return int( (longitude - self.topLeft[1]) / self.degreeBlockSize )

	def latLongToRowCol(self, latLongPair):
		latitude, longitude = latLongPair
		return (self.latToRow(latitude), self.longToCol(longitude))

	def rowToLat(self, row):
		return self.topLeft[0] - row * self.mileBlockSize / self.MILES_PER_DEGREE

	def colToLong(self, col):
		return self.topLeft[1] + col * self.mileBlockSize / self.MILES_PER_DEGREE

	def rowColToLatLong(self, rowColPair):
		row, col = rowColPair
		return (self.rowToLat(row), self.colToLong(col))

	def inBounds(self, r, c):
		return r >= 0 and r < self.numRows() and c >= 0 and c < self.numCols()

	def numRows(self):
		return len(self.locationGrid)

	def numCols(self):
		if len(self.locationGrid) == 0:
			return 0
		else:
			return len(self.locationGrid[0])

	def addEntry(self, dataRow, latitude, longitude):
		r = self.latToRow(float(latitude))
		c = self.longToCol(float(longitude))

		# check bounds
		if not self.inBounds(r, c):
			return False

		self.locationGrid[r][c].append(dataRow)
		return True

	def getBlockSize(self):
		return self.mileBlockSize



class SafePathFeatureExtractor(object):

	def __init__(self, features, counts):
		self.vectorizer = DictVectorizer()
		self.features = features

		dummyData = {}
		for i, feature in enumerate(features):
			dummyData.update({'{}-{}'.format(feature, j) : 0 for j in range(counts[i])})

		self.vectorizer.fit_transform(dummyData)

	def extract(self, values):
		infoDict = {'{}-{}'.format(self.features[i], values[i]) : 1 for i in range(len(self.features))}
		return self.vectorizer.transform(infoDict)		



def learnLogisticModel():

	# input and output
	dictInputData = []
	outputMatrix = []

	csvData = pandas.read_csv("ChicagoEditedDatasetDec.csv", delimiter=",")
	print 'finished reading'

	colNames = [name for name in csvData.dtypes.index]

	for i, row in csvData.iterrows():
		# row, col, weekday, hour, crime
		rowDict = {'{}-{}'.format(colNames[i], row[i]) : 1 for i in range(len(colNames) - 1)}
		dictInputData.append(rowDict)
		outputMatrix.append([row[-1]]) 

	print 'finished appending'

	vectorizer = DictVectorizer()
	inputData = vectorizer.fit_transform(dictInputData)
	outputData = numpy.array(outputMatrix).ravel()

	print vectorizer.get_feature_names()

	# fit model
	logreg = linear_model.LogisticRegression()
	logreg.fit(inputData, outputData)
	
	joblib.dump(logreg, 'logisticModel.pkl')


def loadLogisticModel():	
	# chicago dimensions
	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)
	locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight)

	featureExtractor = SafePathFeatureExtractor(['Row', 'Col', 'Day', 'Hr'], \
		[locationGrid.numRows(), locationGrid.numCols(), 7, 24])
	sample = featureExtractor.extract([100, 145, 2, 23])

	logreg = joblib.load('logisticModel.pkl')

	print logreg.predict(sample)
	print logreg.predict_proba(sample)
	print logreg.coef_



if __name__ == '__main__':

	# learnLogisticModel()

	loadLogisticModel()



