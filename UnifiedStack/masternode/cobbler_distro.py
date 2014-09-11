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

class New_distro():
    def __init__(self,name=None,kernel=None,initrd=None,arch=None,os_version=None,owners=None):
        #distro name
        self.name=name
        #list of owners
        self.owners=owners
        #URL of kernel i.e path of vmlinuz
        self.kernel=kernel
        #URL of initrd.img
        self.initrd=initrd
        #distro architecture
        self.arch=arch
        #distro os_version
        self.os_version=os_version

    def set_name(self,name):
        self.name=name

    def get_name(self):
        return self.name

    def set_owners(self,owners):
        self.owners=owners

    def get_owners(self):
        return self.owners

    def set_kernel(self,kernel):
        slef.kernel=kernel

    def get_kernel(self):
        return sele.kernel

    def set_initrd(self):
        self.initrd=initrd

    def set_arch(self):
        self.arch=arch

    def get_arch(self):
        return self.arch

    def set_os_version(self,os_version):
        self.os_verison=os_version

    def get_os_verison(self):
        return self.os_version

    def save_distro(self):
        try:
            if not is_basestring(self.name):
                raise Exception("Name must be of string")
            if self.owners is not None and not is_basestring(self.owners):
                raise Exception("Owners must be comma separated string type")
            if not is_basestring(self.kernel):
                raise Exception("kernel URL must be of string type")
            if not is_basestring(self.initrd):
                raise Exception("initrd URL must be of string type")
            if self.arch is not None and  not is_basestring(self.arch):
                raise Exception("Kernel arch must be of string type")
            if self.os_version is not None and not is_basestring(self.os_version):
                raise Exception("OS version must be of string type")
            if self.name is None or self.kernel is None or self.initrd is None:
                raise Exception("Name, kernel URL and initrd URL is required")
        except Exception,e:
            print str(e)
            return False
        cobbler_api_handle=cobapi.BootAPI()
        try:
        #check whether distro with this name already exists
            if not cobbler_api_handle.find_distro(self.name) is None:
                raise Exception("Distro with this name already exist")
            cobbler_distro=cobbler_api_handle.new_distro()
            cobbler_distro.set_name(self.name)
            cobbler_distro.set_kernel(self.kernel)
            cobbler_distro.set_initrd(self.initrd)
            if self.arch is not None:
                cobbler_distro.set_arch(self.arch)
            else:
                cobbler_distro.set_arch('x86_64')
            if self.arch is not None:
                cobbler_distro.set_os_version(self.os_version)
            else:
                cobbler_distro.set_os_version('rhel7')
            if self.owners is not None:
                cobbler_distro.set_owners(self.owners)
            else:
                cobbler_distro.set_owners('admin')
            cobbler_distro.set_breed('redhat')
            cobbler_api_handle.add_distro(cobbler_distro)
        except Exception,e:
            print str(e)
            return False
        return True

class Distro_operate():
    def __init__(self):
        pass

    def copy_distro(self,src_distro_name,new_distro_name):
        cobbler_api_handle=cobapi.BootAPI()
        try:
            if not is_basestring(src_distro_name):
                raise("src distro name  must be string")
            if not is_basestring(new_distro_name):
                raise("new distro name must be string")
            reference=cobbler_api_handle.find_distro(src_distro_name)
            if reference is None:
                raise Exception("Distro with name " + src_distro_name + " does not exists")
            if not cobbler_api_handle.find_distro(new_distro_name) is None:
                raise Exception("Distro with name " + new_distro_name + " already exist. Give Some other name for the ditstro being created")
            cobbler_api_handle.copy_distro(reference,new_distro_name)
        except Exception,e:
            print str(e)
            return False
        return False

    def rename_distro(self,old_distro_name,new_distro_name):
        cobbler_api_handle=cobapi.BootAPI()
        try:
            if not is_basestring(old_distro_name):
                raise("old distro name must be string")
            if not is_basestring(new_distro_name):
                raise("new distro name must be string")
            reference=cobbler_api_handle.find_distro(old_distro_name)
            if reference is None:
                raise Exception("Distro with name " + old_distro_name + " does not exists")
            if not cobbler_api_handle.find_distro(new_distro_name) is None:
                raise Exception("Distro with name " + new_distro_name + " already exist. Give some other name")
            cobbler_api_handle.rename_distro(reference,new_distro_name)
        except Exception,e:
            print str(e)
            return False
        return True

    def delete_distro(self,distro_name):
        cobbler_api_handle=cobapi.BootAPI()
        try:
            if not is_basestring(distro_name):
                raise("name of the distro to be deleted must be string")
            reference=cobbler_api_handle.find_distro(distro_name)
            if reference is None:
                raise Exception("Distro with " + distro_name + " does not exists")
            cobbler_api_handle.remove_distro(reference)
        except Exception,e:
            print str(e)
            return False
        return True

    def edit_distro(self,distro_name,new_kernel=None,new_initrd=None,new_owners=None,new_arch=None,new_os_version=None):
        """Edit the existing distro. The name is now editable"""
        cobbler_api_handle=cobapi.BootAPI()
	try:
            if not is_basestring(distro_name):
                raise(distro_name + " must be string")
            reference=cobbler_api_handle.find_distro(distro_name)
            if reference is None:
                raise Exception("Distro with " + distro_name + " does not exists")
            if new_owners is not None and  not is_basestring(new_owners):
                raise Exception("Owners must be comma separated string type")
            if new_kernel is not None and not is_basestring(new_kernel):
                raise Exception("kernel URL must be of string type")
            if  new_initrd is not None and not is_basestring(new_initrd):
                raise Exception("initrd URL must be of string type")
            if  new_arch is not None and not is_basestring(new_arch):
                raise Exception("Kernel arch must be of string type")
            if  new_os_version is not None and not is_basestring(new_os_version):
                raise Exception("OS version must be of string type")
            if  new_kernel is not None:
                reference.set_kernel(new_kernel)
            if new_initrd is not None:
                reference.set_initrd(new_initrd)
            if new_owners is not None:
                reference.set_owners(new_owners)
            if new_arch is not None:
                reference.set_arch(new_arch)
            if new_os_version is not None:
                reference.set_os_version(new_os_version)
            cobbler_api_handle.add_distro(reference)
        except Exception,e:
            print str(e)
            return False
        return True

if __name__== "__main__":
    
    refer=Distro_operate()
    refer.edit_distro('test',new_owners='admin, cobbler')
    """
    ref=New_distro('test1','/mnt/isolinux/vmlinuz','/mnt/isolinux/initrd.img',owners='admin, cobbler')
    ref.save_distro()
    """
    

