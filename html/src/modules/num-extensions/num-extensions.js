angular.module('app.numExtensions', [])

// Turns a number into an integer
.filter('intNum', function(){
	return function(input){
		return parseInt(input, 10);
	};
});