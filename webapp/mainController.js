'use strict';

var keepMeSafeApp = angular.module('keepMeSafeApp', ['ngRoute', 'ngMaterial', 'ngResource', 'ngAnimate', 'ngCookies', 'ngMap']);

keepMeSafeApp.controller('MainController', ['$scope', '$rootScope', '$location', '$mdDialog', '$resource', '$cookies',
    function ($scope, $rootScope, $location, $mdDialog, $resource, $cookies, NgMap) {

        $scope.main = {};
        $scope.main.title = 'Search';

        var heatmap;
        $scope.$on('mapInitialized', function(event, map) {
            heatmap = new google.maps.visualization.HeatmapLayer({
                data: []
            });
            heatmap.setMap(map);
        });


        $scope.hours = [];
        for (var i = 0; i < 24; i++) {
            $scope.hours.push(i);
        }

        $scope.models = ['Safest', 'Shortest', 'Optimal'];
        $scope.days = [['Sunday', 0], ['Monday', 1], ['Tuesday', 2], ['Wednesday', 3], ['Thursday', 4], 
            ['Friday', 5], ['Saturday', 6]];

        var showAlert = function (message) {
            $scope.alertMessage = message;

            $mdDialog.show({
                contentElement: '#alertDialog',
                parent: angular.element(document.body)
            });
        };

        $scope.toggle = function () {
            // Component lookup should always be available since we are not using `ng-if`
            $mdSidenav('left').toggle();
        };

        $scope.hideAlert = function () {
            $mdDialog.hide();
        };

        $scope.submit = function() {

            if ($scope.main.loading) {
                showAlert('Please be patient as we load your results.');
                return;
            }

            // check that all fields are filled 
            if ($scope.main.start === undefined || $scope.main.end === undefined || $scope.main.day === undefined || $scope.main.hour === undefined
                || $scope.main.model === undefined || ($scope.main.model === 'Optimal' && $scope.main.maxTime === undefined)) {
                showAlert('Please fill out all fields.');
                return;
            }

            if ($scope.main.model === 'Optimal' && $scope.main.maxTime < 0) {
                showAlert('Please enter a non-negative maximum time to search.');
                return;
            }

            $scope.main.loading = true;
            var pathRes = $resource('/getPath')
            var pathInfo = pathRes.save({'start': $scope.main.start, 'end': $scope.main.end, 'day': $scope.main.day, 'hour': $scope.main.hour, 'model': $scope.main.model, 'maxTime': $scope.main.maxTime}, function () {
                // success
                showAlert('Path was successfully generated!');
                $scope.main.path = pathInfo.path;

                console.log(pathInfo.crimeData);

                var crimeData = pathInfo.crimeData.map(function(currentVal) {
                    return {location: new google.maps.LatLng(currentVal['lat'], currentVal['long']), weight: currentVal['prob']};
                });

                console.log(crimeData);

                heatmap.setOptions({
                    'data': crimeData,
                    'radius': pathInfo.radius
                });

                $scope.main.loading = false;
            }, function (err) {
                showAlert(err['data']);
                $scope.main.loading = false;
            });   
        };
    }]);
