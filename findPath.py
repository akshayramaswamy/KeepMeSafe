import csv
import math
import copy
from sklearn import linear_model
from sklearn.externals import joblib
import numpy
import pandas
import random
import mdpUtil 
import distMDP


ROWS = 275
COLUMNS = 317


def solveMDP(probabilityGrid, startRow, startCol, endRow, endCol):

	mdp = distMDP.DistMDP(probabilityGrid, startRow, startCol, endRow, endCol)
	startState = mdp.startState()
	alg = mdpUtil.ValueIteration()
	alg.solve(mdp, .0001)



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
			#sample[0][1] = i
			#sample[0][2] = j
			#predicted_prob = logreg.predict_proba(sample)
    		#value = predicted_prob[0][1]
    		

  	#print board
	solveMDP(board, 10, 10, 15, 15)
	
	#print board



