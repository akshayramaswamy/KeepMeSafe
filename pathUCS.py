import searchUtil
from evaluateCrime import LocationGrid, SafePathFeatureExtractor
from sklearn.externals import joblib
import math
import numpy
import matplotlib.pyplot as plt


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


def displayResults(actions, start):

	print start
	
	for action in actions:
		print '\n{}'.format(action)

		dr, dc = getDelta(action)
		start = (start[0] + dr, start[1] + dc)
		print start


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

	# # Generate some test data
	# data = numpy.array(locationGrid.locationGrid)

	# plt.title('Crime Probabilities')
	# plt.imshow(data, cmap='hot', interpolation='nearest')
	# plt.colorbar()
	# plt.show()

	# latitude, longitude, modelFile
	start = (10, 10)
	end = (7, 40)
	modelFile = 'logisticModel.pkl'

	ucs = searchUtil.UniformCostSearch(verbose=0)

	# shortest path
	ucs.solve(ShortestPath(start, end, locationGrid))
	actions = ucs.actions
	displayResults(actions, start)

	# safest path
	ucs.solve(SafestPath(start, end, locationGrid))
	actions = ucs.actions
	print ' '.join(actions)

