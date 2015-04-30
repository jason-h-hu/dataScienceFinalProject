angular.module('app.views.home', [])
  .controller('HomeCtrl', function($scope, $rootScope){
    // Set title of page
    $rootScope.pageTitle = "Home";
  });
