import os
import sys
root_path = os.path.abspath(r"..")
sys.path.append(root_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unifiedstack.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
from configurator.models import Device, DeviceTypeSetting, DeviceSetting
import django.core.exceptions
class System:
    def __init__(self):
        self.purpose = ""
        self.hostname = ""
        self.mac_address = ""
        self.ip_address = ""
        self.interface = ""
        self.profile_name = ""
        self.port = ""
        self.proxy = ""
        self.power_type = ""
        self.power_user = ""
        self.power_password = ""
        self.power_address = ""

class Profile:
    def __init__(self):
        self.profile_name = ""
        self.distro_name = ""

class Cobbler:
    def __init__(self):
	self.device = Device.objects.get(dtype=DeviceTypeSetting.COBBLER_TYPE)	

    def get_compute_hosts_ip(self):
        ip_list=[]
        setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='compute-host')
        lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
        for host in lst:
            ip_list.append(host.value.strip().split(";")[1].strip())
        return ip_list

    def get_network_hosts_ip(self):
        ip_list=[]
        setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='network-host')
        lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
        for host in lst:
            ip_list.append(host.value.strip().split(";")[1].strip())
        return ip_list

    def get(self,attribute):
	try:
	    attribute=attribute.strip()
	    if attribute=='systems':
	        system_list=[]
		for purpose in ['compute','network']:
                    setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith= purpose + '-host')
                    lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                    for system in lst:
			attributes=system.value.strip().split(";")
                        systemObj=System()
		        systemObj.purpose = "Compute"
                        systemObj.hostname = attributes[0].strip()
       		        systemObj.mac_address = attributes[2].strip()
        	        systemObj.ip_address = attributes[1].strip()
        	        systemObj.interface = attributes[4].strip()
        	        systemObj.profile_name = attributes[5].strip()
                        system_list.append(systemObj)
		return system_list
	    elif attribute=='profiles':
		prof_list=[]
		setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='profile(')
		lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)	      
		for prof in lst:
		    profileObj=Profile()
		    profileObj.profile_name=prof.value.strip().split(";")[0].strip()
		    profileObj.distro_name=DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label='distro')
		    prof_list.append(profileObj)
		return prof_list
	    elif 'http' in attribute:
	        setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='proxy')
		if attribute.strip()=='http_proxy_ip':
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[0].strip()
		elif attribute.strip()=='https_proxy_ip':
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[1].strip()
		else:
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[2].strip()
	    elif 'redhat' in attribute:
	        setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='redhat')
		if attribute.strip()=='redhat-username':
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[0].strip()
		elif attribute.strip()=='redhat-password':
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[1].strip()
		else: 
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[2].strip()
	    elif 'cobbler-web' in attribute:
		setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='cobbler-web')
		if attribute.strip()=='cobbler-web-username':
		    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[0].strip()
		else:
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[1].strip()
	    else:
	        setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label=attribute)
	        return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value
	except django.core.exceptions.ObjectDoesNotExist:
	    print "*" * 10 + "Atrribute Does not exists" + "*" * 10


class Foreman:
     def __init__(self):
        self.device = Device.objects.get(dtype=DeviceTypeSetting.FOREMAN_TYPE)

     def get_compute_hosts_ip(self):
	ip_list=[]
	setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='compute-host')
	lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
	for host in lst:
	    ip_list.append(host.value.strip().split(";")[1].strip())
        return ip_list

     def get_network_hosts_ip(self):
	ip_list=[]
        setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='network-host')
        lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
        for host in lst:
            ip_list.append(host.value.strip().split(";")[1].strip())
        return ip_list

     def get(self,attribute):
        try:
	    if attribute.strip()=='systems':
                system_list=[]
                for purpose in ['compute','network']:
                    setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith= purpose + '-host')
                    lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                    for system in lst:
                        attributes=system.value.strip().split(";")
                        systemObj=System()
                        systemObj.hostname = attributes[0].strip() + "-" + purpose 
                        systemObj.mac_address = attributes[2].strip()
                        systemObj.ip_address = attributes[1].strip()
                        system_list.append(systemObj)
                return system_list
	    elif 'redhat' in attribute.strip():
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='redhat')
                if attribute.strip()=='redhat-username':
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[0].strip()
                elif attribute.strip()=='redhat-password':
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[1].strip()
                else:
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[2].strip()

	    elif 'http' in attribute.strip():
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='proxy')
                if attribute.strip()=='http_proxy_ip':
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[0].strip()
                elif attribute.strip()=='https_proxy_ip':
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[1].strip()
                else:
                    return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value.strip().split(";")[2].strip()
	    else:
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label=attribute.strip())
                return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value

        except django.core.exceptions.ObjectDoesNotExist:
            print "*" * 10 + "Atrribute Does not exists" + "*" * 10

