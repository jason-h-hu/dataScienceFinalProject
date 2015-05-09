angular.module('app.views.home', ['angular-progress-arc'])
.controller('HomeCtrl', function($scope, $rootScope, $http, $timeout){
	// Set title of page
	$rootScope.pageTitle = "Home";
	
	var buttonText = 'New Journey';
	var searchProg = 0.05;

	// Data for the HTML
	$scope.buttonText = buttonText;
	$scope.locations = []; // List of (date, location) tuples
	$scope.itinerary = {}; // Dict of location -> list of restaurants
	$scope.currMeal = 0; // Index of meal we're on
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
		$scope.locations = [];
		$scope.itinerary = {};
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
		var total = $scope.locations.length;
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

	// Saves restaurants data for segment to $scope.itinerary dictionary, where key is datetime
	function getRestaurants(seg) {
		var meal = $scope.locations[seg];
		var mealDate = meal[0];
		var mealLocation = meal[1];
		$http({
			url: 'http://localhost:5000/restaurants',
			method: 'POST',
			data: mealLocation,
			headers: {'Content-Type': 'application/json'}
		}).success(function (listOfRestaurants, status) {
			$scope.itinerary[mealDate] = listOfRestaurants; // List of restaurant objects
			incrementMealProgress();
		}).error(function (data, status) {
			showError(data, status);
			console.log('Specifically, error getting restaurant for', mealDate, mealLocation);
		});
	}

	// Shows button text that says error and console logs full thing
	function showError(data, status) {
		$scope.buttonText = 'Error getting journey (server returned status '+status+')';
		console.log('Error getting journey:', data, status);
		clear();
	}

	// Saves journey from start to end to $scope.locations
	$scope.getJourney = function() {
		clear();
		$scope.buttonText = 'Getting mealtimes...';
		$http({
			url: 'http://localhost:5000/journeyWithPath',
			method: 'POST',
			data: {'start': $scope.start, 'end': $scope.end, 'date': $scope.date},
			headers: {'Content-Type': 'application/json'}
		}).success(function (data, status) {
			$scope.path = data["path"]
			$scope.locations = data["locations"];
			setProgress(searchProg, 'Finding restuarants...');
			getRestaurants(0);
		}).error(function (data, status) {
			showError(data, status);
		});
	};
});
