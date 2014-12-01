
var app = angular.module("configurator", ['ngResource', 'ngDialog']);

app.controller("mainController", function($scope,$http,$window,$resource, $compile, $parse, ngDialog, $interpolate){    
    // Result message to be displayed over top of the screen.
    $scope.result_message = "Initial Result Message";
    
    // Data to be accessed all across configurator SPA page.
    $scope.data = {}
    $scope.data.settings = {}
    $scope.data.devices = []
    // Details of new device to be accessed across the ngDialog and main page
    $scope.data.newdevice = {}
    
    
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
		    'data-ng-click="showAddDeviceDialog(\'' + $scope.data.device_types[i][0] + '\')"' +
		    'class="btn btn-success">Add '+ $scope.data.device_types[i][1] + ' Settings</button></li>';
		// $window.alert(device_type_button);
		var compiled_device_type_button = $compile(device_type_button)($scope);
		$('#device-type-nav').append(compiled_device_type_button);
	    }
	})
    };
    
    $scope.showAddDeviceDialog = function (selectedDevice) {
	ngDialog.open({            
	    template: '<div ><br/>' +
			'<b "style="color:Green">Add New '+ selectedDevice + '</b><br/>' + 
			'Title: <input type="text" ng-model="data.newdevice.title" /> <br/>' + 
			'Desc: <input type="text" ng-model="data.newdevice.desc"/> <br/>' +
			'<button data-ng-click=addDevice("' + selectedDevice + '")>Add Device</button>' +
		      '</div>',
	    plain: true,
	    scope:$scope
	});
    }  

    // Util function to help identify and breakdown compound settings
    // Plus store it into the $scope.devices[i].settings
    $scope.addDeviceSetting = function(device_id, device_setting){
	
    }
    
    // Adding a new device - Adds a new device to the database and displays the settings
    // it needs at the devices-holder
    $scope.addDevice = function(device_type){
	// Closing the dialog from showAddDeviceDialog
	ngDialog.close()
	
	// Adding device into database
	var url = api_prefix + "configurator/api/v1.0/dlist/"
	var Device = $resource(url,{});
	var device = new Device();
	device.dtype = device_type;
	device.title = $scope.data.newdevice.title;
	device.desc = $scope.data.newdevice.desc;
	//var newDevice = {}
	device.$save(device,
		    //success
		    function( value ){
			// Getting the id associated to
			// the newly added device
			$scope.data.newdevice = value;
			$window.alert($scope.data.newdevice.id + ", " + $scope.data.newdevice.title);
			//$scope.result_message = value;
		    },
		    //error
		    function( error ){
			$window.alert("Some trouble adding device");
		    }
	)
	return;
	$window.alert("Check this out man.");
	//$scope.data.devices.append(newDevice);
	$window.alert($scope.data.newdevice.id)
	// Adding device template to the devices-holder
	$('#devices-holder').append('<div id="'+ $scope.data.newdevice.id + '"></div');	
	
	// $scope.addDeviceSettings($scope.data.newdevice.id);
	
	// Displaying settings
	url = api_prefix + "configurator/api/v1.0/dtsl/" + device_type
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
    $scope.loadDeviceTypes();
    $scope.sample_interpolate_3 = $interpolate('{{sample_interpolate_1}} {{sample_interpolate_2}}!');

    // Testing
    // $scope.addDevice('S');
    
    $scope.interpolateSample = function(){
	$window.alert($scope.$eval($scope.sample_interpolate_3));
    };
});
