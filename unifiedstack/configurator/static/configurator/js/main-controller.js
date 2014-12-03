
var app = angular.module("configurator", ['ngResource', 'ngDialog']);

app.controller("mainController", function($scope,$http,$window,$resource, $compile, $parse, ngDialog, $interpolate, $log){    
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
		var device_type_button = '<li><button style="width:100%" type="button"' +
		    'data-ng-click="showAddDeviceDialog(\'' + device_types[i][0] + '\')"' +
		    'class="btn btn-success">Add '+ device_types[i][1] + ' Settings</button></li>';
		// $window.alert(device_type_button);
		var compiled_device_type_button = $compile(device_type_button)($scope);
		$('#device-type-nav').append(compiled_device_type_button);
	    }
	})
    };
    
    $scope.showAddDeviceDialog = function (selectedDevice) {
	ngDialog.open({            
	    template: '<div ><br/>' +
			'<b "style="color:Green">Add New '+ $scope.data.device_types[selectedDevice] + '</b><br/>' + 
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
			device_html += '<input type"text" placeholder="' + label_tokens[i].trim() +
					'" ng-model="' + subsetting_model + '"/>'
			setting_html += '{{' + subsetting_model + '}};';
		    }	    
		} else{
		    $log.info("Simple  Setting: " + setting_div_id + ", " + label_str);
		    device_html += '<label>' + label + '</label>';
		    device_html += '<input type="text" ng-model="'+ setting_model + '"/>';
		    setting_html += '{{' + setting_model + '}};';
		}
		if (setting_html.length>=1) { // Removing last semicolon from the set of values
		    setting_html = setting_html.substring(0, setting_html.length-1)
		}
		device_html += setting_html + "<br/>";
		var compiled_device_html = $compile(device_html)($scope)
		$('#'+type_setting_div_id).append(compiled_device_html);
		//$scope.result_message = value;
		$scope.data.settings[setting_model] = $interpolate(setting_html);
		//newDevice.settings[setting_model] = setting_html;
		$log.info("Setting model assigned as: " + setting_html);
		
		/*
		$scope.$log.info("adding device setting: " + setting_model);
		var setting = $parse(setting_model);
		setting.assign($scope, "");
		*/
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
		var device_html = '<div id="' + type_setting_id + '" class="type-setting">'
		if (device_type_settings[i].multiple==true) {
		    $log.info(type_setting_id  + ": is multiple");
		    var tokens = device_type_settings[i].label.split('(');
		    var label_main = tokens[0].trim();
		    device_html += '<label>' + label_main + '</label>';
		    $log.log('"addDeviceSetting(' + newDevice.id + ', ' + device_type_settings[i].id +
				    ',\'' + device_type_settings[i].label + '\')"');
		    
		    device_html += '<a href="#" data-ng-click="addDeviceSetting(' + newDevice.id + ', ' + device_type_settings[i].id +
				    ',\'' + device_type_settings[i].label + '\')">Add One</a> | <a href="#" >Add More</a> <br/>';
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
			'<h2>'+ $scope.data.device_types[value.dtype] + " - " + value.title + '</h2>' + 				    
		    '</div>'
		$log.info("Device Added: " + device_html);
		var compiled_device_html = $compile(device_html)($scope)
		// Adding device template to the devices-holder
		$('#devices-holder').append(compiled_device_html);
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
	// If setting type is coming for the first-time
	if( $('#'+type_setting_div_id).length == 0 ){
	    $('#'+device_div_id).append('<div id="' + type_setting_div_id + '"</div>')
	}
	$http.get(url).then(function (response) {
	    var type_setting = response.data;
	    $log.info("Label: " + type_setting.label );
	    device_html = '<div id="' + setting_div_id + '" class="setting">';
	    var label_str = type_setting.label.trim();
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
		    device_html += '<input type"text" placeholder="' + label_tokens[i].trim() +
				    '" ng-model="' + subsetting_model + '"/>'
		    setting_html += '{{' + subsetting_model + '}};';
		}	    
	    } else{
		$log.info("Simple  Setting: " + setting_div_id + ", " + label_str);
		device_html += '<label>' + label_str + '</label>';
		device_html += '<input type="text" ng-model="'+ setting_model + '"/>';
		setting_html += '{{' + setting_model + '}};';
	    }
	    if (setting_html.length>=1) { // Removing last semicolon from the set of values
		setting_html = setting_html.substring(0, setting_html.length-1)
	    }
	    device_html += setting_html + "<br/>";
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
    
    $scope.reloadConfiguration = function(){
	$window.alert("Reloading the configuration...");
    }
    
    /* Initialization of all the existing devices in the */
    $scope.loadExistingDevices = function(){
	$log.info("Starte loading existing devices");
	var url = api_prefix + "configurator/api/v1.0/dlist"
	$http.get(url).then(function (response) {
	    // device_types is an array of arrays: [["S","Switch"],["C","Cobbler"], ...]
	    var devices = response.data;
	    for (var i=0; i<devices.length && i<10; i++){
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

    $scope.configure = function(){
	$log.info("Started Configuration");
	var url = api_prefix + "configurator/api/v1.0/configure";
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
    $scope.loadDeviceTypes();
    $scope.loadExistingDevices();

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

