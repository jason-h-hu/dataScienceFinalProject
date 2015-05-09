angular.module('app.views.restaurants', [])
.controller('RestaurantsCtrl', function ($scope) {
	$scope.mealExpand = function(rest) {
		rest.expanded = !rest.expanded;
	}
});