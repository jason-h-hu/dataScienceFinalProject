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

    $scope.appName = 'Chipmunk';
    $rootScope.clearAllData();
});