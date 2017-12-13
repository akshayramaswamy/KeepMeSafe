# ./application.py

from flask import Flask, jsonify, make_response, request, session, redirect
from apiclient.discovery import build
from apiclient.errors import HttpError
import requests
import sys
import configparser

from helpers.evaluateCrime import LocationGrid, SafePathFeatureExtractor
from helpers.pathUCS import *
import helpers.searchUtil

# KEYS = {}
MILE_BLOCK_SIZE = 0.1
CHICAGO_TOP_LEFT = (42.038730, -87.969580)
CHICAGO_BOTTOM_RIGHT = (41.640738, -87.510901)
KEYS = {}
SAVED_MODEL = 'logisticModel.pkl'

application = Flask(__name__, static_url_path='', static_folder='')

@application.route("/")
def index():
    # redirect to home page
    return redirect('/main.html')


@application.route('/getPath', methods=['POST'])
def getPath():
    data = request.get_json()

    start = data['start']
    end = data['end']
    hour = data['hour']
    day = data['day']
    model = data['model']

    startLatLong = addressToLatLong(start, KEYS['MAPS_GEOENCODING_KEY'])
    endLatLong = addressToLatLong(end, KEYS['MAPS_GEOENCODING_KEY'])

    if startLatLong is None or endLatLong is None:
        return make_response("Failed to resolve start or end address.", 400)

    locationGrid = LocationGrid(MILE_BLOCK_SIZE, CHICAGO_TOP_LEFT, CHICAGO_BOTTOM_RIGHT)
    start = locationGrid.latLongToRowCol(startLatLong)
    end = locationGrid.latLongToRowCol(endLatLong)

    if not locationGrid.inBounds(start[0], start[1]) or not locationGrid.inBounds(end[0], end[1]):
        return make_response("We currently do not support addresses outside of the Chicago area. Sorry!", 400)

    logreg = joblib.load(SAVED_MODEL)

    featureExtractor = SafePathFeatureExtractor(['Row', 'Col', 'Day', 'Hr'], \
        [locationGrid.numRows(), locationGrid.numCols(), 7, 24])

    heatMapData = []
    for i in range(locationGrid.numRows()):
        for j in range(locationGrid.numCols()):
            # walking on Tuesday at 11 PM
            sample = featureExtractor.extract([i, j, day, hour])
            predicted_prob = logreg.predict_proba(sample)
            locationGrid.locationGrid[i][j] = predicted_prob[0][1]
            heatMapData.append({'lat': locationGrid.rowToLat(i), 'long': locationGrid.colToLong(j), 'prob': predicted_prob[0][1] * 100})

    ucs = searchUtil.UniformCostSearch(verbose=0)

    if model == 'Shortest':
        ucs.solve(ShortestPath(start, end, locationGrid))
    elif model == 'Safest':
        ucs.solve(SafestPath(start, end, locationGrid))
    elif model == 'Optimal':
        ucs.solve(OptimalPath(start, end, locationGrid, data['maxTime']))
    else:
        return make_response("Please select a valid model.", 400)

    actions = ucs.actions

    if actions is None:
        return make_response("No path found. If using optimal path, try increasing the maximum time allowed.", 400)

    path = snapPoints(actions, start, locationGrid, KEYS['MAPS_ROAD_KEY'])
    if path is None:
        return make_response("Failed to create path.", 400)

    return jsonify({'path': path, 'crimeData': heatMapData, 'radius': MILE_BLOCK_SIZE * 200})


def read_keys():
    config = configparser.ConfigParser()
    config.read('keys.ini')

    for key, value in config['keepmesafe'].iteritems():
        # read into global keys
        KEYS[key.upper()] = value

if __name__ == "__main__":
    read_keys()
    application.run()

