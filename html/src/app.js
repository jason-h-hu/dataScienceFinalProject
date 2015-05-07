angular.module('app', [
	//vendor
	'ui.bootstrap',
	'ui.router',

	//app
	'app.partials', //templates
	'app.modules',
	'app.views'
])

.config(function($urlRouterProvider, $stateProvider){
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