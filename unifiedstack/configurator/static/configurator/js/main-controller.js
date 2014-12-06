
var app = angular.module("configurator", ['ngResource', 'ngDialog', 'ui.bootstrap']);

app.filter('reverse', function() {
    return function(items) {
	return items.slice().reverse();
    };
});

app.controller("mainController", function($scope,$http,$window,$resource, $compile, $parse, ngDialog, $interpolate, $log, $interval){    
    // Result message to be displayed over top of the screen.
    $scope.result_message = "Initial Result Message";
    $scope.$log = $log;
    // Data to be accessed all across configurator SPA page.
    $scope.data = {}
    $scope.data.settings = {}
    $scope.data.devices = []
    $scope.data.device_types = {}
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
	    device_types = response.data;
	    for (var i=0; i<device_types.length; i++){
		$scope.data.device_types[device_types[i][0]] = device_types[i][1];
		/*
		var device_type_button = '<li><button style="width:100%" type="button"' +
		    'data-ng-click="showAddDeviceDialog(\'' + device_types[i][0] + '\')"' +
		    'class="btn btn-success">Add '+ device_types[i][1] + ' Settings</button></li>';
		// $window.alert(device_type_button);
		var compiled_device_type_button = $compile(device_type_button)($scope);
		$('#device-type-nav').append(compiled_device_type_button);
		*/
	    }
	})
    };
    
    $scope.showAddDeviceDialog = function (selectedDevice) {
	ngDialog.open({            
	    template: '<center><div >' +
			'<b "style="color:Green">Add New '+ $scope.data.device_types[selectedDevice] + '</b><br/>' +
			'<table cellspacing:"10"><tr><th>' +
			'Title: </th> <td> <input type="text" ng-model="data.newdevice.title" /> </td></tr> <tr><th>' + 
			'Desc: </th> <td> <input type="text" ng-model="data.newdevice.desc"/> </td></tr> </table>' +
			'<button data-ng-click=addDevice("' + selectedDevice + '")>Add Device</button>' +
		      '</div></center>',
	    plain: true,
	    scope:$scope
	});
    }  

    // Util function to help identify and breakdown compound settings
    // Plus store it into the $scope.devices[i].settings
    
    $scope.addDeviceSetting = function(device_id, type_setting_id, label){
	$log.info("Adding a Setting");
	// Id to be placed in front of the 
	var type_setting_div_id = 'setting-'+ device_id + '-' + type_setting_id;
	var url = api_prefix + "configurator/api/v1.0/dslist/" + device_id;
	var Setting = $resource(url,{});
	var setting = new Setting();
	setting.device_id = device_id;
	setting.type_setting_id = type_setting_id;
	setting.value = " "
	//var newDevice = {}
	setting.$save(setting,
	    //success
	    function( value ){
		// Getting the id associated to
		// the newly added setting
		var newSetting = value;
		var setting_div_id = type_setting_div_id + '-' + newSetting.id;
		var setting_model = 'setting_'+ device_id + "_" +
				    type_setting_id + "_" + newSetting.id;

		$log.info("DeviceSetting id: " + setting_div_id);
		device_html = '<div id="' + setting_div_id + '" class="setting">';
		
		var label_str = label.trim();
		var setting_html = ""
		if(label_str[label_str.length-1]==')'){
		    $log.info("Compound Setting: " + setting_div_id + ", " + label_str);
		    // Removing the last ')' character
		    label_str = label_str.substr(0, label_str.length-1);
		    // Seperating the compound setting main label with
		    // label tokens
		    var tokens = label_str.split('(');
		    var label_main = tokens[0].trim();
		    var label_tokens = tokens[1].split(';');
		    // device_html += '<label>' + label_main + '</label>';
		    for (var i=0; i<label_tokens.length; i++) {
			subsetting_model = setting_model + "_" + i;
			$log.info("Sub Field: " + label_tokens[i].trim() + "; Id: " + subsetting_model);
			device_html += '<input type"text" class="form-control" placeholder="' + label_tokens[i].trim() +
					'" ng-model="' + subsetting_model + '"/>'
			setting_html += '{{' + subsetting_model + '}};';
		    }	    
		} else{
		    $log.info("Simple  Setting: " + setting_div_id + ", " + label_str);
		    device_html += '<label style="float:left">' + label + '</label>';
		    device_html += '<input type="text" class="form-control" ng-model="'+ setting_model + '"/>';
		    setting_html += '{{' + setting_model + '}};';
		}
		if (setting_html.length>=1) { // Removing last semicolon from the set of values
		    setting_html = setting_html.substring(0, setting_html.length-1)
		}
		var compiled_device_html = $compile(device_html)($scope)
		$('#'+type_setting_div_id).append(compiled_device_html);
		//$scope.result_message = value;
		$scope.data.settings[setting_model] = $interpolate(setting_html);
		//newDevice.settings[setting_model] = setting_html;
		$log.info("Setting model assigned as: " + setting_html);
	    },
	    //error
	    function( error ){
		$window.alert("Some trouble adding setting");
	    }
	)
    }

    
    // Add all the Device Settings corresponding to a device
    $scope.addDeviceSettings = function(newDevice){
	// Displaying settings
	url = api_prefix + "configurator/api/v1.0/dtsl/" + newDevice.dtype;
	// $window.alert(url);
	$http.get(url).then(function (response) {
	    var device_type_settings = response.data;
	    for (var i=0; i<device_type_settings.length; i++){
		var type_setting_id = 'setting-'+ newDevice.id + '-' + device_type_settings[i].id;
		$log.info("Type Setting id: " + type_setting_id);
		var device_html = '<div id="' + type_setting_id + '" class="type-setting">';
		var label_str = device_type_settings[i].label.trim();
		if (device_type_settings[i].multiple==true) {
		    var device_html = '<div id="' + type_setting_id + '">';
		    /*
		    var device_html = '<div class="table-responsive">' +
			    '<table class="table table-bordered table-hover table-striped" id="' +
			    type_setting_id + '">';
		    */
		    $log.info(type_setting_id  + ": is multiple");
		    var tokens = device_type_settings[i].label.split('(');
		    var label_main = tokens[0].trim();
		    device_html += '<label>' + label_main + '</label>';
		    $log.log('"addDeviceSetting(' + newDevice.id + ', ' + device_type_settings[i].id +
				    ',\'' + device_type_settings[i].label + '\')"');
		    
		    device_html += '<div style="float:right"><a href="#" data-ng-click="addDeviceSetting(' + newDevice.id + ', ' + device_type_settings[i].id +
				    ',\'' + device_type_settings[i].label + '\')">Add One</a> | <a href="#" >Add More</a></div> <br/>';
		    device_html += '</div>';
		} else if(label_str[label_str.length - 1]==')'){
		    var tokens = device_type_settings[i].label.split('(');
		    var label_main = tokens[0].trim();
		    device_html += '<label>' + label_main + '</label>'
		} else{
		    $log.info(type_setting_id  + ": is not multiple");
		}
		device_html += '</div>'
		var compiled_device_html = $compile(device_html)($scope);
		$('#device-'+newDevice.id).append(compiled_device_html);
		$scope.addDeviceSetting(newDevice.id, device_type_settings[i].id,
					device_type_settings[i].label);
	    }
	})
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
		var device_html =
		    '<div id="device-'+ value.id + '">' +
			'<h2 style="padding-top:0px">'+ $scope.data.device_types[value.dtype] + " - " + value.title + '</h2>' + 				    
		    '</div>'
		$log.info("Device Added: " + device_html);
		var compiled_device_html = $compile(device_html)($scope)
		// Adding device template to the devices-holder
		$('#devices-holder').html(compiled_device_html);
		// $scope.data.devices.push(value.id);
    		$log.info("Device being added into scope: " + value.id );
		$scope.addDeviceSettings(value);
		$log.info("Device after adding Settings: " + value.settings)
		//$scope.result_message = value;
	    },
	    //error
	    function( error ){
		$window.alert("Some trouble adding device");
	    }
	)
    };
    
    $scope.loadExistingDeviceSetting = function(device, setting){
	var url = api_prefix + "configurator/api/v1.0/dtsget/" + setting.device_type_setting_id;
	$log.info("Existing device setting url: " + url);
	var device_div_id = "device-" + device.id;
	var type_setting_div_id = "setting-" + device.id + "-" + setting.device_type_setting_id;
	var setting_div_id = type_setting_div_id + "-" + setting.id;
	var setting_model = "setting_" + device.id + "_" + setting.device_type_setting_id + "_" + setting.id;
	$log.info(device_div_id + ", " + type_setting_div_id + ", " + setting_model);
	var device_html = "";
	
	$http.get(url).then(function (response) {
	    var type_setting = response.data;
	    $log.info("Label: " + type_setting.label );
	    
	    var label_str = type_setting.label.trim();
	    // If setting type is coming for the first-time
	    if( $('#'+type_setting_div_id).length == 0 ){
		device_html = '<div id="' + type_setting_div_id + '" class="type-setting">';
		if (type_setting.multiple==true) {
		    $log.info(type_setting_div_id  + ": is multiple");
		    var tokens = type_setting.label.split('(');
		    var label_main = tokens[0].trim();
		    device_html += '<label>' + label_main + '</label>';
		    $log.log('"addDeviceSetting(' + device.id + ', ' + type_setting.id +
				    ',\'' + type_setting.label + '\')"');
		    
		    device_html += '<div style="float:right"><a href="#" data-ng-click="addDeviceSetting(' + device.id + ', ' + type_setting.id +
				    ',\'' + type_setting.label + '\')">Add One</a> | <a href="#" >Add More</a></div> <br/>';
		} else if(label_str[label_str.length - 1]==')'){
		    var tokens = type_setting.label.split('(');
		    var label_main = tokens[0].trim();
		    device_html += '<label>' + label_main + '</label>'
		} else{
		    $log.info(type_setting_div_id  + ": is not multiple");
		}
		device_html += '</div>'
		var compiled_device_html = $compile(device_html)($scope);
		$('#'+device_div_id).append(compiled_device_html)
	    }
	    
	    device_html = '<div id="' + setting_div_id + '" class="setting">';
	    var setting_html = ""
	    if(label_str[label_str.length-1]==')'){
		$log.info("Compound Setting: " + setting_div_id + ", " + label_str);
		// Removing the last ')' character
		label_str = label_str.substr(0, label_str.length-1);
		// Seperating the compound setting main label with
		// label tokens
		var tokens = label_str.split('(');
		var label_main = tokens[0].trim();
		var label_tokens = tokens[1].split(';');
		var value_tokens = setting.value.trim().split(';');
		// device_html += '<label>' + label_main + '</label>';
		for (var i=0; i<label_tokens.length; i++) {
		    subsetting_model = setting_model + "_" + i;
		    $log.info("Sub Field: " + label_tokens[i].trim() + "; Id: " + subsetting_model);
		    device_html += '<input type"text" class="form-control" placeholder="' + label_tokens[i].trim() +
				    '" ng-model="' + subsetting_model + '"/>'
		    setting_html += '{{' + subsetting_model + '}};';
		    var subsetting_model_var = $parse(subsetting_model);
		    subsetting_model_var.assign($scope, value_tokens[i]);
		}	    
	    } else{
		$log.info("Simple  Setting: " + setting_div_id + ", " + label_str);
		device_html += '<label>' + label_str + '</label>';
		device_html += '<input type="text" class="form-control" ng-model="'+ setting_model + '"/>';
		setting_html += '{{' + setting_model + '}};';
		var setting_model_var = $parse(setting_model);
		setting_model_var.assign($scope, setting.value);
	    }
	    if (setting_html.length>=1) { // Removing last semicolon from the set of values
		setting_html = setting_html.substring(0, setting_html.length-1)
	    }
	    var compiled_device_html = $compile(device_html)($scope)
	    $('#'+type_setting_div_id).append(compiled_device_html);
	    //$scope.result_message = value;
	    $scope.data.settings[setting_model] = $interpolate(setting_html);
	})

    };
    
    $scope.loadExistingDeviceSettings = function(device){
	var url = api_prefix + "configurator/api/v1.0/dslist/" + device.id;
	$http.get(url).then(function (response) {
	    var settings = response.data;
	    for (var i=0; i<settings.length; i++) {
		$log.info("Value: " + settings[i].value);
		$scope.loadExistingDeviceSetting(device, settings[i]);
	    }
	})
    };
    


    
    /* Clear all the settings. Useful while reloading existing settings. */
    $scope.clearSettings = function(){
	$scope.data.settings = {}
	$('#devices-holder').html("");
    }
    
    $scope.loadExistingDevicesOfType = function(device_type){
	$log.info("Starte loading existing devices");
	$scope.clearSettings();
	var url = api_prefix + "configurator/api/v1.0/dlist/" + device_type
	$http.get(url).then(function (response) {
	    var devices = response.data;
	    for (var i=0; i<devices.length; i++){
		$log.info(i + ": Device: Title-" + devices[i].title + " Type-" + devices[i].dtype );
		$log.info($scope.data.device_types[devices[i].dtype]);
		var device_html =
		    '<div id="device-'+ devices[i].id + '">' +
			'<div class="lead" style="padding-top:0px;margin-top:0px">'+ $scope.data.device_types[devices[i].dtype] + " - " + devices[i].title + '</div>' + 				    
		    '</div>'
		$log.info("Device Added: " + device_html);
		var compiled_device_html = $compile(device_html)($scope);
		$('#devices-holder').append(compiled_device_html);
		$scope.loadExistingDeviceSettings(devices[i]);
	    }
	})
    }
    
    /* Initialization of all the existing devices in the */
    $scope.loadExistingDevices = function(){
	$log.info("Starte loading existing devices");
	$scope.clearSettings();
	var url = api_prefix + "configurator/api/v1.0/dlist"
	$http.get(url).then(function (response) {
	    // device_types is an array of arrays: [["S","Switch"],["C","Cobbler"], ...]
	    var devices = response.data;
	    for (var i=0; i<devices.length; i++){
		$log.info(i + ": Device: Title-" + devices[i].title + " Type-" + devices[i].dtype );
		$log.info($scope.data.device_types[devices[i].dtype]);
		var device_html =
		    '<div id="device-'+ devices[i].id + '">' +
			'<h2>'+ $scope.data.device_types[devices[i].dtype] + " - " + devices[i].title + '</h2>' + 				    
		    '</div>'
		$log.info("Device Added: " + device_html);
		var compiled_device_html = $compile(device_html)($scope);
		$('#devices-holder').append(compiled_device_html);
		$scope.loadExistingDeviceSettings(devices[i]);
	    }
	})
    };
    
    $scope.reloadConfiguration = function(){
	$window.alert("Reloading the configuration...");
	var url = api_prefix + "configurator/api/v1.0/reload";
	$http.get(url).then(function (response) {
	    $window.alert("Configuration Completed");
	    $scope.clearSettings()
	    $scope.loadExistingDevices();
	})
    }; 
    
    $scope.loadGeneralConfiguration = function(){
	// Check if General Configuration exists. If not add it and display
	var url = api_prefix + "configurator/api/v1.0/dlist/G"
	$http.get(url).then(function (response) {
	    var devices = response.data;
	    if (devices.length >= 1) {
		$scope.loadExistingDevicesOfType('G');
	    } else{
		$scope.data.newdevice.title = "Common Settings";
		$scope.data.newdevice.desc = "settings common to all the devices";
		$scope.addDevice('G');
	    }
	})
	
    }
    
    $scope.saveConfiguration = function(){
	$log.info("Started Configuration");
	var url = api_prefix + "configurator/api/v1.0/saveconfiguration";
	var Configuration = $resource(url,{});
	var configuration = new Configuration();
	for (var setting in $scope.data.settings) {
	    //var setting_interpolation = $interpolate($scope.data.settings[setting]);
	    setting_value = $scope.$eval($scope.data.settings[setting]);
	    configuration[setting] = setting_value;
	    $log.info("Setting: " + setting + ", " + setting_value);
	    //code
	}
	configuration.$save(configuration);
    }
    
    $scope.configure = function(){
	var url = api_prefix + "configurator/api/v1.0/configure";
	var Configuration = $resource(url,{});
	var conf = new Configuration();
	conf.$save(conf,
	    //success
	    function( value ){
		//$scope.progress_value = 100;
		$window.alert("Configuration Completed Successfully");
	    },
	    //error
	    function( error ){
		$window.alert("Some trouble adding device")
	    }
	 )
    };
    
    $scope.showConfigurationResult = function () {
	$scope.progress_value = 2;
	ngDialog.open({            
	    template: '<div ><br/>' +
			'<b "style="color:Green">Unified Stack Configurator in Progress.<br/> Please donot Interrupt.</b><br/>' + 
			'<progressbar class="progress-striped active" max="100" value="progress_value" type="info"></progressbar>' + 
			'<div style="width:430px; height:400px;overflow-y:auto;overflow-x:auto;">' +
			    '<div ng-repeat="console_log in console_logs | reverse">' +
				'<div><i>{{console_log.console_summary}}</i></div>' +
			    '</div>' +
			'</div>' +
		      '</div>',
	    plain: true,
	    scope:$scope
	   
	});
	$scope.configure()
    }  

    $scope.count = 0;
    $scope.progress_value = 0;
    $scope.loadConsoleMessages = function(){

	var console_url = 'http://localhost:8000/console';
	$http.get(console_url).then(function (response) {
	    $scope.console_logs = response.data; 
	});
	if ($scope.progress_value!=0 && $scope.progress_value<=100) {
	    $scope.progress_value += 2;
	}
	$log.info("Called loading console");
	$scope.count++;
    };
    
    $interval($scope.loadConsoleMessages, 1000);    
    $scope.loadDeviceTypes();
    $scope.loadGeneralConfiguration();
    //$scope.loadExistingDevices();
    // Testing
    // $scope.addDevice('S');
    
});



