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

		self.degreeBlockSize = mileBlockSize / self.MILES_PER_DEGREE

		gridHeight = self.latToRow(bottomRight[0]) + 1
		gridWidth = self.longToCol(bottomRight[1]) + 1
		self.locationGrid = [[copy.deepcopy(entry) for j in range(gridWidth)] for i in range(gridHeight)]	


	def latToRow(self, latitude):
		return int(math.floor( abs(latitude - self.topLeft[0]) / self.degreeBlockSize ))

	def longToCol(self, longitude):
		return int(math.floor( abs(longitude - self.topLeft[1]) / self.degreeBlockSize ))

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


# class MDPFeatureExtractor(object):

# 	def __init__(self, features):
# 		self.vectorizer = DictVectorizer()

# 		# dummy dict
# 		featuresDict = {feat : 0 for feat in features}
# 		self.vectorizer.fit_transform(featuresDict)


# 	def extract(featuresDict):


# 		return []

def learnLogisticModel():

	# input and output
	dictInputData = []
	outputMatrix = []

	csvData = pandas.read_csv("ChicagoEditedDatasetDec.csv", delimiter=",")

	for i, row in csvData.iterrows():
		pass
		# # row, col, weekday, hour, crime
		# rowDict = {}
		# crimeValue = None
		# for col in row:
		# 	name = row[col].name
		# 	value = row[col].values[0]

		# 	if name == 'Crime':
		# 		crimeValue = value
		# 	else:
		# 		rowDict['{}-{}'.format(name, value)] = 1

		# dictInputData.append(rowDict)
		# outputMatrix.append([crimeValue])

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

	logreg = joblib.load('logisticModel.pkl')

	sample = numpy.reshape([400, 145, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], (1, -1))

	print logreg.predict(sample)
	print logreg.predict_proba(sample)
	print logreg.coef_



if __name__ == '__main__':

	learnLogisticModel()

	# loadLogisticModel()



