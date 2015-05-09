angular.module('app.views.itinerary', [])
  .controller('ItineraryCtrl', function($scope, $rootScope){
  	
  	$scope.select = function(index) {
  		var location = $rootScope.locations[index];
  		if (!$rootScope.itinerary[location[0]]) return;
  		$rootScope.mealStats.curr = index;
  	}

  });
