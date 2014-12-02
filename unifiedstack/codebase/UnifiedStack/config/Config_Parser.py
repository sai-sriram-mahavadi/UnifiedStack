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

# FI_Config_Parser.py:
# Parser to parse config file.
# Provides any additional config details as necessary.

import ConfigParser
import os
import inspect

class SystemNode:
    
    def __init__(self):
       
        self.purpose = ""
        self.hostname = ""
        self.mac_address = ""
        self.ip_address = ""
        self.interface = ""
        self.profile_name = ""
        self.port = ""
        self.proxy = ""
	self.power_type = "ipmilan"
        self.power_user = ""
	self.power_password = ""
	self.power_address = ""
        
    def __str__(self):
        str_node = ""
        str_node += "Purpose:       " + self.purpose + "\r\n"
        str_node += "Hostname:      " + self.hostname + "\r\n"
        str_node += "Mac address:   " + self.mac_address + "\r\n"
        str_node += "IP address:    " + self.ip_address + "\r\n"
        str_node += "Interface:     " + self.interface + "\r\n"
        str_node += "Profile Name:  " + self.profile_name + "\r\n"
        str_node += "Port:          " + self.port + "\r\n"  
	str_node += "Power Type:    " + self.power_type + "\r\n"
        return str_node

    
class Profile:
    
    def __init__(self):
        self.profile_name = ""
        self.distro_name = ""
        
    def __str__(self):
        str_node = ""
        str_node += "Profile Name:  " + self.profile_name + "\r\n"
        str_node += "Distro Name:   " + self.distro_name + "\r\n"
        return str_node


class Config:
    
    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../data_static/unified_stack.cfg')
    
    @staticmethod
    def get_field(section, field):
        return Config.config.get(section, field, 0)
    @staticmethod
    def get_general_field(field):
	return Config.get_field("Default", field)
    @staticmethod
    def get_cobbler_field(field):
        return Config.get_field("Cobbler-Configuration", field)
    
    @staticmethod
    def get_fi_field(field):
        return Config.get_field("FI-Configuration", field)
    
    @staticmethod
    def get_switch_field(field):
        return Config.get_field("Switch-Configuration", field)
    
    @staticmethod
    def get_cimc_field(field):
        return Config.get_field("CIMC-Configuration", field)
    
    @staticmethod
    def get_systems_data():
        sys_nodes = []
        str_nodes = Config.get_field("Cobbler-Configuration", "compute-hosts")
        str_compute_nodes = str_nodes.split(",")
        for str_compute_node in str_compute_nodes:
            sys_node = SystemNode()
            sys_node.purpose = "compute"
            str_compute_node = str_compute_node.strip()
            sys_node.hostname = str_compute_node.split("(")[0]
            other_fields_str = str_compute_node.split("(")[1][:-1]
            other_fields = other_fields_str.split(";")
            sys_node.ip_address = other_fields[0]
            sys_node.mac_address = other_fields[1]
            sys_node.port = other_fields[2]
            sys_node.interface = other_fields[3]
            sys_node.profile_name = other_fields[4]
	    #sys_node.power_user = other_fields[5]
	    #sys_node.power_password = other_fields[6]
	    #sys_node.power_address = other_fields[7]
	    #sys_node.power_type = Config.get_cobbler_field("power_type")
	    #sys_node.power_proxy = Config.get_cobbler_field("http_proxy_ip")
            sys_nodes.append(sys_node)

        str_nodes = Config.get_field("Cobbler-Configuration", "network-hosts")
        str_network_nodes = str_nodes.split(",")
        for str_network_node in str_network_nodes:
            sys_node = SystemNode()
            sys_node.purpose = "network"
            str_network_node = str_network_node.strip()
            sys_node.hostname = str_network_node.split("(")[0].strip()
            other_fields_str = str_network_node.split("(")[1][:-1]
            other_fields = other_fields_str.split(";")
            sys_node.ip_address = other_fields[0]
            sys_node.mac_address = other_fields[1]
            sys_node.port = other_fields[2]
            sys_node.interface = other_fields[3]
            sys_node.profile_name = other_fields[4]
	    #sys_node.power_user = other_fields[5]
            #sys_node.power_password = other_fields[6]
            #sys_node.power_address = other_fields[7]
            #sys_node.power_type = Config.get_cobbler_field("power_type")
            #sys_node.power_proxy = Config.get_cobbler_field("http_proxy_ip")
            sys_nodes.append(sys_node)
        return sys_nodes

    @staticmethod
    def get_profiles_data():
        profile_nodes = []
        str_profiles = Config.get_field("Cobbler-Configuration", "profiles")
        str_profile_nodes = str_profiles.split(",")
        for str_profile_node in str_profile_nodes:
            profile_node = Profile()
            str_profile_node = str_profile_node.strip()
            profile_node.profile_name = str_profile_node.split("(")[0].strip()
            profile_node.distro_name = str_profile_node.split("(")[1][:-1].strip()
            profile_nodes.append(profile_node)
        return profile_nodes    
    
    @staticmethod
    def get_cobbler_field(field):
        return Config.get_field("Cobbler-Configuration", field)
   
    @staticmethod
    def get_packstack_field(field):
        return Config.get_field("Packstack-Configuration", field)
    
if __name__=="__main__":
    print Config.get_cobbler_field("cobbler_ipaddress")

    print Config.get_packstack_field("keystone-admin-pw")
    for node in Config.get_systems_data():
        print node
    for node in Config.get_profiles_data():
        print node
    #node = SystemNode()

