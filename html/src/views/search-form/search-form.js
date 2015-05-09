angular.module('app.views.searchForm', [])
.controller('SearchCtrl', function($scope, $rootScope, $http, $timeout){
	// HTML Data
	$rootScope.pageTitle = "Find Meals";
	$scope.buttonEnabled = true;
	$scope.date = new Date();

	// TODO: TESTING
	$scope.start = "Providence, RI";
	$scope.end = "San Francisco, CA";

	// Packages up data and route into a post request for $http
	function packagePost(route, data) {
		return {
			url: 'http://localhost:5000/'+route,
			method: 'POST',
			data: data,
			headers: {'Content-Type': 'application/json'}
		}
	}

	// Shows button text that says error and console logs full thing
	function showError(data, status) {
		console.log('Error getting journey:', data, status);
		$rootScope.formError = 'Error getting journey: '+data;
		clearAllData();
	}

	// Saves data from the server to the current meal slot ($rootScope.mealStats.loaded)
	// Calls getMeal() if more need to be loaded
	function getNextMeal(rests) {
		var mealDate = $rootScope.locations[$rootScope.mealStats.loaded][0];
		$rootScope.itinerary[mealDate] = rests; // List of restaurant objects
		
		// Increment progress and get next meal
		$rootScope.mealStats.loaded += 1;
		if ($rootScope.mealStats.loaded < $rootScope.mealStats.total) getMeal();
		else $scope.buttonEnabled = true; // Done searching
	}

	// Saves restaurants data for segment to $scope.itinerary dictionary, where key is datetime
	function getMeal() {
		var mealLocation = $rootScope.locations[$rootScope.mealStats.loaded][1];
		$http(packagePost('restaurants', mealLocation))
		.success(getNextMeal)
		.error(showError);
	}

	// Saves journey from start to end as (date, mealtime) tuples to to $rootScope.locations
	$scope.getJourney = function() {
		$rootScope.clearAllData();
		$scope.buttonEnabled = false;
		$http(packagePost('journey',{'start': $scope.start, 'end': $scope.end, 'date': $scope.date}))
		.success(function (data) {
			$rootScope.locations = data; // List of (date, location) tuples
			$rootScope.mealStats.total = data.length;
			getMeal();
		}).error(showError);
	};
});
