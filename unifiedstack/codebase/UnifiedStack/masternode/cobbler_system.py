#!/usr/bin/python

#   Copyright 2014 Prakash Kumar
#
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

# FI_Pool_setup.py:
# Configures uuid pools and mac pools.
# Values are hardcoded for the purpose of simplicity as of now.

import cobbler.api as cobapi
from general_utils import is_basestring


class New_system():

    def __init__(self,
            name=None,
            owners=None,
            profile=None,
            status="testing",
            netboot_enabled=True,
            hostname=None,
            interface=None,
            mac_addr=None,
 	    proxy=None,
            ipaddr=None,
            virt_bridge=None,
	    kickstart="/var/lib/cobbler/kickstarts/rhe7-osp5.ks",
            power_management_type=None,
            power_management_addr=None,
            power_management_username=None,
            power_management_password=None,
            power_management_id=None):
        """Required fields are name, profile, status,edit_interface,power management type"""
        # System name
        self.name = name
        # list of owners delimited by commas
        self.owners = owners
        # name of the profile to associate
        self.profile = profile
        # It should be either--production, testing
        #acceptance or development
        self.status = status
        # Set true if netboot needs to be enabled
        self.netboot_enabled = netboot_enabled
        # hostname of the system
        self.hostname = hostname
        # Interface which will be used for PXE boot
        # by the system which is going to network boot
        self.interface = interface
        # mac address of the above interface
        self.mac_addr = mac_addr
        # ip address of this interface
        self.ipaddr = ipaddr
        # Below parameters are less used.
        self.proxy=proxy
	self.kickstart=kickstart
        self.virt_bridge = virt_bridge
        self.power_management_type = power_management_type
        self.power_management_addr = power_management_addr
        self.power_management_username = power_management_username
        self.power_management_password = power_management_password
        self.power_management_id = power_management_id

    def save_system(self):
        try:
            if not is_basestring(self.name):
                raise Exception("Name must be of string ")
            if self.owners is not None and not is_basestring(self.owners):
                raise Exception("Owners must be comma separated string ")
            if not is_basestring(self.profile):
                raise Exception("Profile must be of string ")
            if self.status is not None and not is_basestring(self.status):
                raise Exception("Status must be of string ")
            if self.hostname is not None and not is_basestring(self.hostname):
                raise Exception("Hostname must be string")
            if not isinstance(self.netboot_enabled, bool):
                raise Exception("OS version must be True or False")
            if self.interface is not None and not is_basestring(
                    self.interface):
                raise Exception("Interface must be string ")
            if self.mac_addr is not None and not is_basestring(self.mac_addr):
                raise Exception("Mac address must be string ")
            if self.ipaddr is not None and not is_basestring(self.ipaddr):
                raise Exception("Ip address must be of string ")
            if self.virt_bridge is not None and not is_basestring(
                    self.virt_bridge):
                raise Exception("Virtual bridge must be of string ")
            if self.power_management_type is not None and not is_basestring(
                    self.power_management_type):
                raise Exception(
                    "self.power_management_type must be of string ")
            if self.power_management_addr is not None and not is_basestring(
                    self.power_management_addr):
                raise Exception(
                    "self.power_management_addr must be of string ")
            if self.power_management_username is not None and not is_basestring(
                    self.power_management_username):
                raise Exception(
                    "self.power_management_username must be of string ")
            if self.power_management_password is not None and not is_basestring(
                    self.power_management_password):
                raise Exception(
                    "self.power_management_password must be of string ")
            if self.power_management_id is not None and not is_basestring(
                    self.power_management_id):
                raise Exception("self.power_management_id must be of string ")
            if self.name is None or self.profile is None or self.status is None:
                raise Exception("Name, Profile status are required")
        except Exception as e:
            print str(e)
            return False

        cobbler_api_handle = cobapi.BootAPI()
        try:
            # check whether system with this name already exists
            if not cobbler_api_handle.find_system(self.name) is None:
                raise Exception("System with this name already exist")
            cobbler_system = cobbler_api_handle.new_system()
            cobbler_system.set_name(self.name)
            cobbler_system.set_profile(self.profile)
            cobbler_system.set_status(self.status)
            if self.interface is not None:
                cobbler_system.set_interface_type('na', self.interface)
            cobbler_system.set_netboot_enabled(self.netboot_enabled)
            if self.mac_addr is not None:
                cobbler_system.set_mac_address(self.mac_addr,self.interface)
            if self.ipaddr is not None:
                cobbler_system.set_ip_address(self.ipaddr, self.interface)
            if self.owners is not None:
                cobbler_system.set_owners(self.owners)
            else:
                cobbler_system.set_owners('admin')
            if self.virt_bridge is not None:
                cobbler_system.set_virt_bridge(
                    self.virt_bridge,
                    self.interface)
            if self.hostname is not None:
                cobbler_system.set_hostname(self.hostname)
            if self.power_management_type is not None:
                cobbler_system.set_power_type(self.power_management_type)
            if self.power_management_username is not None:
                cobbler_system.set_power_user(self.power_management_username)
            if self.power_management_password is not None:
                cobbler_system.set_power_pass(self.power_management_password)
            if self.power_management_id is not None:
                cobbler_system.set_power_id(self.power_management_id)
            if self.power_management_addr is not None:
                cobbler_system.set_power_address(self.power_management_addr)
	    if self.proxy is not None:
		cobbler_system.set_proxy(self.proxy)
	    cobbler_system.set_kickstart(self.kickstart)
            cobbler_api_handle.add_system(cobbler_system)
	    
        except Exception as e:
            print str(e)
            return False
        return True


