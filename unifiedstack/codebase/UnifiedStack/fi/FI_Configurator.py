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


from FI_Config_Parser import FIConfig
from FI_Port_setup import FIPortConfigurator
from FI_Pool_Setup import FIPoolConfigurator
from FI_Service_Profile_Setup import FIServiceProfileConfigurator
from FI_Service_Profile_Clone import FICloneConfigurator
from  FI_SP_Binding import FIBindingConfigurator 

class FIConfigurator:
    
    def configure_fi_components(self):    
        # Configuring Server and Uplink ports
        port_config = FIPortConfigurator()
       
        server_ports = FIConfig.get_server_ports()
        for server_port in server_ports:
            port_config.configure_server_port(str(server_port), 'sw-A', str(1))
        
        uplink_ports = FIConfig.get_uplink_ports()
        print uplink_ports
        for uplink_port in uplink_ports:
            port_config.configure_uplink_port(str(uplink_port), 'sw-A', str(1))
        # Configuring uuid and mac pools
        pool_config = FIPoolConfigurator()
        pool_config.configure_uuid_pool( FIConfig.get_uuid_pool_name(),
                                         FIConfig.get_uuid_pool_start(),
                                         FIConfig.get_uuid_pool_end())
        
        pool_config.configure_mac_pool( FIConfig.get_mac_pool_name(),
                                        FIConfig.get_mac_pool_start(),
                                        FIConfig.get_mac_pool_end())
       
        # Configuring service profiles
        sp_config = FIServiceProfileConfigurator()
        vnic_names = FIConfig.get_vnic_names()
        print vnic_names
        for vnic_id in range(1,len(vnic_names)+1):
            sp_config.add_vlan(vnic_id, vnic_names[vnic_id-1])
            vlan_ids = FIConfig.get_vlans(vnic_id)
            for vlan_id in vlan_ids:
                sp_config.associate_vlan_vnic("vlan-"+str(vlan_id), FIConfig.get_uuid_pool_name(),
                                              FIConfig.get_mac_pool_name(), vnic_names[vnic_id-1],
                                              FIConfig.get_service_profile_name(), "A")
    	clone_config = FICloneConfigurator()
	for i in range(1, 9):
       	    clone_config.clone_profile(FIConfig.get_service_profile_name() + str(i), FIConfig.get_service_profile_name())

	bindconfig = FIBindingConfigurator()
	for i in range(1, 9):
	    p_service_profile = FIConfig.get_service_profile_name() + str(i)
            p_bladeDn = "sys/rack-unit-" + str(i)
            bindconfig.configure_bindings(
                service_profile=p_service_profile,
                bladeDn=p_bladeDn)
        print "Completed"
if __name__ == '__main__':
    ficonfig = FIConfigurator()
    ficonfig.configure_fi_components()
    
