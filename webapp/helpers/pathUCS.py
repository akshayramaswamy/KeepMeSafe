import searchUtil
from evaluateCrime import LocationGrid, SafePathFeatureExtractor
from sklearn.externals import joblib
import math
import numpy
# import matplotlib.pyplot as plt
import requests

def getStringAction(dr, dc):
	resultString = ''

	if dr == -1:
		resultString += 'U'
	elif dr == 1:
		resultString += 'D'

	if dc == -1:
		resultString += 'L'
	elif dc == 1:
		resultString += 'R'

	return resultString

def getDelta(directionString):
	change = [0, 0]
	
	if 'L' in directionString:
		change[1] = -1
	elif 'R' in directionString:
		change[1] = 1

	if 'U' in directionString:
		change[0] = -1
	elif 'D' in directionString:
		change[0] = 1

	return change


def displayResults(actions, start, locationGrid, title=None):

	print 'START: {}'.format(start)
	
	# need to reset values
	maxProb = 0
	for r in range(locationGrid.numRows()):
		for c in range(locationGrid.numCols()):
			maxProb = max(locationGrid.locationGrid[r][c], maxProb)

	# initialize danger sum
	dangerSum = locationGrid.locationGrid[start[0]][start[1]]

	# mark start
	locationGrid.locationGrid[start[0]][start[1]] = maxProb

	if actions is None:
		print 'No path found'
		return


	for action in actions:
		dr, dc = getDelta(action)
		start = (start[0] + dr, start[1] + dc)

		dangerSum += locationGrid.locationGrid[start[0]][start[1]]
		
		# mark start
		locationGrid.locationGrid[start[0]][start[1]] = maxProb
		
		print '%2s --> %s' % (action, start)

	print 'Sum Danger: {}, Num Actions: {}, Mean Danger: {}, Estimated Time: {}, Actual Time: {}'.format(dangerSum, len(actions), \
		dangerSum / len(actions), len(actions) * locationGrid.getBlockSize() * 15.0, \
		len([a for a in actions if sum([abs(num) for num in getDelta(a)]) == 1]) * locationGrid.getBlockSize() * 15.0 + \
		len([a for a in actions if sum([abs(num) for num in getDelta(a)]) == 2]) * math.sqrt(2 * locationGrid.getBlockSize() ** 2) * 15.0)

	createHeatMap(locationGrid.locationGrid, title, False)


def snapPoints(actions, start, locationGrid, roadsKey):
	if actions is None:
		return None

	latLong = locationGrid.rowColToLatLong(start)
	latLongPairs = ["{},{}".format(latLong[0], latLong[1])]

	# iterate over every 100 points
	for action in actions:
		dr, dc = getDelta(action)
		start = (start[0] + dr, start[1] + dc)
		latLong = locationGrid.rowColToLatLong(start)
		latLongPairs.append("{},{}".format(latLong[0], latLong[1]))
		
	results = []
	for i in range(0, len(latLongPairs), 100):
		# loop over every 100
		r = requests.get("https://roads.googleapis.com/v1/snapToRoads", params={'key': roadsKey, \
			'path': '|'.join(latLongPairs[i: i + 100]), 'interpolate': True})
		
		if r.status_code != 200:
			return None

		results += [(point['location']['latitude'], point['location']['longitude']) for point in r.json()['snappedPoints']]

	return results



def createHeatMap(data, title=None, showLegend=True):
	# Generate some test data
	newData = numpy.array(data)

	plt.imshow(newData, cmap='hot', interpolation='nearest')

	if title is not None:
		plt.title(title)
	if showLegend:
		plt.colorbar()

	plt.show()


def addressToLatLong(address, geoencodingKey):
	r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={'address': address, 'key': geoencodingKey})
	if r.status_code == 200:
		results = r.json()['results']
		if len(results) != 0:
			info = results[0]['geometry']['location']
			return (info['lat'], info['lng'])

	return None