class General:
    def __init__(self):
        self.device = Device.objects.get(dtype=DeviceTypeSetting.GENERAL_TYPE)	
    def get(self,attribute):
        try: 
	    setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label=attribute.strip())
            return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value
	except django.core.exceptions.ObjectDoesNotExist:
            print "*" * 10 + "Atrribute Does not exists" + "*" * 10

class Packstack:
    def __init__(self):
        self.device = Device.objects.get(dtype=DeviceTypeSetting.PACKSTACK_TYPE)
    def get(self,attribute):
        try:
            setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label=attribute.strip())
            return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value
        except django.core.exceptions.ObjectDoesNotExist:
            print "*" * 10 + "Atrribute Does not exists" + "*" * 10

class Vlan:
    def __init__(self):
	self.id=''
	self.ip=''
	self.netmask=''

class Interface:
    def __init__(self):
	self.name=''
	self.type=''
	self.description=''
	self.vlan=''

class Port_Channel:
    def __init__(self):	
	self.number=''
	self.interfaces=''

class Switch:
    def __init__(self,device):
	self.device=device

    def get(self,attribute):
	try:
	    if attribute.strip()=='vlans' :
		vlan_list=[]
		setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='vlan(id')
		lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
		for vlan in lst:
		    vlanObj=Vlan()			
		    attributes=vlan.value.strip().split(";")	    	
		    vlanObj.id=attributes[0].strip()
		    vlanObj.ip=attributes[1].strip()
		    vlanObj.netmask=attributes[2].strip()
		    vlan_list.append(vlanObj)
	        return vlan_list
	    elif attribute.strip()=='interfaces':
		interfaces_list=[]
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='interface(name')
                lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                for interface in lst:
                    interfaceObj=Interface()
                    attributes=interface.value.strip().split(";")
                    interfaceObj.name=attributes[0].strip()
                    interfaceObj.type=attributes[1].strip()
		    interfaceObj.description=attributes[2].strip()
                    interfaceObj.vlan=attributes[3].strip()
                    vlan_list.append(interfaceObj)
                return interface_list
	    elif attribute.strip()=='port-channels':
		port_channel_list=[]
		setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='port-channel')
		lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
		for port_channel in lst:
		    portchannelObj=Port_Channel()
		    attributes=interface.value.strip().split(";")
		    portchannelObj.number=attributes[0].strip()
		    portchannelObj.interfaces=attributes[1].strip()
		    port_channel_list.append(portchannelObj)
	    else:
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label=attribute.strip())
                return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value
    
	except django.core.exceptions.ObjectDoesNotExist:
            print "*" * 10 + "Atrribute Does not exists" + "*" * 10	
	    	

class Slot:
    def __init__(self):
	self.id=''
	self.ports=''
class Uuid_pool:
    def __init__(self):
	self.name=''
	self.start=''
	self.end=''
class Mac_pool:
    def __init__(self):
	self.name=''
	self.start=''
	self.end=''
class Vnic:
    def __init__(self):
	self.name=''
        self.start=''
	self.end=''
class Ip_pool:
    def __init__(self):
	self.name=''
	self.start=''
	self.end=''
	self.gateway=''
	self.subnet=''
    
