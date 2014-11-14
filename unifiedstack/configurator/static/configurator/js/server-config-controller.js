	var log_services = angular.module("logger_services", ['ngResource']);
	log_services.factory('Log', ['$resource',
	    function($resource){
		return $resource('loglist', {}, {
	    query: {method:'GET', params:{}, isArray:true}
	  });
	}]);
	  
	var log_app = angular.module("configurator", ['logger_services']);
	
        log_app.controller("serverConfigController", function($scope,$http,$window,$resource){
	    $scope.result_message = "Initial Result Message";
	
	    $scope.configure = function(){
		$window.alert("Congiguration started. Please donot interrupt in between");
		var Configuration = $resource('http://localhost:8000/configuration',
		{}, {
		 charge: {method:'POST', params:{charge:true}}
		});
		var conf = new Configuration();
		conf.general_pool_id = $scope.general_pool_id;
		conf.$save(conf,
		    //success
		    function( value ){
			$window.alert("Configuration Completed")

		    },
		    //error
		    function( error ){
			$window.alert("Some trouble adding device")
		    }
		 )
		};


	});
