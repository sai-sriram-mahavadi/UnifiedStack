import cobbler_system as system
import cobbler_profile as profile
import cobbler_distro as distro
import inspect
import os
import sys

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config.Config_Parser import Config


class Build_Server():

    def __init__(self):
        pass

    def create_distro(self):
<<<<<<< HEAD
        name = "RHELx_86"  # Config.get_distro_field("distro_name")
=======
        name = "RHEL1"  # Config.get_distro_field("distro_name")
>>>>>>> upstream/proto
        # Config.get_distro_field("vmlinuz_path")
        vmlinuz_path = "rhel_mount/isolinux/vmlinuz"
        # Config.get_distro_field("initrd_path")
        initrd_path = "rhel_mount/isolinux/initrd.img"
        handle = distro.New_distro(
            name,
            kernel=vmlinuz_path,
            initrd=initrd_path)
        handle.save_distro()

    def create_profile(self):
        profiles = Config.get_profiles_data()
        for profile in profiles:
            name = profile.profile_name
            distro = profile.distro_name
            handle = distro.New_profile(name, distro)
            handle.save_distro()

    def create_system(self):
        systems = Config.get_systems_data()
        for system in systems:
            name = system.system_name
            purpose = system.purpose
            hostname = system.hostname
            mac_addr = system.mac_address
            ipaddress = system.ip_address
            interface = system.interface
            profile = system.profile_name
            name = '' + name + "-" + purpose
            handle = distro.New_system(
                name=name,
                hostname=hostname,
                mac_addr=mac_addr,
                ipaddr=ipaddress,
                interface=interface,
                profile=profile)
            handle.save_system()


if __name__ == "__main__":
    handle = Build_Server()
    handle.create_distro()
