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
		conf.general_name_server = $scope.general_name_server;
		conf.general_enable_fi = $scope.general_enable_fi;
		conf.general_hostname_port_mapping_1 = $scope.general_hostname_port_mapping_1;
		conf.general_hostname_port_mapping_2 = $scope.general_hostname_port_mapping_2;
		conf.general_hostname_port_mapping_3 = $scope.general_hostname_port_mapping_3;
		conf.general_rhel_image_url = $scope.general_rhel_image_url;
		conf.cobbler_compute_hosts = $scope.cobbler_compute_hosts;
		conf.cobbler_network_hosts = $scope.cobbler_network_hosts;
		conf.cobbler_profiles = $scope.cobbler_profiles;
		conf.cobbler_distro_name = $scope.cobbler_distro_name;
		conf.cobbler_interface = $scope.cobbler_interface;
		conf.cobbler_ipaddress = $scope.cobbler_ipaddress;
		conf.cobbler_netmask = $scope.cobbler_netmask;
		conf.cobbler_server = $scope.cobbler_server;
		conf.cobbler_next_server = $scope.cobbler_next_server;
		conf.cobbler_subnet = $scope.cobbler_subnet;
		conf.cobbler_option_router = $scope.cobbler_option_router;
		conf.cobbler_DNS = $scope.cobbler_DNS;
		conf.cobbler_hostname = $scope.cobbler_hostname;
		conf.cobbler_web_username = $scope.cobbler_web_username;
		conf.cobbler_web_password = $scope.cobbler_web_password;
		conf.redhat_username = $scope.redhat_username;
		conf.redhat_password = $scope.redhat_password;
		conf.redhat_pool = $scope.redhat_pool;
		conf.http_proxy_ip = $scope.http_proxy_ip;
		conf.https_proxy_ip = $scope.https_proxy_ip;
		conf.https_port = $scope.https_port;
		conf.cobbler_power_type = $scope.cobbler_power_type;
		conf.FI_Cluster_IP = $scope.FI_Cluster_IP;
		conf.FI_Cluster_Username = $scope.FI_Cluster_Username;
		conf.FI_Cluster_Password = $scope.FI_Cluster_Password;
		conf.FI_Server_Ports = $scope.FI_Server_Ports;
		conf.FI_Uplink_Ports = $scope.FI_Uplink_Ports;
		conf.FI_Slot_Id = $scope.FI_Slot_Id;
		conf.FI_Slot_1_ports = $scope.FI_Slot_1_ports;
		conf.FI_UUID_pool_name = $scope.FI_UUID_pool_name;
		conf.FI_UUID_pool_start = $scope.FI_UUID_pool_start;
		conf.FI_UUID_pool_end = $scope.FI_UUID_pool_end;
		conf.FI_MAC_pool_name = $scope.FI_MAC_pool_name;
		conf.FI_MAC_pool_start = $scope.FI_MAC_pool_start;
		conf.FI_MAC_pool_end = $scope.FI_MAC_pool_end;
		conf.FI_vnic_1_name = $scope.FI_vnic_1_name;
		conf.FI_vnic_1_vlan_range = $scope.FI_vnic_1_vlan_range;
		conf.FI_vnic_2_name = $scope.FI_vnic_2_name;
		conf.FI_vnic_2_vlan_range = $scope.FI_vnic_2_vlan_range;
		conf.FI_vnic_3_name = $scope.FI_vnic_3_name;
		conf.FI_vnic_3_vlan_range = $scope.FI_vnic_3_vlan_range;
		conf.FI_Service_profile_name = $scope.FI_Service_profile_name;
		conf.Switch_available_switches = $scope.Switch_available_switches;
		conf.Switch_1_Hostname = $scope.Switch_1_Hostname;
		conf.Switch_1_Ip_address = $scope.Switch_1_Ip_address;
		conf.Switch_1_username = $scope.Switch_1_username;
		conf.Switch_1_password = $scope.Switch_1_password;
		conf.Switch_1_vlan = $scope.Switch_1_vlan;
		conf.Switch_1_trunk_interfaces = $scope.Switch_1_trunk_interfaces;
		conf.Switch_1_VRF = $scope.Switch_1_VRF;
		conf.Switch_1_Mgmt_interface = $scope.Switch_1_Mgmt_interface;
		conf.Packstack_compute_hosts = $scope.Packstack_compute_hosts;
		conf.Packstack_network_hosts = $scope.Packstack_network_hosts;
		conf.Packstack_admin_pw = $scope.Packstack_admin_pw;
		conf.Packstack_enable_openswitch = $scope.Packstack_enable_openswitch;
		conf.Packstack_enable_cisconexus = $scope.Packstack_enable_cisconexus;
		conf.Packstack_vlan_mapping_ranges = $scope.Packstack_vlan_mapping_ranges;
		
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
