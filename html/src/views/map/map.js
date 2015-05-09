angular.module('app.views.map', ['uiGmapgoogle-maps'])
.controller('MapCtrl', function($scope){
	$scope.map = { center: { latitude: 39.82, longitude: -98.57 }, zoom: 4 };
})