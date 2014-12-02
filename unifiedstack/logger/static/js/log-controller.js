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
	
        log_app.controller("logController", function($scope,$http,$window,$resource, $compile, $parse){
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
	    $scope.loadDeviceSettings = function () {
		var url = "http://localhost:8000/dslist/1/"
		$http.get(url).then(function (response) {
		    $scope.data = response.data;
		    $('#dynamic_form').append("compilation started...");
		    /*
		    var sampleHtml = '<div>' +
					
				    '</div>';
		    */
		    var sampleHtml = '<div>';
		    for (var i=0; i<$scope.data.length; i++){
			sampleHtml += '<label>' + $scope.data[i].label + '</label>';
			var model_str = 'setting_'+ $scope.data[i].label;
			var model = $parse(model_str);
			model.assign($scope, $scope.data[i].value);
			sampleHtml += '<input type="text" data-ng-model="setting_' + $scope.data[i].label +
					'" value="'+ $scope.data[i].value + '"</input>';
			sampleHtml += '{{ setting_'+ $scope.data[i].label + ' }}'
		    }
		    sampleHtml += '</div>';
		    var compHtml = $compile(sampleHtml)($scope);
		    $('#dynamic_form').append(compHtml);
		    $('#dynamic_form').append("compilation done...");
		    $.each(data, function(i, field) {
			$window.alert(field);
			var sourceHtml = '<div>' +
			    '<label>' + field.label + '</label'> +
			    '<input type="text" data-ng-model="data.' +
			    field.key + '">' +
				    '</div>';
			var compiledHtml = $compile(html)($scope);
			$('#dynamic_form').append("fun fun");
			$window.alert("Came here");
			$scope.device_settings = response.data;
		    });
		    $window.alert("Simply came out");
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
		
	    $scope.newLog = function (data) {
		var Log = $resource('http://localhost:8000/loglist',
		{}, {
		 charge: {method:'POST', params:{charge:true}}
		});
		var log = new Log();
		log.device_id = 1;
		log.message = $scope.new_log_text;
		log.level = 'I';
		log.$save(log,
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
	    //$scope.loadDevices()
	    $scope.loadDeviceSettings()
	});
