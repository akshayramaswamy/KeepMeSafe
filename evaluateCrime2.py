import csv
import math
import copy
from sklearn import linear_model
import numpy
import pandas

class LocationGrid(object):

	MILES_PER_DEGREE = 69.0

	def __init__(self, mileBlockSize, topLeft, bottomRight, entry=[]):
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
		return r >= 0 and r < len(self.locationGrid) and c >= 0 and c < len(self.locationGrid[0])

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


def evaluateCrimes():

	data = pandas.read_csv("ChicagoEditedDataset.csv", delimiter=',', skiprows=1)
	print 'Finished loading'

	inputMatrix = data[:10,:-1]
	outputMatrix = data[:10,-1:]
		
	logreg = linear_model.LogisticRegression()

	logreg.fit(inputMatrix, outputMatrix)

	print logreg.predict([99, 145, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
	print logreg.predict_proba([99, 145, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])





if __name__ == '__main__':

	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	# locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight)
	evaluateCrimes()



