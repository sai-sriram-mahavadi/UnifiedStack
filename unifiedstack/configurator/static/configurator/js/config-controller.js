	var log_services = angular.module("logger_services", ['ngResource']);
	log_services.factory('Log', ['$resource',
	    function($resource){
		return $resource('loglist', {}, {
	    query: {method:'GET', params:{}, isArray:true}
	  });
	}]);
	  
	var log_app = angular.module("configurator", ['logger_services']);
	
	var app = angular.module('myApp', ['ngResource']);

        log_app.controller("configController", function($scope,$http,$window,$resource){
	    $scope.result_message = "Initial Result Message";
	    $scope.ds_url = 'http://localhost:8000/dslist';
	    $scope.dev_url = 'http://localhost:8000/devicelist'
	    $scope.devices = null;
	    $scope.devices_fields = {};
	    $scope.loadDevices = function () {
		$http.get($scope.dev_url).then(function (response) {
		    $scope.devices = response.data;
		    $scope.loadDeviceFields()
		    /*$scope.loadDeviceFields()*/
		});
	    };
	    $scope.loadDeviceFields = function(){
		for (var i = 0; i <= $scope.devices.length - 1; i++) {
		    $scope.device_id = $scope.devices[i].id;
			$window.alert($scope.ds_url + "/" + $scope.device_id + "/");
			$http.get($scope.ds_url + "/" + $scope.device_id + "/").then(function (response) {
			    $scope.devices_fields[$scope.device_id] = response.data;
			});
		}
	    };
	    $scope.validate = function(){
		$window.alert("called")
		$scope.result_message = "Configure Button Clicked";
	    };
	    $scope.loadDevices()
	});
