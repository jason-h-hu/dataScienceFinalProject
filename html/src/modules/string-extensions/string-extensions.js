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
