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


class New_profile():

    def __init__(
            self,
            name=None,
            owners=None,
            distro=None,
            enable_pxe_menu=True,
            kickstart_file='/var/lib/cobbler/kickstarts/rhe7-osp5.ks',
            proxy=None,
            repos=None):
        """Required fields are name, distro"""
        # profile name
        self.name = name
        # list of owners delimited by commas
        self.owners = owners
        # The distro to be used with this profile
        self.distro = distro
        self.enable_pxe_menu = enable_pxe_menu
        # full path of the kickstart
        self.kickstart_file = kickstart_file
        self.proxy = proxy
        # Space delimited list of repos
        self.repos = repos

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_owners(self, owners):
        self.owners = owners

    def get_owners(self):
        return self.owners

    def set_distro(self, distro):
        self.distro = distro

    def get_distro(self):
        return self.distro

    def set_enable_pxe_menu(self, enable_pxe_menu):
        self.enable_pxe_menu = enable_pxe_menu

    def get_enable_pxe_menu(self):
        return self.enable_pxe_menu

    def set_repos(self, repos):
        self.repos = repos

    def get_repos(self):
        return self.repos

    def set_kickstart_file(self, kickstart_file):
        self.kickstart_file = kickstart_file

    def get_kickstart_file(self):
        return self.kickstart_file

    def set_proxy(self, proxy):
        self.proxy = proxy

    def get_proxy(self):
        return self.proxy

    def save_profile(self):
        try:
            if not is_basestring(self.name):
                raise Exception("Name must be of string ")
            if self.owners is not None and not is_basestring(self.owners):
                raise Exception("Owners must be comma separated string ")
            if not is_basestring(self.distro):
                raise Exception("distro URL must be of string ")
            if not is_basestring(self.kickstart_file):
                raise Exception("kickstart file URL must be of string ")
            if self.repos is not None and not is_basestring(self.repos):
                raise Exception(
                    "repos must be of string with space delimited parameters")
            if not isinstance(self.enable_pxe_menu, bool):
                raise Exception("OS version must be True or False")
            if self.proxy is not None and not is_basestring(self.proxy):
                raise Exception("proxy must be of a string ")
            if self.name is None or self.distro is None:
                raise Exception("Name and distro are required")
        except Exception as e:
            print str(e)
            return False

        # Virtualization features hard coded
        virt_auto_boot = True
        # number of virtual CPUs
        virt_cpu = 1
        # Size of storage in GB
        virt_file_size = 5
        # size of RAM in KB
        virt_ram = 512
        # hypervisor type by default xenpv
        virt_type = 'xenpv'
        # path where the virtual files to be stored
        # necessary only in advanced cases
        virt_bridge = 'xenbr0'
        virt_disk_driver_type = 'raw'

        cobbler_api_handle = cobapi.BootAPI()
        try:
            # check whether profile with this name already exists
            if not cobbler_api_handle.find_profile(self.name) is None:
                raise Exception("Profile with this name already exist")
            if cobbler_api_handle.find_distro(self.distro) is None:
                raise Exception("Distro specified is not found")
            cobbler_profile = cobbler_api_handle.new_profile()
            cobbler_profile.set_name(self.name)
            cobbler_profile.set_distro(self.distro)
            cobbler_profile.set_enable_menu(self.enable_pxe_menu)
            if self.repos is not None:
                cobbler_profile.set_repos(self.repos)
            if self.proxy is not None:
                cobbler.set_proxy(self.proxy)
            
            if self.kickstart_file is not None:
                cobbler_profile.set_kickstart(self.kickstart_file)
            if self.owners is not None:
                cobbler_profile.set_owners(self.owners)
            else:
                cobbler_profile.set_owners('admin')
            cobbler_profile.set_virt_auto_boot(virt_auto_boot)
            cobbler_profile.set_virt_cpus(virt_cpu)
            cobbler_profile.set_virt_file_size(virt_file_size)
            cobbler_profile.set_virt_ram(virt_ram)
            cobbler_profile.set_virt_type(virt_type)
            cobbler_profile.set_virt_bridge(virt_bridge)
            cobbler_profile.set_virt_disk_driver(virt_disk_driver_type)
            # save the profile
            cobbler_api_handle.add_profile(cobbler_profile)
        except Exception as e:
            print str(e)
            return False
        return True


