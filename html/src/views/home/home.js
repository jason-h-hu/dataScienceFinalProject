angular.module('app.views.home', [])
.controller('HomeCtrl', function($scope, $rootScope, $http){
	// Set title of page
	$rootScope.pageTitle = "Home";

	// Testing purposes, maybe date is a good one to keep in
	$scope.start = "Providence, RI";
	$scope.end = "San Francisco, CA";
	$scope.date = new Date();	

	function clear() {
		$scope.restaurantOps = undefined;
		$scope.mealLocations = undefined;
	}

	// Saves restaurants data to $scope.restaurantOps dictionary, where key is datetime
	$scope.singleLocation = function(date, rest) {
		$http({
			url: 'http://localhost:5000/restaurants',
			method: 'POST',
			data: rest,
			headers: {'Content-Type': 'application/json'}
		}).success(function (data, status) {
			if ($scope.restaurantOps === undefined) $scope.restaurantOps = {};
			$scope.restaurantOps[date] = data; // List of restaurant objects
		}).error(function (data, status) {
			console.log('Error getting restaurant for', date, rest, ':', data, status);
		});
	};

	// Saves restaurants data for each location in $scope.mealLocations
	$scope.getRestaurants = function() {
		angular.forEach($scope.mealLocations, function(meal) {
			$scope.singleLocation(meal[0], meal[1]);
		});
	};

	// Saves journey from start to end to $scope.mealLocations
	$scope.getJourney = function() {
		clear();
		$http({
			url: 'http://localhost:5000/journey',
			method: 'POST',
			data: {'start': $scope.start, 'end': $scope.end, 'date': $scope.date},
			headers: {'Content-Type': 'application/json'}
		}).success(function (data, status) {
			$scope.mealLocations = data;
			$scope.getRestaurants();
		}).error(function (data, status) {
			console.log('Error getting journey:', data, status);
		});
	};
});
