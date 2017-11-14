import csv
import math

MILES_PER_DEGREE = 69.0

def evaluateCrimes(topLeft, bottomRight, degreeBlockSize):

	def latToRow(latitude):
		return int(math.floor( abs(latitude - topLeft[0]) / degreeBlockSize ))

	def longToCol(longitude):
		return int(math.floor( abs(longitude - topLeft[1]) / degreeBlockSize ))

	# create grid that stores data rows at each (i, j) index
	# lat x long
	gridHeight = latToRow(bottomRight[0]) + 1
	gridWidth = longToCol(bottomRight[1]) + 1
	locationGrid = [[[] for j in range(gridWidth)] for i in range(gridHeight)]	

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

			r = latToRow(float(latitude))
			c = longToCol(float(longitude))

			# check bounds
			if r < 0 or r >= len(locationGrid) or c < 0 or c >= len(locationGrid[0]):
				continue

			count += 1
			locationGrid[r][c].append(row)
			
	print count


def getDegreeBlockSize(mileBlockSize):
	return mileBlockSize / MILES_PER_DEGREE


if __name__ == '__main__':

	degreeBlockSize = getDegreeBlockSize(0.1)

	# coordinates
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	evaluateCrimes(topLeft, bottomRight, degreeBlockSize)


## naive bayes
# P(crime | location, ..., other factors) = P(location, ..., other factors | crime) P (crime) / P (location, ..., other factors)






