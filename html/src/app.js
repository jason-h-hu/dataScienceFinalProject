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
            'header': {
                templateUrl: 'views/header/header.tpl.html'
            },
            'content': {
                templateUrl: 'views/home/home.tpl.html'
            },
            'map@home': {
                templateUrl: 'views/map/map.tpl.html'
            },
            'restaurants@home': {
                templateUrl: 'views/restaurants/restaurants.tpl.html'
            },
            'footer': {
                templateUrl: 'views/footer/footer.tpl.html'
            }
        }
    })

    $stateProvider.state('about',{
        url: '/about',
        views: {
            'header': {
                templateUrl: 'views/header/header.tpl.html'
            },
            'content': {
                templateUrl: 'views/about/about.tpl.html'
            },
            'footer': {
                templateUrl: 'views/footer/footer.tpl.html'
            }
        }
    })

	// Configure other router providers
	$urlRouterProvider.otherwise('/');
})

.controller('AppCtrl', function($scope) {
	$scope.appName = 'Road Trip';
});