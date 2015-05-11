angular.module('app', [
	//vendor
	'ui.bootstrap',
	'ui.router',

	//app
	'app.partials', //templates
	'app.modules',
	'app.views'
])

.config(function($urlRouterProvider, $stateProvider, uiGmapGoogleMapApiProvider){

    uiGmapGoogleMapApiProvider.configure({
        v: '3.17',
        libraries: 'drawing,geometry,visualization'
    });


	// Set up states
	$stateProvider.state('home',{
        url: '/',
        views: {
            'itinerary': {
                templateUrl: 'views/itinerary/itinerary.tpl.html'
            },
            'search-form': {
                templateUrl: 'views/search-form/search-form.tpl.html'
            },
            'map': {
                templateUrl: 'views/map/map.tpl.html'
            },
            'restaurants': {
                templateUrl: 'views/restaurants/restaurants.tpl.html'
            }
        }
    })

	// Configure other router providers
	$urlRouterProvider.otherwise('/');
})

.controller('AppCtrl', function($scope, $rootScope) {

    // Clear all saved data to default
    $rootScope.clearAllData = function(){
        $rootScope.isLoading = false; // Whether we're fetching route data
        $rootScope.locations = []; // List of (date, location) tuples
        $rootScope.itinerary = {}; // Dict of location -> list of restaurants
        $rootScope.mealStats = {
            loaded: 0,  // Farthest meal that's fully loaded
            total:  0,  // Total number of meals
            curr:   0   // Index of meal we've selected in frontend
        }
    }

    // Returns with range in array
    $rootScope.range = function(n) {
        return new Array(n);
    };

    $scope.appName = 'Chipmunk';
    $rootScope.clearAllData();
});
angular.module('app.modules', [
	'app.numExtensions',
	'app.phoneFilter',
	'app.dateExtensions'
]);

angular.module('app.views', [
  'app.views.itinerary',
  'app.views.map',
  'app.views.restaurants',
  'app.views.searchForm'
 ])

angular.module('app.dateExtensions', [])

// Converts string date in UTC to local time and prints it nicely
.filter('formatDate', function(){
	return function(date) {
		var date = new Date(date);
		date = new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
		var options = {
			year: 'numeric', 
			month: 'short',
			day: 'numeric', 
			hour: '2-digit'
		};
		return date.toLocaleTimeString('en-us', options);
	}
})
angular.module('app.metaModifier', [])
.provider('metaModifier', function($compileProvider, $rootScopeProvider, $rootElementProvider) {
  var added = {};

  this.$get = function() {
    var Meta = {};
	var head = angular.element(document.getElementsByTagName('head')[0]);

    // Used to add metadata to the head
    Meta.addMap = function(meta) {
    	head.append(processMap(meta));
    	angular.forEach(meta, function(value, key){
    		added.key = value;
    	});
    };

    // Takes a key and value and makes a meta tag
	var makeMetaTag = function(key, value) {
		return '<meta name="'+key+'" content="'+value+'">';
	};

	// Take mapped data in mappedData and 
	var processMap = function(metadataMap) {
		var text = '';
		angular.forEach(metadataMap, function(value, key){
			if (added.key) return; // Don't add same one twice
			text += makeMetaTag(key, value);
		});
		return text;
	};
	return Meta;
  };
});

angular.module('app.numExtensions', [])

// Turns a number into an integer
.filter('intNum', function(){
	return function(input){
		return parseInt(input, 10);
	};
});
angular.module('app.phoneFilter', [])
.filter('tel', function () {
    return function (tel) {
        if (!tel) return '';

        var value = tel.toString().trim().replace(/-/g, '');

        if (value.match(/[^0-9]/)) {
            return tel;
        }

        var country, city, number;

        switch (value.length) {
            case 10: // +1PPP####### -> C (PPP) ###-####
                country = 1;
                city = value.slice(0, 3);
                number = value.slice(3);
                break;

            case 11: // +CPPP####### -> CCC (PP) ###-####
                country = value[0];
                city = value.slice(1, 4);
                number = value.slice(4);
                break;

            case 12: // +CCCPP####### -> CCC (PP) ###-####
                country = value.slice(0, 3);
                city = value.slice(3, 5);
                number = value.slice(5);
                break;

            default:
                return tel;
        }

        if (country == 1) country = "";

        number = number.slice(0, 3) + '-' + number.slice(3);

        return (country + " (" + city + ") " + number).trim();
    };
});

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

angular.module('app.views.itinerary', [])
  .controller('ItineraryCtrl', function($scope, $rootScope){
  	
  	$scope.select = function(index) {
  		var location = $rootScope.locations[index];
  		if (!$rootScope.itinerary[location[0]]) return;
  		$rootScope.mealStats.curr = index;
  	}

  });

angular.module('app.views.map', ['uiGmapgoogle-maps'])
.controller('MapCtrl', function($scope, $rootScope){
	$scope.map = { center: { latitude: 39.82, longitude: -98.57 }, zoom: 4 };

	$scope.setRestaurant = function(idx) {
		$scope.$apply(function(){
			$rootScope.mealStats.curr = idx;
		})
	}
})
angular.module('app.views.restaurants', [])
.controller('RestaurantsCtrl', function ($scope) {
	$scope.mealExpand = function(rest) {
		rest.expanded = !rest.expanded;
	}
});
angular.module('app.views.searchForm', [])
.controller('SearchCtrl', function($scope, $rootScope, $http, $timeout){
	$rootScope.pageTitle = "Find Meals";
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
		else $rootScope.isLoading = false; // Done searching
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
		$rootScope.isLoading = true;
		$http(packagePost('journey',{'start': $scope.start, 'end': $scope.end, 'date': $scope.date}))
		.success(function (data) {
			$rootScope.locations = data; // List of (date, location) tuples
			$rootScope.mealStats.total = data.length;
			getMeal();
		}).error(showError);
	};
});
