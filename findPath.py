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

def getNewLoc(row, col, action):
	# Up action
    if action == "U":
        newRow = row - 1
        newCol = col
        return (newRow, newCol)

    # Down action
    if action == "D":
        newRow = row + 1
        newCol = col
        return (newRow, newCol)

    # Left action
    if action == "L":
        newRow = row
        newCol = col - 1
        return (newRow, newCol)

    # Right action
    if action == "R":
        newRow = row
        newCol = col + 1
        return (newRow, newCol)

    # Up-left action
    if action == "UL":
        newRow = row - 1
        newCol = col - 1
        return (newRow, newCol)

    # Up-right action
    if action == "UR":
        newRow = row - 1
        newCol = col + 1
        return (newRow, newCol)

    # Down-left action
    if action == "DL":
        newRow = row + 1
        newCol = col - 1
        return (newRow, newCol)

    # Down-right action
    if action == "DR":
        newRow = row + 1
        newCol = col + 1
        return (newRow, newCol)


def solveMDP(probabilityGrid, startRow, startCol, endRow, endCol):

	mdp = distMDP.DistMDP(probabilityGrid, startRow, startCol, endRow, endCol)
	startState = mdp.startState()
	alg = mdpUtil.ValueIteration()
	alg.solve(mdp, .0001)
	optPolicy = alg.pi
	optValue = alg.V
	loc = (startRow, startCol)
	print [l for l in optValue.keys() if optValue[l] > 0]
	#print optPolicy[(10, 10)]
	#print optPolicy[(15, 14)]
	#print optPolicy[(15, 16)]
	print optValue[(13, 13)]
	loc = (endRow, endCol)
	for i in range(10):
		row, col = loc
		newLoc = (row - 1, col - 1)
		print newLoc
		print optPolicy[newLoc]
		loc = newLoc

	# for i in range(100):
	# 	print loc
	# 	action = optPolicy[loc]
	# 	loc = getNewLoc(loc[0], loc[1], action)



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



