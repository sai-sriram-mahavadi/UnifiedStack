#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Common interface to access/configure fi from outside

from configurator import fetch_db
from FI_Config_Parser import FIConfig
from FI_Port_setup import FIPortConfigurator
from FI_Pool_Setup import FIPoolConfigurator
from FI_Service_Profile_Setup import FIServiceProfileConfigurator
from FI_Service_Profile_Clone import FICloneConfigurator
from FI_SP_Binding import FIBindingConfigurator 
from FI_BootPolicy import FIBootPolicy 

class FIConfigurator():
 
    def configure_fi_components(self):    
        # Configuring Server and Uplink ports
        port_config = FIPortConfigurator()
        server_ports = fetch_db.FI().get('fi-server-ports').strip().split(",")	
        for server_port in server_ports:
            port_config.configure_server_port(str(server_port), 'sw-A', str(1))
        
        uplink_ports = fetch_db.FI().get('fi-uplink-ports').strip().split(",")
        print uplink_ports
        for uplink_port in uplink_ports:
            port_config.configure_uplink_port(str(uplink_port), 'sw-A', str(1))
        # Configuring uuid and mac pools
        uuid_pool_list=fetch_db.FI().get('fi-uuid-pools')
        pool_config = FIPoolConfigurator()
        for uuid_pool in uuid_pool_list:
            pool_config.configure_uuid_pool( uuid_pool.name,
                                         uuid_pool.start,
                                         uuid_pool.end)
        mac_pool_list=fetch_db.FI().get('fi-mac-pools')
        for mac_pool in mac_pool_list:
            pool_config.configure_mac_pool( mac_pool.name,
                                        mac_pool.start,
                                        mac_pool.end)
        ip_pool_list=fetch_db.FI().get('fi-ip-pools')
        for ip_pool in ip_pool_list: 
            pool_config.configure_ip_pool( ip_pool.name,
                                        ip_pool.start,
                                        ip_pool.end,
                                        ip_pool.gateway,
                                        ip_pool.subnet)
	# Configuring service profiles
        sp_config = FIServiceProfileConfigurator()
        
	vnic_names = FIConfig.get_vnic_names()
        """
        for vnic_id in range(1,len(vnic_names)+1):
            sp_config.add_vlan(vnic_id, vnic_names[vnic_id-1])
            vlan_ids = FIConfig.get_vlans(vnic_id)
            for vlan_id in vlan_ids:
                sp_config.associate_vlan_vnic("vlan-"+str(vlan_id), FIConfig.get_uuid_pool_name(),
                                              FIConfig.get_mac_pool_name(), vnic_names[vnic_id-1],
                                              FIConfig.get_service_profile_name(), "A")
	"""
	boot_policy = FIBootPolicy()
        boot_policy_name = fetch_db.FI().get('fi-boot-policy-name')
        boot_policy_vnic = fetch_db.FI().get('fi-boot-vnic')
        boot_policy.configure_boot_policy(boot_policy_name, boot_policy_vnic)
        vnic_list=fetch_db.FI().get('fi-vnics')
        
        for vnic_id in range(1,len(vnic_list)+1):
            for vlan_id in range(int(vnic_list[vnic_id-1].start),int(vnic_list[vnic_id-1].end) + 1):
                sp_config.add_vlan(vlan_id, 'vlan-' + str(vlan_id))
            for vlan_id in range(int(vnic_list[vnic_id-1].start),int(vnic_list[vnic_id-1].end) + 1):
                sp_config.associate_vlan_vnic("vlan-"+str(vlan_id), uuid_pool_list[0].name,
                                              mac_pool_list[0].name, vnic_list[vnic_id-1].name,
                                              fetch_db.FI().get('fi-service-profile-name'),"A",
                                              fetch_db.FI().get('fi-boot-policy-name'),ip_pool_list[0].name)
                               
	clone_config = FICloneConfigurator()
	for i in range(1, 9):
       	    clone_config.clone_profile(fetch_db.FI().get('fi-service-profile-name') + str(i), fetch_db.FI().get('fi-service-profile-name'))

	bindconfig = FIBindingConfigurator()
	for i in range(1, 9):
	    p_service_profile = fetch_db.FI().get('fi-service-profile-name') + str(i)
            p_bladeDn = "sys/rack-unit-" + str(i)
            bindconfig.configure_bindings(
                service_profile=p_service_profile,
                bladeDn=p_bladeDn)
        print "Completed"
	"""
        boot_policy = FIBootPolicy()
        boot_policy_name = fetch_db.FI().get('fi-boot-policy-name')
        boot_policy_vnic = fetch_db.FI().get('fi-boot-vnic')
        boot_policy.configure_boot_policy(boot_policy_name, boot_policy_vnic)
        """

if __name__ == '__main__':
    ficonfig = FIConfigurator()
    ficonfig.configure_fi_components()
    
