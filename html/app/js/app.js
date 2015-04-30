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
angular.module('app.modules', [
	'app.metaModifier'
]);

angular.module('app.views', [
  'app.views.footer',
  'app.views.header',
  'app.views.home'
 ])
angular.module('app.metaModifier', [])
.provider('metaModifier', function($compileProvider, $rootScopeProvider, $rootElementProvider) {
  var added = {};

  this.$get = function() {
    var Meta = {};
	var head = angular.element(document.getElementsByTagName('head')[0]);

    // Used to add metadata to the head
    Meta.addMap = function(meta) {
    	head.append(processMap(meta));
    	angular.forEach(meta, function(value, key){
    		added.key = value;
    	});
    };

    // Takes a key and value and makes a meta tag
	var makeMetaTag = function(key, value) {
		return '<meta name="'+key+'" content="'+value+'">';
	};

	// Take mapped data in mappedData and 
	var processMap = function(metadataMap) {
		var text = '';
		angular.forEach(metadataMap, function(value, key){
			if (added.key) return; // Don't add same one twice
			text += makeMetaTag(key, value);
		});
		return text;
	};
	return Meta;
  };
});

angular.module('app.phoneFilter', [])
.filter('tel', function () {
    return function (tel) {
        if (!tel) return '';

        var value = tel.toString().trim().replace(/-/g, '');

        if (value.match(/[^0-9]/)) {
            return tel;
        }

        var country, city, number;

        switch (value.length) {
            case 10: // +1PPP####### -> C (PPP) ###-####
                country = 1;
                city = value.slice(0, 3);
                number = value.slice(3);
                break;

            case 11: // +CPPP####### -> CCC (PP) ###-####
                country = value[0];
                city = value.slice(1, 4);
                number = value.slice(4);
                break;

            case 12: // +CCCPP####### -> CCC (PP) ###-####
                country = value.slice(0, 3);
                city = value.slice(3, 5);
                number = value.slice(5);
                break;

            default:
                return tel;
        }

        if (country == 1) country = "";

        number = number.slice(0, 3) + '-' + number.slice(3);

        return (country + " (" + city + ") " + number).trim();
    };
});

angular.module('app.stringExtensions', [])
.factory('StringExtensions', function() {
	var StrExten = {};

	// Trims whitespace, turns it to lowercase, and changes special characters to dashes
	StrExten.hrefify = function(string) {
		if (!string) return "";
		return string.trim()
             .toLowerCase()
             .replace(/[\/. ,:-]+/g, "-");
	};

	// Returns if a string starts with looking
	StrExten.startsWith = function(string, looking){
		return string.lastIndexOf(looking, 0) === 0;
	};

	// Gets last dash component (issue-name-id returns id alone)
	StrExten.lastDashComponent = function(string) {
		var array = string.split('-');
		if (array.length === 0) return "";
		if (array.length === 1) return array[0];
		return array[array.length-1];
	};

	// Removes character
	StrExten.removeChar = function(string, char) {
		var reg = new RegExp(char, "g");
		return string.replace(reg,'');
	};

	// Nth occurence
	StrExten.nthOccurrence = function(string, char, nth) {
		var first_index = string.indexOf(char);
		var length_up_to_first_index = first_index + 1;

		if (nth == 1) {
			return first_index;
		} else {
			var string_after_first_occurrence = string.slice(length_up_to_first_index);
			var next_occurrence = StrExten.nthOccurrence(string_after_first_occurrence, char, nth - 1);

			if (next_occurrence === -1) {
				return -1;
			} else {
				return length_up_to_first_index + next_occurrence;  
			}
		}
	};

	return StrExten;
});

angular.module('app.views.footer', [])
  .controller('FooterCtrl', function($scope){
  	$scope.date = new Date();
  });

angular.module('app.views.header', [])
  .controller('HeaderCtrl', function($scope){
  	$scope.isCollapsed = true;

  	$scope.navigation = [
  		{ state:'home', title: 'Home' }
  	];
  });

angular.module('app.views.home', [])
  .controller('HomeCtrl', function($scope, $rootScope){
    // Set title of page
    $rootScope.pageTitle = "Home";
  });
