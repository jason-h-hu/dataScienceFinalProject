angular.module('app.dateExtensions', [])

// Converts string date in UTC to local time and prints it nicely
.filter('formatDate', function(){
	return function(date) {
		var date = new Date(date);
		date = new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
		var options = {
			year: 'numeric', 
			month: 'short',
			day: 'numeric', 
			hour: '2-digit'
		};
		return date.toLocaleTimeString('en-us', options);
	}
})