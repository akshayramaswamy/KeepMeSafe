import searchUtil
from sklearn.externals import joblib
import numpy

ROWS = 275
COLUMNS = 317
class SearchProblem(searchUtil.SearchProblem):
    def __init__(self, initialState, endState, probabilityGrid):
        self.initialState = initialState
        self.endState = endState
        self.probabilityGrid = probabilityGrid 

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.initialState
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        return state == self.endState
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        x, y = state
        results = []
        if x-1 >= 0: results.append(('U', (x-1, y), self.probabilityGrid[x-1][y][0]))
        if x+1 < ROWS: results.append(('D', (x+1, y), self.probabilityGrid[x+1][y][0]))
        if y-1 >= 0: results.append(('L', (x, y-1), self.probabilityGrid[x][y-1][0]))
        if y+1 < COLUMNS: results.append(('R', (x, y+1), self.probabilityGrid[x][y+1][0]))
        return results 
        # END_YOUR_CODE

if __name__ == '__main__':

	# get input from user 
	#parsing feature vector

	logreg = joblib.load('logisticModel.pkl')
	sample = numpy.reshape([400, 145, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], (1, -1))

	board = [[[0, False] for j in range(COLUMNS)] for i in range(ROWS)]
	
	for i in range(ROWS):
		for j in range(COLUMNS):
			sample[0][0] = i
			sample[0][1] = j
			predicted_prob = logreg.predict_proba(sample)
			value = predicted_prob[0][1]
			board[i][j] = [value, False]

    		

  	#print board
  	ucs = searchUtil.UniformCostSearch(verbose=0)
  	startState = (10,10)
  	endState = (7,40)
  	ucs.solve(SearchProblem(startState, endState, board))
  	print ucs.actions
    #return (''.join(ucs.actions)).rstrip()