import searchUtil
from evaluateCrime import LocationGrid
from sklearn.externals import joblib
import math


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
        return state == end

    def succAndCost(self, state):
        results = []

        for dr in range(-1, 2):
        	for dc in range(-1, 2):

        		if dr == 0 and dc == 0:
        			continue

        		newLocation = (state[0] + dr, state[1] + dc)
        		results.append((getStringAction(dr, dc), newLocation, math.sqrt(dr ** 2 + dc ** 2)))

        return results


# class SafestPath(searchUtil.SearchProblem):
#     def __init__(self, start, end, mileBlockSize, modelFile):

#         self.start = start

#     def startState(self):
#         return 0

#     def isEnd(self, state):
#         return state == len(self.query)

#     def succAndCost(self, state):
#         results = []
#         for i in range(state, len(self.query)):
#             newUnigram = self.query[state:i+1]
#             results.append((newUnigram, i + 1, self.unigramCost(newUnigram)))
#         return results


if __name__ == '__main__':

	# chicago dimensions
	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight)

	# latitude, longitude, modelFile
	start = (10, 10)
	end = (21, 15)
	modelFile = 'logisticModel.pkl'

	ucs = searchUtil.UniformCostSearch(verbose=3)
	ucs.solve(ShortestPath(start, end, locationGrid))

	actions = ucs.actions
	print ' '.join(actions)
