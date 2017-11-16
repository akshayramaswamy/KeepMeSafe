import csv
import re
from datetime import datetime
from evaluateCrime2 import LocationGrid


def createRow(dataWriter, r, c, month, weekday, hour, crime):
	newRow = [r, c] + [0 if i != month else 1 for i in range(12)] + \
		[0 if i != weekday else 1 for i in range(7)] + [0 if i != hour else 1 for i in range(24)] + [crime]
	
	dataWriter.writerow(newRow)


if __name__ == '__main__':

	# use locationGrid for latitude to row and longitude to col conversion
	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	# store three sets of seen months, day, hour
	locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight, \
		[set(), set(), set()])

	count = 0


	with open('ChicagoEditedDataset.csv', 'wb') as newfile:
		dataWriter = csv.writer(newfile)

		# [(row, col), day [0 - 6], month [0 - 11], hour [0 - 23], block, crime]
		dataWriter.writerow(['Row', 'Col'] + ['Month {}'.format(i) for i in range(12)] + \
			['Day of Week {}'.format(i) for i in range(7)] + ['Hour {}'.format(i) for i in range(24)] + ['Crime'])

		# reformat rows of old crime dataset 
		with open('Chicago_Crimes_2012_to_2017.csv', 'rb') as oldfile:
			dataReader = csv.reader(oldfile)

			# read first line, which has titles
			dataReader.next()

			# loop over and reformat data rows
			for row in dataReader:

				# exclude domestic crimes
				if row[10] == 'True':
					continue

				latitude, longitude = row[20], row[21]

				# skip rows missing lat / long data
				if latitude == '' or longitude == '':
					continue

				r = locationGrid.latToRow(float(latitude))
				c = locationGrid.longToCol(float(longitude))

				# ignore out of buonds
				if not locationGrid.inBounds(r, c):
					continue

				# parse data from the row
				date = datetime.strptime(row[3], '%m/%d/%Y %I:%M:%S %p')
				
				# Sunday is 0, Saturday is 6
				weekday = (date.weekday() + 1) % 7
				month = date.month - 1
				hour = date.hour

				# add the current month, day, hour
				locationGrid.locationGrid[r][c][0].add(month)
				locationGrid.locationGrid[r][c][1].add(weekday)
				locationGrid.locationGrid[r][c][2].add(hour)

				createRow(dataWriter, r, c, month, weekday, hour, 1)
				count += 1

		# generate safe rows
		for r in range(locationGrid.numRows()):
			for c in range(locationGrid.numCols()):
				seenMonths, seenDays, seenHours = locationGrid.locationGrid[r][c]

				for month in range(12):
					if month in seenMonths:
						continue

					for weekday in range(7):
						if weekday in seenDays:
							continue

						for hour in range(24):
							if hour in seenHours:
								continue

							# generate a safe data row
							createRow(dataWriter, r, c, month, weekday, hour, 0)
							count += 1

		print '{} rows generated.'.format(count)

	 