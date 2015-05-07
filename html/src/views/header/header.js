angular.module('app.views.header', [])
  .controller('HeaderCtrl', function($scope){
  	$scope.isCollapsed = true;

  	$scope.navigation = [
  		{ state:'home', title: 'Plan Journey' },
  		{ state:'about', title: 'About' }
  	];
  });