/*
 * Adding Device Setting - deprecated code
$scope.addDeviceSetting = function(newDevice, device_type_setting){
	$log.info("Adding a Setting");
	var type_setting_id = 'setting-'+ newDevice.id + '-' + device_type_setting.id;
	
	var url = api_prefix + "configurator/api/v1.0/dslist/" + newDevice.id;
	var Setting = $resource(url,{});
	var setting = new Setting();
	setting.device_id = newDevice.id;
	setting.type_setting_id = device_type_setting.id;
	setting.value = " "
	//var newDevice = {}
	setting.$save(setting,
	    //success
	    function( value ){
		// Getting the id associated to
		// the newly added setting
		var newSetting = value;
		var setting_id = type_setting_id + '-' + newSetting.id;
		var setting_model = 'setting_'+ newDevice.id + "_" +
				    device_type_setting.id + "_" + newSetting.id;

		$log.info("DeviceSetting id: " + setting_id);
		device_html = '<div id="' + newSetting.id + '" class="setting">';
		
		var label_str = device_type_setting.label.trim();
		var setting_html = ""
		if(label_str[label_str.length-1]==')'){
		    $log.info("Compound Setting: " + setting_id + ", " + label_str);
		    // Removing the last ')' character
		    label_str = label_str.substr(0, label_str.length-1);
		    // Seperating the compound setting main label with
		    // label tokens
		    var tokens = label_str.split('(');
		    var label_main = tokens[0].trim();
		    var label_tokens = tokens[1].split(';');
		    // device_html += '<label>' + label_main + '</label>';
		    for (var i=0; i<label_tokens.length; i++) {
			subsetting_model = setting_model + "_" + i;
			$log.info("Sub Field: " + label_tokens[i].trim() + "; Id: " + subsetting_model);
			device_html += '<input type"text" placeholder="' + label_tokens[i].trim() +
					'" ng-model="' + subsetting_model + '"/>'
			setting_html += '{{' + subsetting_model + '}};';
		    }	    
		} else{
		    $log.info("Simple  Setting: " + setting_id + ", " + label_str);
		    device_html += '<label>' + device_type_setting.label + '</label>';
		    device_html += '<input type="text" ng-model="'+ setting_model + '"/><br/>';
		    setting_html += '{{' + setting_model + '}};';
		}
		if (setting_html.length>=1) { // Removing last semicolon from the set of values
		    setting_html = setting_html.substring(0, setting_html.length-1)
		}
		device_html += setting_html + "<br/>";
		var compiled_device_html = $compile(device_html)($scope)
		$('#'+type_setting_id).append(compiled_device_html);
		//$scope.result_message = value;
		$scope.data.settings[setting_model] = $interpolate(setting_html);
		//newDevice.settings[setting_model] = setting_html;
		$log.info("Setting model assigned as: " + setting_html);
	    },
	    //error
	    function( error ){
		$window.alert("Some trouble adding setting");
	    }
	)
    }
*/

