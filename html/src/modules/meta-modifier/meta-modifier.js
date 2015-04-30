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
