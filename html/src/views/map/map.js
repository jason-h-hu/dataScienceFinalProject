angular.module('app.views.map', ['uiGmapgoogle-maps'])
.controller('MapCtrl', function($scope, $rootScope){
	$scope.map = { center: { latitude: 39.82, longitude: -98.57 }, zoom: 4 };

	$scope.setRestaurant = function(idx) {
		$scope.$apply(function(){
			$rootScope.mealStats.curr = idx;
		})
	}
})