class ShortestPath(searchUtil.SearchProblem):
	# very simple distance UCS, just
	# takes the shortest path to the end 
	# goal
	
    def __init__(self, start, end, locationGrid):
        self.start = start
        self.end = end
        self.locationGrid = locationGrid

    def startState(self):
        return self.start

    def isEnd(self, state):
        return state == self.end

    def succAndCost(self, state):
        results = []

        for dr in range(-1, 2):
        	for dc in range(-1, 2):
        		if (dr == 0 and dc == 0):
        			continue

        		newR = state[0] + dr
        		newC = state[1] + dc

        		if not self.locationGrid.inBounds(newR, newC):
        			continue

        		results.append((getStringAction(dr, dc), (newR, newC), math.sqrt(dr ** 2 + dc ** 2)))

        return results


class SafestPath(searchUtil.SearchProblem):
    def __init__(self, start, end, locationGrid):
        self.start = start
        self.end = end
        self.locationGrid = locationGrid 

    def startState(self):
        return self.start

    def isEnd(self, state):
        return state == self.end

    def succAndCost(self, state):
        results = []

        for dr in range(-1, 2):
        	for dc in range(-1, 2):
        		if (dr == 0 and dc == 0):
        			continue

        		newR = state[0] + dr
        		newC = state[1] + dc

        		if not self.locationGrid.inBounds(newR, newC):
        			continue

        		results.append((getStringAction(dr, dc), (newR, newC), \
        			self.locationGrid.locationGrid[newR][newC]))

        return results 


class OptimalPath(searchUtil.SearchProblem):
    def __init__(self, start, end, locationGrid, maxTime):
        self.start = start
        self.end = end
        self.locationGrid = locationGrid 

        # 15 minutes / mile
        self.maxActions = int(math.floor(maxTime / 15.0 / self.locationGrid.getBlockSize()))


    def startState(self):
        return (self.start, 0)

    def isEnd(self, state):
        return state[0] == self.end

    def succAndCost(self, state):

    	location, numActions = state

    	if numActions == self.maxActions:
    		return []

        results = []

        for dr in range(-1, 2):
        	for dc in range(-1, 2):
        		if (dr == 0 and dc == 0):
        			continue

        		newR = location[0] + dr
        		newC = location[1] + dc

        		if not self.locationGrid.inBounds(newR, newC):
        			continue

        		results.append((getStringAction(dr, dc), ((newR, newC), numActions + 1), \
        			self.locationGrid.locationGrid[newR][newC]))

        return results 


if __name__ == '__main__':

	# chicago dimensions
	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight)
	logreg = joblib.load('logisticModel.pkl')

	featureExtractor = SafePathFeatureExtractor(['Row', 'Col', 'Day', 'Hr'], \
		[locationGrid.numRows(), locationGrid.numCols(), 7, 24])

	for i in range(locationGrid.numRows()):
		for j in range(locationGrid.numCols()):
			# walking on Tuesday at 11 PM
			sample = featureExtractor.extract([i, j, 2, 23])
			predicted_prob = logreg.predict_proba(sample)
			locationGrid.locationGrid[i][j] = predicted_prob[0][1]

	start = "1824 W Pershing Rd, Chicago, IL 60609"
	end = "8000 Michigan Avenue, Chicago, IL 60609"

	startLatLong = addressToLatLong(start)
	endLatLong = addressToLatLong(end)

	if start is None or end is None:
		quit()

	start = locationGrid.latLongToRowCol(startLatLong)
	end = locationGrid.latLongToRowCol(endLatLong)
	modelFile = 'logisticModel.pkl'

	ucs = searchUtil.UniformCostSearch(verbose=0)

	# currently can only run one of these at a time,
	# need to figure out matplot lib
	# displayResults also changes locationGrid, so need
	# to create separate instance of class in each call or copy grid beforehand

	# # shortest path
	# ucs.solve(ShortestPath(start, end, locationGrid))
	# actions = ucs.actions
	# displayResults(actions, start, locationGrid, "Shortest Path")

	# # safest path
	ucs.solve(SafestPath(start, end, locationGrid))
	actions = ucs.actions
	# displayResults(actions, start, locationGrid, "Safest Path")

	# # best path
	# time = 120
	# ucs.solve(OptimalPath(start, end, locationGrid, time))
	# actions = ucs.actions
	print snapPoints(actions, start, locationGrid)
# 	displayResults(actions, start, locationGrid, "Optimal Path, T = {}".format(time))

