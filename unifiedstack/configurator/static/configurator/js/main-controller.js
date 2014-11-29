
var app = angular.module("configurator", ['ngResource']);

app.controller("mainController", function($scope,$http,$window,$resource, $compile, $parse){    
    // Result message to be displayed over top of the screen.
    $scope.result_message = "Initial Result Message";
    
    // Data to be accessed all across configurator SPA page.
    $scope.data = {}
    $scope.data.settings = {}
    $scope.data.devices = []
    
    // API endpoint details
    var api_host = "localhost";
    var api_port = 8000;
    var api_prefix = "http://" + api_host + ":" + api_port + "/"
    
    // Loading the Device types supported
    $scope.loadDeviceTypes = function () {
	var url = api_prefix + "configurator/api/v1.0/dtl"
	// $window.alert(url);
	$http.get(url).then(function (response) {
	    // device_types is an array of arrays: [["S","Switch"],["C","Cobbler"], ...]
	    $scope.data.device_types = response.data;
	    for (var i=0; i<$scope.data.device_types.length; i++){
		var device_type_button = '<li><button style="width:100%" type="button"' +
		    'data-ng-click="addDevice(\'' + $scope.data.device_types[i][0] + '\')"' +
		    'class="btn btn-success">Add '+ $scope.data.device_types[i][1] + ' Settings</button></li>';
		// $window.alert(device_type_button);
		var compiled_device_type_button = $compile(device_type_button)($scope);
		$('#device-type-nav').append(compiled_device_type_button);
	    }
	})
    };
    
    // Adding a new device
    $scope.addDevice = function(device_type){
	var url = api_prefix + "configurator/api/v1.0/dtsl/" + device_type
	// $window.alert(url);
	$http.get(url).then(function (response) {
	    var device_type_settings = response.data;
	    var device_html = '<div>'
	    device_html += '<h2>' + device_type + '</h2>'
	    for (var i=0; i<device_type_settings.length; i++){
		var setting_str = 'data.settings.setting_'+ device_type + "_" + device_type_settings[i]["id"];
		$window.alert(setting_str);
		var setting = $parse(setting_str);
		setting.assign($scope, "");
		var device_type_setting_control = '<label>' + device_type_settings[i]["label"] + '</label>' +
		    '<input type="text" ng-model="'+ setting_str + '"/>' + '{{' + setting_str + '}}';
		device_html += device_type_setting_control;
	    }
	    device_html += "</div>";
	    var compiled_device_html = $compile(device_html)($scope);
	    $('#devices-holder').append(compiled_device_html);
	})
    };
    
    $scope.configure = function(){
	var url = api_prefix + "configurator/api/v1.0/dtsl/C"
	var Setting = $resource(url,{}, {charge: {method:'POST', params:{charge:true}}});
	var setting = new Setting();
	setting.fun = "fun";
	var setting_str = 'id';
	var setting_var = $parse(setting_str);
	setting_var.assign(setting, "20");
	setting.$save(setting);
	$window.alert("Configuring Devices " + $scope.data.settings.setting_C_3);
    }
    
    $scope.loadDeviceTypes()
});