class FI:
    def __init__(self):
        self.device=Device.objects.get(dtype=DeviceTypeSetting.FI_TYPE)

    def get(self,attribute):
        try:
            if attribute.strip()=='fi-slots' :
                slot_list=[]
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='fi-slot')
                lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                for slot in lst:
                    slotObj=Slot()
                    attributes=slot.value.strip().split(";")
                    slotObj.id=attributes[0].strip()
                    slotObj.ports=attributes[1].strip()
                    slot_list.append(slotObj)
                return slot_list
            elif attribute.strip()=='fi-uuid-pools':      
                uuidpool_list=[]
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='fi-uuid-pool')
                lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                for pool in lst:
                    uuidObj=Uuid_pool()
                    attributes=pool.value.strip().split(";")
                    uuidObj.name=attributes[0].strip()
                    uuidObj.start=attributes[1].strip()
                    uuidObj.end=attributes[2].strip()
                    uuidpool_list.append(uuidObj)
                return uuidpool_list
            elif attribute.strip()=='fi-mac-pools':
                macpool_list=[]
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label__startswith='fi-mac-pool')
                lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                for mac in lst:
                    macpoolObj=Mac_pool()
                    attributes=mac.value.strip().split(";")
                    macpoolObj.name=attributes[0].strip()
                    macpoolObj.start=attributes[1].strip()
                    macpoolObj.end=attributes[2].strip() 
                    macpool_list.append(macpoolObj)
	        return macpool_list
	    elif attribute.strip()=='fi-vnics':
                vnic_list=[]
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype,  standard_label__startswith='fi-vnic(')
                lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                for vnic in lst:
                    vnicObj=Vnic()
                    attributes=vnic.value.strip().split(";")
                    vnicObj.name=attributes[0].strip()
                    vnicObj.start=attributes[1].strip()
                    vnicObj.end=attributes[2].strip()
                    vnic_list.append(vnicObj)
		return vnic_list
	    elif attribute.strip()=='fi-ip-pools':
                ip_pool_list=[]
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype,  standard_label__startswith='fi-ip-pool(')
                lst=DeviceSetting.objects.filter(device=self.device,device_type_setting=setting)
                for ippool in lst:
                    ippoolObj=Ip_pool()
                    attributes=ippool.value.strip().split(";")
                    ippoolObj.name=attributes[0].strip()
                    ippoolObj.start=attributes[1].strip()
                    ippoolObj.end=attributes[2].strip()
		    ippoolObj.gateway=attributes[3].strip()
		    ippoolObj.subnet=attributes[4].strip()
                    ip_pool_list.append(ippoolObj)
                return ip_pool_list
            else:
                setting = DeviceTypeSetting.objects.get(dtype=self.device.dtype, standard_label=attribute.strip())
                return DeviceSetting.objects.get(device=self.device,device_type_setting=setting).value

        except django.core.exceptions.ObjectDoesNotExist:
            print "*" * 10 + "Atrribute Does not exists" + "*" * 10


#!/usr/bin/env python
import os
import sys
root_path = os.path.abspath(r"..")
sys.path.append(root_path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unifiedstack.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
    from configurator.models import Device, DeviceTypeSetting, DeviceSetting
    
    #USAGE

    #SWITCH
    #Getting Vlans, interfaces and port-channels 
    #Value returned as List. Iterate and get the values
    device_id=Device.objects.get(dtype=DeviceTypeSetting.SWITCH_TYPE)
    vlanObjectList=Switch(device_id).get('vlans')
    for i in vlanObjectList:
	print i.id
	print i.ip
	print i.netmask
    print "*" * 60
    #Getting simple configuration field's value
    device_id=Device.objects.get(dtype=DeviceTypeSetting.SWITCH_TYPE)
    print Switch(device_id).get('username')
    print "*" * 60
    print "*" * 60

    #FI
    #Getting fi-slots, fimac-pools and other mutiple value fields
    #Value returned as List. Iterate and get the values
    fiSlotsObjectList=FI().get('fi-slots')
    for i in fiSlotsObjectList:
	print i.id
	print i.ports
    print "*" * 60
    #Getting simple configuration field's value
    print FI().get('fi-mgmt-native-vlan')
    print "*" * 60
    print "*" * 60
	    
    #General
    print General().get('host-ip-address')    
    print General().get('rhel-image-url') 
    print "*" * 60
    print "*" * 60
    #Packstack
    print Packstack().get('keystone-admin-pw')   
    print "*" * 60
    #If Cobbler is being used. 
    #TO get the list of all compute-hosts	
    compute_hosts_ip_list=Cobbler().get_compute_hosts_ip()
    for i in compute_hosts_ip_list:
	print i
    print "*" * 60
    #To get network-hosts
    network_hosts_ip_list=Cobbler().get_network_hosts_ip()
    for i in network_hosts_ip_list:
        print i
    print "*" * 60
    #Similarly if Foreman is bring used
    compute_hosts_ip_list=Cobbler().get_compute_hosts_ip()
    for i in compute_hosts_ip_list:
        print i