class System_operate():

    def __init__(self):
        pass

    def copy_system(self, src_system_name, new_system_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(src_system_name):
                raise("src system name  must be string")
            if not is_basestring(new_system_name):
                raise("new system name must be string")
            reference = cobbler_api_handle.find_system(src_system_name)
            if reference is None:
                raise Exception(
                    "system with name " +
                    src_system_name +
                    " does not exists")
            if not cobbler_api_handle.find_system(new_system_name) is None:
                raise Exception(
                    "system with name " +
                    new_system_name +
                    " already exist. Give Some other name for the system\
		    being created")
            cobbler_api_handle.copy_system(reference, new_system_name)
        except Exception as e:
            print str(e)
            return False
        return True

    def rename_system(self, old_system_name, new_system_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(old_system_name):
                raise("old system name must be string")
            if not is_basestring(new_system_name):
                raise("new system name must be string")
            reference = cobbler_api_handle.find_system(old_system_name)
            if reference is None:
                raise Exception(
                    "system with name " +
                    old_system_name +
                    " does not exists")
            if not cobbler_api_handle.find_system(new_system_name) is None:
                raise Exception(
                    "system with name " +
                    new_system_name +
                    " already exist. Give some other name")
            cobbler_api_handle.rename_system(reference, new_system_name)
        except Exception as e:
            print str(e)
            return False
        return True

    def delete_system(self, system_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(system_name):
                raise("name of the system to be deleted must be string")
            reference = cobbler_api_handle.find_system(system_name)
            if reference is None:
                raise Exception(
                    "system with " +
                    system_name +
                    " does not exists")
            cobbler_api_handle.remove_system(reference)
        except Exception as e:
            print str(e)
            return False
        return True

    def edit_system(
            self,
            system_name,
            owners=None,
            profile=None,
            status=None,
            netboot_enabled=None,
            hostname=None,
            interface=None,
            mac_addr=None,
            ipaddr=None,
            virt_bridge=None,
            power_management_type=None,
            power_management_addr=None,
            power_management_username=None,
            power_management_password=None,
            power_management_id=None):
        """Edit the existing System. The name is now editable"""
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(system_name):
                raise("system name must be string")
            if owners is not None and not is_basestring(owners):
                raise Exception("Owners must be comma separated string ")
            if profile is not None and not is_basestring(profile):
                raise Exception("Profile must be of string ")
            if status is not None and not is_basestring(status):
                raise Exception("Status must be of string ")
            if hostname is not None and not is_basestring(hostname):
                raise Exception("Hostname must be string")
            if netboot_enabled is not None and not isinstance(
                    netboot_enabled,
                    bool):
                raise Exception("OS version must be True or False")
            if interface is not None and not is_basestring(interface):
                raise Exception("Interface must be string ")
            if mac_addr is not None and not is_basestring(mac_addr):
                raise Exception("Mac address must be string ")
            if ipaddr is not None and not is_basestring(ipaddr):
                raise Exception("Ip address must be of string ")
            if virt_bridge is not None and not is_basestring(virt_bridge):
                raise Exception("Virtual bridge must be of string ")
            if power_management_type is not None and not is_basestring(
                    power_management_type):
                raise Exception("power_management_type must be of string ")
            if power_management_addr is not None and not is_basestring(
                    power_management_addr):
                raise Exception("power_management_addr must be of string ")
            if power_management_username is not None and not is_basestring(
                    power_management_username):
                raise Exception("power_management_username must be of string ")
            if power_management_password is not None and not is_basestring(
                    power_management_password):
                raise Exception("power_management_password must be of string ")
            if power_management_id is not None and not is_basestring(
                    power_management_id):
                raise Exception("power_management_id must be of string ")
        except Exception as e:
            print str(e)
            return False
        try:
            # check whether system with this name already exists
            reference = cobbler_api_handle.find_system(system_name)
            if reference is None:
                raise Exception(
                    "System with " +
                    system_name +
                    " does not exists")
            if profile is not None:
                reference.set_profile(profile)
            if status is not None:
                reference.set_status(status)
            if interface is not None:
                reference.set_interface_type('na', interface)
            if netboot_enabled is not None:
                reference.set_netboot_enabled(netboot_enabled)
            if mac_addr is not None:
                reference.set_mac_address(mac_addr, interface)
            if ipaddr is not None:
                reference.set_ip_address(ipaddr, interface)
            if owners is not None:
                reference.set_owners(owners)
            if virt_bridge is not None:
                reference.set_virt_bridge(virt_bridge, interface)
            if hostname is not None:
                reference.set_hostname(hostname)
            if power_management_type is not None:
                reference.set_power_type(power_management_type)
            if power_management_username is not None:
                reference.set_power_user(power_management_username)
            if power_management_password is not None:
                reference.set_power_pass(power_management_password)
            if power_management_id is not None:
                reference.set_power_id(power_management_id)
            if power_management_addr is not None:
                reference.set_power_address(power_management_addr)
     
            cobbler_api_handle.add_system(reference)
        except Exception as e:
            print str(e)
            return False
        return True
    
    def power_on(self,sys_name):
	cobbler_api_handle = cobapi.BootAPI()
        try:
            reference = cobbler_api_handle.find_system(sys_name)
            if reference is None:
                raise Exception(
                    "system with name " +
                    sysname +
                    " does not exists")
            cobbler_api_handle.power_on(reference)
	    return True
        except Exception,e: 
	    return False

    def power_off(self,sys_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            reference = cobbler_api_handle.find_system(sys_name)
            if reference is None:
                raise Exception(
                    "system with name " +
                    sysname +
                    " does not exists")
            cobbler_api_handle.power_off(reference)
            return True
        except Exception,e:
            return False

   
	    

if __name__ == "__main__":
    """
    ref=New_system("test-sys",interface="eth0",owners="admin",profile="profile4",status="develpoment")
    ref.save_system()
    """
    ref = System_operate()
    ref.edit_system(
        "system2",
        owners="admin, cobbler",
        profile="RHEL7-1",
        status="production",
        ipaddr="192.168.10.1",
        mac_addr="AD:12:12:12:12:11",
        interface='eth0')
