
import sys
import os

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config import Config_Parser
# Alias for simple usage of Config parser
Config = Config_Parser.Config

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
    def fetch_all_vlan_config(switch_config_section):
        vlan_config_arr = []
        str_vlan = Config.get_field(switch_config_section, "vlans")
        str_vlan_config_arr = str_vlan.split(",")
        for str_vlan_config in str_vlan_config_arr:
            vlan_config = VlanConfig()
            str_vlan_config = str_vlan_config.strip()
            vlan_config.vlan_label = str_vlan_config.split("(")[0].strip()
            other_fields_str = str_vlan_config.split("(")[1][:-1].strip()
            other_fields = other_fields_str.split(";")
            vlan_config.ip_address = other_fields[0]
            vlan_config.subnet_address = other_fields[1]
            vlan_config_arr.append(vlan_config)
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

    def get_3750_general_configuration(self):
        general_config_lines =  "conf t" + "\n" + "ip routing" + "\n"
        general_config_lines += "hostname " + Config.get_field("Switch-3750", "hostname") + "\n"
        general_config_lines += "username " + Config.get_field("Switch-3750", "username") + \
                                " privilege 15 password 0 " + \
                                Config.get_field("Switch-3750", "password") + "\n"
        return general_config_lines

    def get_3750_vlan_configuration(self):
        vlan_config_lines = ""
        vlan_config_arr = SwitchExtractor.fetch_all_vlan_config("Switch-3750")
        for vlan_config in vlan_config_arr:
            vlan_config_lines += "interface Vlan" + vlan_config.vlan_label + "\n"
            vlan_config_lines += "ip address " + vlan_config.ip_address +\
                                 " " + vlan_config.subnet_address + "\n"
        return vlan_config_lines

    def get_3750_access_interface_configuration(self, int_config_arr):
        access_config_lines = ""
        for int_config in int_config_arr:
            access_config_lines += "interface " + int_config.interface + "\n"
            if not int_config.desc == "":
                access_config_lines += "description " + int_config.desc + "\n"
            if not int_config.vlan == "":
                access_config_lines += "switchport access vlan " + int_config.vlan + "\n"
            access_config_lines += "switchport trunk encapsulation dot1q" + "\n"
            access_config_lines += "switchport mode access" + "\n"
        return access_config_lines
    
    def get_3750_trunk_interface_configuration(self, int_config_arr):
        trunk_config_lines = ""
        for int_config in int_config_arr:
            trunk_config_lines += "interface " + int_config.interface + "\n"
            if not int_config.desc == "":
                trunk_config_lines += "description " + int_config.desc + "\n"
            trunk_config_lines += "switchport trunk encapsulation dot1q" + "\n"
            trunk_config_lines += "switchport mode trunk" + "\n"
        return trunk_config_lines

    def get_3750_portchannel_interface_configuration(self, int_config_arr):
        portchannel_config_lines = ""
        for int_config in int_config_arr:
            portchannel_config_lines += "interface " + int_config.interface + "\n"
            if not int_config.desc == "":
                portchannel_config_lines += "description " + int_config.desc + "\n"
            portchannel_config_lines += "switchport trunk encapsulation dot1q" + "\n"
            portchannel_config_lines += "switchport mode trunk" + "\n"
            portchannel_config_lines += "channel-group 1 mode active" + "\n"
        return portchannel_config_lines

    def get_3750_interface_configuration(self):
        interface_config_lines = ""
        int_config_arr = SwitchExtractor.fetch_interface_config("Switch-3750", "access-interfaces")
        interface_config_lines += self.get_3750_access_interface_configuration(int_config_arr)
        int_config_arr = SwitchExtractor.fetch_interface_config("Switch-3750", "trunk-interfaces")
        interface_config_lines += self.get_3750_trunk_interface_configuration(int_config_arr)
        int_config_arr = SwitchExtractor.fetch_interface_config("Switch-3750", "portchannel-1-interfaces")
        interface_config_lines += self.get_3750_portchannel_interface_configuration(int_config_arr)
        return interface_config_lines

    def get_3750_console_configuration(self):
        console_config_lines = "exit" + "\n"
        console_config_lines += "ip classless" + "\n"
        console_config_lines += "ip route 0.0.0.0 0.0.0.0 " + \
                                Config.get_field("Switch-3750", "default-route") + "\n"
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
    
    def get_9k_general_configuration(self):
        general_config_lines =  "conf t" + "\n"
        general_config_lines += "hostname " + Config.get_field("Switch-9k", "hostname") + "\n"
        general_config_lines += "username " + Config.get_field("Switch-9k", "username") + \
                                Config.get_field("Switch-9k", "password") + "\n"
        general_config_lines += "copp profile strict " + "\n"
        general_config_lines += "vrf context management " + "\n"
        return general_config_lines

    def get_9k_vlan_configuration(self):
        vlan_config_lines = ""
        vlan_str = Config.get_field("Switch-9k", "vlan")
        vlan_config_arr = vlan_str.split(', ')
        for vlan_config in vlan_config_arr:
            vlan_config_lines += "Vlan" + vlan_config.strip() + "\n"
        return vlan_config_lines

    def get_9k_trunk_interface_configuration(self):
        trunk_config_lines = ""
        int_str = Config.get_field("Switch-9k", "trunk-interfaces")
        int_config_arr = int_str.split(', ')
        for int_config in int_config_arr:
            trunk_config_lines += "interface " + int_config + "\n"
            trunk_config_lines += "switchport mode trunk" + "\n"
        return trunk_config_lines
    
    def get_9k_management_interface_configuration(self, int_config_arr):
        management_config_lines = ""
        mgmt_str = Config.get_field("Switch-9k", "managment-interface")
        mgmt_label = mgmt_str.split("(")[0].strip()
        other_fields_str = mgmt_str.split("(")[1][:-1].strip()
        other_fields = other_fields_str.split(";")
        ip_address = other_fields[0]
        subnet = other_fields[1]
        management_config_lines += "interface" + mgmt_label + "\n"
        management_config_lines += "ip address " + ip_address + " " + subnet + "\n"
        return management_config_lines
    
    def generate_config_file(self, switch_config_section):
        config_file_name = switch_config_section + "_commands.cmds"
        with open(config_file_name, 'w') as config_file:
            if switch_config_section=="Switch-3750":
                # Commands Specific to sw-3750
                config_file.write( self.get_3750_general_configuration() )
                config_file.write( self.get_3750_vlan_configuration() )
                config_file.write( self.get_3750_interface_configuration() )
                config_file.write( self.get_3750_console_configuration() )
            elif switch_config_section=="Switch-9k":
                # Commands Specific to sw-9k
                config_file.write( self.get_9k_general_configuration() )
                config_file.write( self.get_9k_vlan_configuration() )
                config_file.write( self.get_9k_trunk_interface_configuration() )
                config_file.write( self.get_9k_management_interface_configuration() )
                

if __name__=="__main__":
    sw_gen = SwitchConfigGenerator()
    #sw_gen.generate_config_file("switch-3750")
    sw_gen.generate_config_file("switch-9k")
    
