angular.module('app.views.home', ['angular-progress-arc'])
.controller('HomeCtrl', function($scope, $rootScope, $http, $timeout){
	// Set title of page
	$rootScope.pageTitle = "Home";
	
	var buttonText = 'New Journey';
	var searchProg = 0.05;

	$scope.buttonText = buttonText;

	// Testing purposes, maybe date is a good one to keep in
	$scope.start = "Providence, RI";
	$scope.end = "San Francisco, CA";
	$scope.date = new Date();	

	// Resets progress and deletes all data
	function clear() {
		$http({
			url: 'http://localhost:5000/clear',
			method: 'POST'
		});
		resetProgress();
		$scope.mealLocations = undefined;
		$scope.restaurantOps = undefined;
	}

	// Saves restaurants data for segment to $scope.restaurantOps dictionary, where key is datetime
	function getRestaurants(seg) {
		var meal = $scope.mealLocations[seg];
		var m_rest = meal[1];
		var m_date = meal[0];
		$http({
			url: 'http://localhost:5000/restaurants',
			method: 'POST',
			data: m_rest,
			headers: {'Content-Type': 'application/json'}
		}).success(function (data, status) {
			if ($scope.restaurantOps === undefined) $scope.restaurantOps = {};
			$scope.restaurantOps[m_date] = data; // List of restaurant objects
			incrementMealProgress();
		}).error(function (data, status) {
			showError(data, status);
			console.log('Specifically, error getting restaurant for', m_date, m_rest);
		});
	}

	// Resets progress to 0 along with segment
	function resetProgress() {
		$scope.progress = 0.0;
		$scope.segment = 0;
	}

	function setProgress(prog, text){
		$scope.progress = prog;
		$scope.buttonText = text;
	}

	function incrementMealProgress() {
		$scope.segment += 1;
		var total = $scope.mealLocations ? $scope.mealLocations.length : 0;
		var seg = $scope.segment;

		// Bounds between 0.05 (searchProg) and 1.0) and sets text
		$scope.progress = Math.max(searchProg, Math.min(seg/total, 1.0));
		$scope.buttonText = 'Got restaurants for meal '+seg+'/'+total+'...';
		
		// Gets next meal
		if (seg < total) {
			getRestaurants(seg);
		}

		// Sets progress to 100% and relevant text, with timeout to reset to new state
		else {
			$scope.progress = 1.0;
			$scope.buttonText = 'Done planning meals!';
			$timeout(function() {
				$scope.buttonText = buttonText;
				resetProgress();
			}, 4000);
		}
	}

	// Shows button text that says error and console logs full thing
	function showError(data, status) {
		$scope.buttonText = 'Error getting journey (server returned status '+status+')';
		console.log('Error getting journey:', data, status);
		clear();
	}

	// Saves journey from start to end to $scope.mealLocations
	$scope.getJourney = function() {
		clear();
		$scope.buttonText = 'Getting mealtimes...';
		$http({
			url: 'http://localhost:5000/journey',
			method: 'POST',
			data: {'start': $scope.start, 'end': $scope.end, 'date': $scope.date},
			headers: {'Content-Type': 'application/json'}
		}).success(function (data, status) {
			$scope.mealLocations = data;
			setProgress(searchProg, 'Finding restuarants...');
			getRestaurants(0);
		}).error(function (data, status) {
			showError(data, status);
		});
	};
}).filter('intNum', function(){
	return function(input){
		return parseInt(input, 10);
	};
});