class Profile_operate():

    def __init__(self):
        pass

    def copy_profile(self, src_profile_name, new_profile_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(src_profile_name):
                raise("src profile name  must be string")
            if not is_basestring(new_profile_name):
                raise("new profile name must be string")
            reference = cobbler_api_handle.find_profile(src_profile_name)
            if reference is None:
                raise Exception(
                    "profile with name " +
                    src_profile_name +
                    " does not exists")
            if not cobbler_api_handle.find_profile(new_profile_name) is None:
                raise Exception(
                    "profile with name " +
                    new_profile_name +
                    " already exist. Give Some other name for the profile being created")
            cobbler_api_handle.copy_profile(reference, new_profile_name)
        except Exception as e:
            print str(e)
            return False
        return True

    def rename_profile(self, old_profile_name, new_profile_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(old_profile_name):
                raise("old profile name must be string")
            if not is_basestring(new_profile_name):
                raise("new profile name must be string")
            reference = cobbler_api_handle.find_profile(old_profile_name)
            if reference is None:
                raise Exception(
                    "profile with name " +
                    old_profile_name +
                    " does not exists")
            if not cobbler_api_handle.find_profile(new_profile_name) is None:
                raise Exception(
                    "profile with name " +
                    new_profile_name +
                    " already exist. Give some other name")
            cobbler_api_handle.rename_profile(reference, new_profile_name)
        except Exception as e:
            print str(e)
            return False
        return True

    def delete_profile(self, profile_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(profile_name):
                raise("name of the profile to be deleted must be string")
            reference = cobbler_api_handle.find_profile(profile_name)
            if reference is None:
                raise Exception(
                    "Profile with " +
                    profile_name +
                    " does not exists")
            cobbler_api_handle.remove_profile(reference)
        except Exception as e:
            print str(e)
            return False
        return True

    def edit_profile(
            self,
            profile_name,
            new_owners=None,
            new_distro=None,
            new_enable_pxe_menu=None,
            new_kickstart_file=None,
            new_proxy=None,
            new_repos=None):
        """Edit the existing distro. The name is not editable"""
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(profile_name):
                raise("Profile name must be string")
            reference = cobbler_api_handle.find_profile(profile_name)
            if reference is None:
                raise Exception(
                    "Profile with " +
                    profile_name +
                    " does not exists")
            if new_owners is not None and not is_basestring(new_owners):
                raise Exception("Owners must be comma separated string ")
            if new_distro is not None and not is_basestring(new_distro):
                raise Exception("distro URL must be of string ")
            if new_kickstart_file is not None and not is_basestring(
                    new_kiskstart_file):
                raise Exception("kickstart file URL must be of string ")
            if new_repos is not None and not is_basestring(new_repos):
                raise Exception(
                    "repos must be of string with space delimited parameters")
            if new_enable_pxe_menu is not None and not isinstance(
                    new_enable_pxe_menu,
                    bool):
                raise Exception("Enable pxe menu must be True or False")
            if new_proxy is not None and not is_basestring(new_proxy):
                raise Exception("proxy must be of a string ")
            if new_owners is not None:
                reference.set_owners(new_owners)
            if new_distro is not None:
                reference.set_distro(new_distro)
            if new_kickstart_file is not None:
                reference.set_kickstart_file(new_kickstart_file)
            if new_repos is not None:
                reference.set_repos(new_repos)
            if new_proxy is not None:
                reference.set_proxy(new_proxy)
            if new_enable_pxe_menu is not None:
                reference.set_enable_menu(new_enable_pxe_menu)
            cobbler_api_handle.add_profile(reference)
        except Exception as e:
            print str(e)
            return False
        return True

if __name__ == "__main__":
    """Refer this section for usage."""

    ref = Profile_operate()
    ref.delete_profile("profile1")
    """
    ref=New_profile("profile2","admin,cobbler","RHEL7-4")
    ref.save_profile()
    """
