import csv
import math

class LocationGrid(object):

	MILES_PER_DEGREE = 69.0

	def __init__(self, mileBlockSize, topLeft, bottomRight):
		# assert that coordinates make sense
		assert(topLeft[0] > bottomRight[0] and topLeft[1] < bottomRight[1])

		# store this for future usage
		self.topLeft = topLeft

		self.degreeBlockSize = mileBlockSize / self.MILES_PER_DEGREE

		gridHeight = self.latToRow(bottomRight[0]) + 1
		gridWidth = self.longToCol(bottomRight[1]) + 1
		self.locationGrid = [[[] for j in range(gridWidth)] for i in range(gridHeight)]	


	def latToRow(self, latitude):
		return int(math.floor( abs(latitude - self.topLeft[0]) / self.degreeBlockSize ))

	def longToCol(self, longitude):
		return int(math.floor( abs(longitude - self.topLeft[1]) / self.degreeBlockSize ))

	def addEntry(self, row, latitude, longitude):
		r = self.latToRow(float(latitude))
		c = self.longToCol(float(longitude))

		# check bounds
		if r < 0 or r >= len(self.locationGrid) or c < 0 or c >= len(self.locationGrid[0]):
			return False

		self.locationGrid[r][c].append(row)
		return True


def evaluateCrimes(locationGrid):
	count = 0
	with open('Chicago_Crimes_2012_to_2017.csv', 'rb') as csvfile:
		dataReader = csv.reader(csvfile)

		# read first line, which has titles
		dataReader.next()

		for row in dataReader:
			latitude, longitude = row[20], row[21]

			# skip rows missing lat / long data
			if latitude == '' or longitude == '':
				continue

			if locationGrid.addEntry(row, latitude, longitude):
				count += 1
			
	print count

if __name__ == '__main__':

	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight)
	evaluateCrimes(locationGrid)


## naive bayes
# P(crime | location, ..., other factors) = P(location, ..., other factors | crime) P (crime) / P (location, ..., other factors)






