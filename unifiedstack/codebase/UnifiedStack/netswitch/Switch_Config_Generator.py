import sys
import os

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)
from configurator import fetch_db
from UnifiedStack.config import Config_Parser

# Helper classes to parse Switch Config Data
class VlanConfig:
    def __init__(self):
        self.vlan_label = ""
        self.ip_address = ""
        self.subnet_address = ""

    def __str__(self):
        str_output =  "Vlan Label: " + self.vlan_label + "\n"
        str_output += "IP Address: " + self.ip_address + "\n"
        str_output +=  "Subnet:     " + self.subnet_address
        return str_output

    
class InterfaceConfig:
    def __init__(self):
        self.interface = ""
        self.desc = ""
        self.vlan = ""

    def __str__(self):
        str_output =  "Interface: " + self.interface + "\n"
        str_output += "desc: " + self.desc + "\n"
        str_output += "vlan: " + self.vlan + "\n"
        return str_output


class SwitchExtractor:
    @staticmethod
    def fetch_all_vlan_config(vlan_list):
        vlan_config_arr = []
        for vlan in vlan_list:
	    vlan_fields=[vlan.id,vlan.ip,vlan.netmask]
            vlan_config_arr.append(vlan_fields)
        return vlan_config_arr

    @staticmethod
    def fetch_interface_config(switch_config_section, interface_type):
        int_config_arr = []
        str_int = Config.get_field(switch_config_section, interface_type) 
        str_int_arr = str_int.split(",")
        for str_int in str_int_arr:
            int_config = InterfaceConfig()
            str_int_fields = str_int.split("(")
            int_config.interface = str_int_fields[0].strip()
            other_fields_str = "" if (len(str_int_fields)==1) else str_int_fields[1][:-1].strip()
            other_fields = other_fields_str.split(";")
            int_config.desc = "" if(len(other_fields)<=0) else other_fields[0]
            int_config.vlan = "" if(len(other_fields)<=1) else other_fields[1]
            int_config_arr.append(int_config)
        return int_config_arr

    
class SwitchConfigGenerator:

    def get_general_configuration(self,device):
	Config = fetch_db.Switch(device)
        general_config_lines =  "conf t" + "\n" + "ip routing" + "\n"
        general_config_lines += "hostname " + Config.get("hostname") + "\n"
        general_config_lines += "username " + Config.get("username") + \
                                " privilege 15 password 0 " + \
                                Config.get( "password") + "\n"
        return general_config_lines

    def get_vlan_configuration(self,device):
	Config = fetch_db.Switch(device)	
        vlan_config_lines = ""
	vlan_list=Config.get("vlans")
        vlan_config_arr = SwitchExtractor.fetch_all_vlan_config(vlan_list)
        for vlan_config in vlan_config_arr:
            vlan_config_lines += "interface Vlan" + vlan_config[0] + "\n"
            vlan_config_lines += "ip address " + vlan_config[1] +\
                                 " " + vlan_config[2] + "\n"
        return vlan_config_lines

    def get_access_interface_configuration(self, device):
	Config = fetch_db.Switch(device)
	interface_list=Config.get("interfaces")
        access_config_lines = ""
        for interface in interface_list:
	    if interface.type=="access":
            	access_config_lines += "interface " + interface.name + "\n"
                if not interface.description == "":
                    access_config_lines += "description " + interface.description + "\n"
                if not interface.vlan == "":
                    access_config_lines += "switchport access vlan " + interface.vlan + "\n"
                access_config_lines += "switchport trunk encapsulation dot1q" + "\n"
                access_config_lines += "switchport mode access" + "\n"
        return access_config_lines
    
    def get_trunk_interface_configuration(self, device):
	Config = fetch_db.Switch(device)
	interface_list=Config.get("interfaces")
        trunk_config_lines = ""
        for interface in interface_list:
	    if interface.type=="trunk":
                trunk_config_lines += "interface " + interface.name + "\n"
                if not interface.description == "":
                    trunk_config_lines += "description " + interface.description + "\n"
		if not interface.vlan == "":
		    trunk_config_lines += "switchport trunk allowed vlan " + interface.vlan + "\n"
                trunk_config_lines += "switchport trunk encapsulation dot1q" + "\n"
                trunk_config_lines += "switchport mode trunk" + "\n"
        return trunk_config_lines

    def get_portchannel_interface_configuration(self, device):
        portchannel_config_lines = ""
	Config = fetch_db.Switch(device)
        port_channel_list=Config.get("port-channels")
        for port_channel in port_channel_list :
	    interface_list=port_channel.interfaces.strip().split(",")
	    for interface in interface_list:
                portchannel_config_lines += "interface " + interface + "\n"
                portchannel_config_lines += "channel-group " + port_channel.number + "  mode active" + "\n"
        return portchannel_config_lines

    def get_interface_configuration(self,device):
        interface_config_lines = "" 
        interface_config_lines += self.get_access_interface_configuration(device)    
        interface_config_lines += self.get_trunk_interface_configuration(device)
        interface_config_lines += self.get_portchannel_interface_configuration(device)
        return interface_config_lines

    def get_console_configuration(self):
        console_config_lines = "exit" + "\n"
        console_config_lines += "ip classless" + "\n" 
        console_config_lines += "ip http server" + "\n"
        console_config_lines += "ip http secure-server" + "\n"
        console_config_lines += "ip sla enable reaction-alerts" + "\n"
        console_config_lines += "line con 0" + "\n"
        console_config_lines += "exit" + "\n"
        console_config_lines += "line vty 0 4" + "\n"
        console_config_lines += "login local" + "\n"
        console_config_lines += "line vty 5 15" + "\n"
        console_config_lines += "login local" + "\n"
        return console_config_lines  
   
    def generate_config_file(self, device):
        config_file_name = str(device.id)  + "_commands.cmds"
        with open(config_file_name , 'w') as config_file:
   	    config_file.write( self.get_general_configuration(device))   
            config_file.write( self.get_vlan_configuration(device))
	    config_file.write( self.get_interface_configuration(device))
	    config_file.write( self.get_console_configuration())
	    
if __name__=="__main__":
    sw_gen = SwitchConfigGenerator()
    
