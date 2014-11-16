import cobbler_system as syst
import cobbler_profile as prof
import cobbler_distro as dist
import inspect
import os
import sys

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config.Config_Parser import Config


class Build_Server():

    def __init__(self):
        pass

    def create_distro(self,name):    
        # Config.get_distro_field("vmlinuz_path")
        vmlinuz_path = "/var/www/cobbler/images/RHEL/images/pxeboot/vmlinuz"
        # Config.get_distro_field("initrd_path")
        initrd_path = "/var/www/cobbler/images/RHEL/images/pxeboot/initrd.img"
        handle = dist.New_distro(
            name,
            kernel=vmlinuz_path,
            initrd=initrd_path)
        handle.save_distro()

    def create_profile(self,profiles): 
        for profile in profiles:
            name = profile.profile_name
            distro = profile.distro_name
            handle = prof.New_profile(name=name, distro=distro)
            handle.save_profile()
           

    def create_system(self,systems): 
        for system in systems:
            purpose = system.purpose
            hostname = system.hostname
            mac_addr = system.mac_address
            ipaddress = system.ip_address
            interface = system.interface
            profile = system.profile_name
	    proxy=system.http_proxy_ip + '80'
            #power_id= system.power_id
            power_type=system.power_type
            power_user=system.power_user
            power_pass=system.power_password
            power_addr=system.power_address
            name = '' + hostname + "-" + purpose
	    
            handle = syst.New_system(name=name,
				      hostname=hostname, 
           			      mac_addr=mac_addr,
				      ipaddr=ipaddress,
				      interface=interface,
         			      profile=profile, 
            			      power_management_username=power_user,
				      power_management_type=power_type,
            			      power_management_password=power_pass,
				      power_management_addr=power_addr)            	    
	    handle.save_system()
	    

    def power_on_systems(self,systems):
	    handle=syst.System_operate() 
	    for system in systems:
		purpose = system.purpose
                hostname = system.hostname
		name = '' + hostname + "-" + purpose
		try:
                    if handle.power_on(name):
			print "System " + name + " powered on"
		    else:
			raise Exception("Not able to power on System " + name )
		except Exception,e:
		    print e

    def power_off_systems(self,systems):
            handle=syst.System_operate() 
            for system in systems:
                purpose = system.purpose
                hostname = system.hostname
                name = '' + hostname + "-" + purpose
                try:
                    if handle.power_off(name):
                        print "System " + name + " powered off"
                    else:
                        raise Exception("Not able to power off System " + name )
                except Exception,e:
                    print e

    def power_cycle_systems(self,systems):
            handle=syst.System_operate() 
            for system in systems:
                purpose = system.purpose
                hostname = system.hostname
                name = '' + hostname + "-" + purpose
                try:
                    if handle.power_off(name):
                        pass
                    else:
                        raise Exception("Not able to power off System " + name )
                    if handle.power_on(name):
                        pass
                    else:
                        raise Exception("Not able to power on System " + name )
                except Exception,e:
                    return False

		
    def disable_netboot_systems(self,systems):
	    handle=syst.System_operate()     
            for system in systems:
                purpose = system.purpose
                hostname = system.hostname
                name = '' + hostname + "-" + purpose
	        handle.edit_system(name,netboot_enabled=False)

    def enable_netboot_systems(self,systems):
            handle=syst.System_operate()  
            for system in systems:
                purpose = system.purpose
                hostname = system.hostname
                name = '' + hostname + "-" + purpose
                handle.edit_system(name,netboot_enabled=True)

	    
if __name__ == "__main__":
    handle=Build_Server()
    handle.enable_netboot_systems()
    #handle = Build_Server()

    #handle.create_distro()
