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

# Parser to parse config file.
# Provides any additional config details as necessary.

import ConfigParser
import os
import inspect

class FIConfig:
    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\..\config\unified_stack.cfg')

    
    @staticmethod
    def get_field(field):
        return FIConfig.config.get('FI-Configuration', field, 0)
    
    @staticmethod
    def get_cluster_ipaddress():
        return FIConfig.get_field('fi-cluster-ip-address')

    @staticmethod
    def get_cluster_username():
        return FIConfig.config.get('FI-Configuration', 'fi-cluster-username', 0)

    @staticmethod
    def get_cluster_password():
        return FIConfig.config.get('FI-Configuration', 'fi-cluster-password', 0)

    @staticmethod
    def get_server_ports():
        server_ports_str = FIConfig.get_field('fi-server-ports')
        server_ports = []
        str_ports = server_ports_str.split(',')
        for str_port in str_ports:
            port_num = int(str_port.strip())
            server_ports.append(port_num)
        return server_ports

    @staticmethod
    def get_uplink_ports():
        uplink_ports_str = FIConfig.get_field('fi-uplink-ports')
        uplink_ports = []
        str_ports = uplink_ports_str.split(',')
        for str_port in str_ports:
            port_num = int(str_port.strip())
            uplink_ports.append(port_num)
        return uplink_ports

    @staticmethod
    def get_uuid_pool_name():
        return FIConfig.get_field('fi-uuid-pool-name')

    @staticmethod
    def get_uuid_pool_start():
        return FIConfig.get_field('fi-uuid-pool-start')

    @staticmethod
    def get_uuid_pool_end():
        return FIConfig.get_field('fi-uuid-pool-end')

    @staticmethod
    def get_mac_pool_name():
        return FIConfig.get_field('fi-mac-pool-name')

    @staticmethod
    def get_mac_pool_start():
        return FIConfig.get_field('fi-mac-pool-start')

    @staticmethod
    def get_mac_pool_end():
        return FIConfig.get_field('fi-mac-pool-end')

    @staticmethod
    def get_vnic_names():
        vnic_names = []
        vnic_names.append(FIConfig.get_field('fi-vnic-1-name'))
        vnic_names.append(FIConfig.get_field('fi-vnic-2-name'))
        vnic_names.append(FIConfig.get_field('fi-vnic-3-name'))
        return vnic_names

    @staticmethod
    def get_vlans(vnic_index):
        vlan_str = FIConfig.get_field('fi-vnic-'+str(vnic_index)+'-vlan-range')
        vlan_ids = []
        str_vlan_ids = vlan_str.split('-')
        vlan_id_start = int(str_vlan_ids[0].strip())
        vlan_id_end = int(str_vlan_ids[1].strip()) if (len(str_vlan_ids) == 2) else vlan_id_start
        for vlan_id in range(vlan_id_start, vlan_id_end+1):
            vlan_ids.append(vlan_id)
        return vlan_ids               

    @staticmethod
    def get_service_profile_name():
        return FIConfig.get_field('fi-service-profile-name')
    
if __name__ == '__main__':
    
    print FIConfig.get_cluster_ipaddress()
    print FIConfig.get_cluster_username()
    print FIConfig.get_cluster_password()
    print FIConfig.get_server_ports()
    print FIConfig.get_uplink_ports()
    print FIConfig.get_vnic_names()
    print FIConfig.get_vlans(1)
    print FIConfig.get_vlans(2)
    print FIConfig.get_vlans(3)
    
    
