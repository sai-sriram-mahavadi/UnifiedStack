	var log_services = angular.module("logger_services", ['ngResource']);
	log_services.factory('Log', ['$resource',
	    function($resource){
		return $resource('loglist', {}, {
	    query: {method:'GET', params:{}, isArray:true}
	  });
	}]);
	  
	var log_app = angular.module("logger", ['logger_services']);
	
	var app = angular.module('myApp', ['ngResource']);

	app.factory("Post", function($resource) {
	  return $resource("http://localhost:8000/:id");
	});
	
        log_app.controller("logController", function($scope,$http,$window,$resource){
	    $scope.name = "fun";
	    $scope.device_title = "";
	    $scope.device_desc = "";
	    $scope.url = "http://localhost:8000/devicelist";
	    $scope.selectedClient = null;
	    $scope.log_devices = null;
	    $scope.loadDevices = function () {
		$scope.data = "yes data is not collected";
		$http.get($scope.url).then(function (response) {
		    $scope.data = response.data;
		    $scope.log_devices = response.data;
		});
	    };
	    $scope.newDevice = function (data) {
		var Device = $resource('http://localhost:8000/devicelist',
		{}, {
		 charge: {method:'POST', params:{charge:true}}
		});
		var dev = new Device();
		dev.title = $scope.device_title;
		dev.desc = $scope.device_desc;
		dev.$save(dev,
		    //success
		    function( value ){
			$scope.loadDevices()
		    },
		    //error
		    function( error ){
			$window.alert("Some trouble adding device")
		    }
		 )
		};
	    $scope.loadDevices()
	    
	});
