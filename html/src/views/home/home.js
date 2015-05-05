angular.module('app.views.home', ['angular-progress-arc'])
.controller('HomeCtrl', function($scope, $rootScope, $http, $timeout){
	// Set title of page
	$rootScope.pageTitle = "Home";
	
	var buttonText = 'Journey';
	var searchProg = 0.05;

	$scope.buttonText = buttonText;

	// Testing purposes, maybe date is a good one to keep in
	$scope.start = "Providence, RI";
	$scope.end = "San Francisco, CA";
	$scope.date = new Date();	

	function resetProgress() {
		$scope.progress = 0.0;
		$scope.segment = 0;
	}

	function clear() {
		resetProgress();
		$scope.mealLocations = undefined;
		$scope.restaurantOps = undefined;
	}

	function incProg(prog) {
		var total = $scope.mealLocations ? $scope.mealLocations.length : 0;
		$scope.segment += 1;
		$scope.progress = prog ? prog : Math.min(($scope.segment)/(total+1)+searchProg, 1.0);
		$scope.buttonText = 'Planned '+parseInt(100*$scope.progress, 10)+'%';
		if ($scope.segment==total+1) {
			$scope.buttonText = 'Meals Planned';
			$timeout(function() {
				$scope.buttonText = buttonText;
				resetProgress();
			}, 4000);
		}
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
			incProg();
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
		$scope.segment = -1;
		incProg(searchProg);
		$http({
			url: 'http://localhost:5000/journey',
			method: 'POST',
			data: {'start': $scope.start, 'end': $scope.end, 'date': $scope.date},
			headers: {'Content-Type': 'application/json'}
		}).success(function (data, status) {
			$scope.mealLocations = data;
			$scope.segment = 0;
			incProg();
			$scope.getRestaurants();
		}).error(function (data, status) {
			console.log('Error getting journey:', data, status);
		});
	};
}).filter('intNum', function(){
	return function(input){
		return parseInt(input, 10);
	};
});
