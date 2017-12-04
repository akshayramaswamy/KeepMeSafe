import searchUtil
from evaluateCrime import LocationGrid, SafePathFeatureExtractor
from sklearn.externals import joblib
import math
import numpy
import matplotlib.pyplot as plt



if __name__ == '__main__':

	# chicago dimensions
	mileBlockSize = 0.1
	topLeft = (42.038730, -87.969580)
	bottomRight = (41.640738, -87.510901)

	locationGrid = LocationGrid(mileBlockSize, topLeft, bottomRight)
	logreg = joblib.load('logisticModel.pkl')





#  Englewood 41.778473, -87.641990
	row = locationGrid.latToRow(41.778473)
	col = locationGrid.longToCol(-87.641990)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

# West Garfield Park, 41.881322, -87.729652

	row = locationGrid.latToRow(41.881322)
	col = locationGrid.longToCol(-87.729652)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]




#East Garfield Park - 41.877249, -87.706017
	row = locationGrid.latToRow(41.877249)
	col = locationGrid.longToCol(-87.706017)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

#West Englewood - 41.778056, -87.666707
	row = locationGrid.latToRow(41.778056)
	col = locationGrid.longToCol(-87.666707)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

# Fuller Park 41.810802, -87.632639
	featureExtractor = SafePathFeatureExtractor(['Row', 'Col', 'Day', 'Hr'], \
		[locationGrid.numRows(), locationGrid.numCols(), 7, 24])
	row = locationGrid.latToRow(41.778473)
	col = locationGrid.longToCol(-87.641990)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]
	
# Edison Park 42.008285, -87.813701
	row = locationGrid.latToRow(42.008285)
	col = locationGrid.longToCol(-87.813701)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

#Andersonville - 41.984870, -87.674503
	row = locationGrid.latToRow(41.984870)
	col = locationGrid.longToCol(-87.674503)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

#Forest Glen - 41.991700, -87.758720
	row = locationGrid.latToRow(41.991700)
	col = locationGrid.longToCol(-87.758720)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

#Greektown - 41.876983, -87.747183
	row = locationGrid.latToRow(41.776983)
	col = locationGrid.longToCol(-87.747183)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]

#Mount Greenwood - 41.691420, -87.713285
	row = locationGrid.latToRow(41.691420)
	col = locationGrid.longToCol(-87.713285)
	sample = featureExtractor.extract([row, col, 2, 23])
	predicted_prob = logreg.predict_proba(sample)
	print predicted_prob[0][1]