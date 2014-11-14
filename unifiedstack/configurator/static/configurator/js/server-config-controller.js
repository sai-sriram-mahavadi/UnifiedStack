	var log_services = angular.module("logger_services", ['ngResource']);
	log_services.factory('Log', ['$resource',
	    function($resource){
		return $resource('loglist', {}, {
	    query: {method:'GET', params:{}, isArray:true}
	  });
	}]);
	  
	var log_app = angular.module("configurator", ['logger_services']);
	log_app.factory("poollingFactory", function($interval) {
	    var timeIntervalInSec = 5;
	    function callFnOnInterval(fn, timeInterval) {
		return $interval(fn, 1000 * timeIntervalInSec);        
	    };
	    return {
		callFnOnInterval: callFnOnInterval
	    };
	});
        log_app.controller("serverConfigController", function($scope,$http,$window,$resource, $interval){
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
	    $scope.count = 0;
	    $scope.load_console_messages = function(){

		var console_url = 'http://localhost:8000/console';
		$http.get(console_url).then(function (response) {
		    $scope.console_logs = response.data; 
		});
	    
		$scope.count++;
	    };
	    
	    
	    $interval($scope.load_console_messages, 1000)
	    //poollingFactory.callFnOnInterval($scope.load_console_messages);

	});
