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

"""
Note:-- Every operation returns True or False
        for success or unsuccess.
        Also every parameter being passed is checked
        if it is of correct type and in correct format
        using basestring  method if it needs to be a
        string or using isinstance method with the
        correct type it is supposed to be.
        Ex. owners should be passed as string with
        owners separated by comma.
"""


class New_distro():

    """Create an instance of New_Distro. While instantiation
       call the constructor with the required parameters.
       kernel--full path of the vmlinuz file
       initrd-- full path of the initrd.img file
       arch--architecture
       os_version-- ex. rhel7, rhel6
       owners-- who are the owners of the distro

       Note that u can send the parameters during the
       New_distro constructor call or these parameters
       can be set using set_XXX method.
       The constructor will return the reference to the
       New_distro object. Call the save_distro method
       on it.
       For usage:- refer to the __name__==__main__
       section at the bottom of file.

    """

    def __init__(
            self,
            name=None,
            kernel=None,
            initrd=None,
            arch=None,
            os_version=None,
            owners=None):
        # distro name
        self.name = name
        # list of owners
        self.owners = owners
        # URL of kernel i.e path of vmlinuz
        self.kernel = kernel
        # URL of initrd.img
        self.initrd = initrd
        # distro architecture
        self.arch = arch
        # distro os_version
        self.os_version = os_version

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_owners(self, owners):
        self.owners = owners

    def get_owners(self):
        return self.owners

    def set_kernel(self, kernel):
        slef.kernel = kernel

    def get_kernel(self):
        return sele.kernel

    def set_initrd(self):
        self.initrd = initrd

    def set_arch(self):
        self.arch = arch

    def get_arch(self):
        return self.arch

    def set_os_version(self, os_version):
        self.os_verison = os_version

    def get_os_verison(self):
        return self.os_version

    def save_distro(self):
        """Call this method on the instance of New_distro object
           to add a new distro.
        """
        try:
            if not is_basestring(self.name):
                raise Exception("Name must be of string")
            if self.owners is not None and not is_basestring(self.owners):
                raise Exception("Owners must be comma separated string type")
            if not is_basestring(self.kernel):
                raise Exception("kernel URL must be of string type")
            if not is_basestring(self.initrd):
                raise Exception("initrd URL must be of string type")
            if self.arch is not None and not is_basestring(self.arch):
                raise Exception("Kernel arch must be of string type")
            if self.os_version is not None and not is_basestring(
                    self.os_version):
                raise Exception("OS version must be of string type")
            if self.name is None or self.kernel is None or self.initrd is None:
                raise Exception("Name, kernel URL and initrd URL is required")
        except Exception as e:
            print str(e)
            return False

        cobbler_api_handle = cobapi.BootAPI()
        try:
            # check whether distro with this name already exists
            if not cobbler_api_handle.find_distro(self.name) is None:
                raise Exception("Distro with this name already exist")
            cobbler_distro = cobbler_api_handle.new_distro()
            # Below is called the API methods of the
            # cobbler.item_distro package.
            cobbler_distro.set_name(self.name)
            cobbler_distro.set_kernel(self.kernel)
            cobbler_distro.set_initrd(self.initrd)
            # assumption--x86_64 is the default arch
            if self.arch is not None:
                cobbler_distro.set_arch(self.arch)
            else:
                cobbler_distro.set_arch('x86_64')
            # assumptiom--rhel7 is the default os_version
            if self.os_version is not None:
                cobbler_distro.set_os_version(self.os_version)
            else:
                cobbler_distro.set_os_version('rhel7')
            # assumption--admin is the default owner
            if self.owners is not None:
                cobbler_distro.set_owners(self.owners)
            else:
                cobbler_distro.set_owners('admin')
            # Assumtiom--Since the prototype is for
            # openstack setup breed is redhat by default
            # modify __init__() to accept os breed in case
            # apart from rhel any other o/s is going to be
            # used.
            cobbler_distro.set_breed('redhat')
            print "Ok"
            cobbler_api_handle.add_distro(cobbler_distro)
        except Exception as e:
            print str(e)
            return False
        return True


class Distro_operate():

    """Create an instance of Distro_operate to delete
       copy, rename or edit an existing distro
       Usage:-- Create an instance of the Distro_operate
       class and call the methods like edit, copy etc.
       to perform operation. For usage see the __name__
       ==__main__ section at the bottom of file.
    """

    def __init__(self):
        pass

    def copy_distro(self, src_distro_name, new_distro_name):
        """Provide the distro name of an existing distro which
           is to be copied and the name of the newly distro
           being created.
           src_distro name is the name of the existing distro
           which is to be copied.
        """
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(src_distro_name):
                raise("src distro name  must be string")
            if not is_basestring(new_distro_name):
                raise("new distro name must be string")
            reference = cobbler_api_handle.find_distro(src_distro_name)
            # check if the source distro exists
            if reference is None:
                raise Exception(
                    "Distro with name " +
                    src_distro_name +
                    " does not exists")
            # if a distro with the name same as new_distro already exists
            # the copy operation can't be performed.
            if not cobbler_api_handle.find_distro(new_distro_name) is None:
                raise Exception(
                    "Distro with name " +
                    new_distro_name +
                    " already exist. Give Some other name for the ditstro being created")
            cobbler_api_handle.copy_distro(reference, new_distro_name)
        except Exception as e:
            print str(e)
            return False
        return True

    def rename_distro(self, old_distro_name, new_distro_name):
        """old_distro_name is the existing name of the distro.
           new_distro name is the new name.
        """
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(old_distro_name):
                raise("old distro name must be string")
            if not is_basestring(new_distro_name):
                raise("new distro name must be string")
            reference = cobbler_api_handle.find_distro(old_distro_name)
            # check if odl_distro already exists.
            if reference is None:
                raise Exception(
                    "Distro with name " +
                    old_distro_name +
                    " does not exists")
            # if a distro with the name same as new_distro already exists
            # the rename operation can't be performed.
            if not cobbler_api_handle.find_distro(new_distro_name) is None:
                raise Exception(
                    "Distro with name " +
                    new_distro_name +
                    " already exist. Give some other name")
            cobbler_api_handle.rename_distro(reference, new_distro_name)
        except Exception as e:
            print str(e)
            return False
        return True

    def delete_distro(self, distro_name):
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(distro_name):
                raise("name of the distro to be deleted must be string")
            reference = cobbler_api_handle.find_distro(distro_name)
            # check if the distro being deleted does exists.
            if reference is None:
                raise Exception(
                    "Distro with " +
                    distro_name +
                    " does not exists")
            cobbler_api_handle.remove_distro(reference)
        except Exception as e:
            print str(e)
            return False
        return True

    def edit_distro(
            self,
            distro_name,
            new_kernel=None,
            new_initrd=None,
            new_owners=None,
            new_arch=None,
            new_os_version=None):
        """Edit the existing distro. The name is not editable
           Pass the parameters which needs to be changed to this
           function.
        """
        cobbler_api_handle = cobapi.BootAPI()
        try:
            if not is_basestring(distro_name):
                raise distro_name
            reference = cobbler_api_handle.find_distro(distro_name)
            # checking if distro already exists
            if reference is None:
                raise Exception(
                    "Distro with " +
                    distro_name +
                    " does not exists")
            if new_owners is not None and not is_basestring(new_owners):
                raise Exception("Owners must be comma separated string type")
            if new_kernel is not None and not is_basestring(new_kernel):
                raise Exception("kernel URL must be of string type")
            if new_initrd is not None and not is_basestring(new_initrd):
                raise Exception("initrd URL must be of string type")
            if new_arch is not None and not is_basestring(new_arch):
                raise Exception("Kernel arch must be of string type")
            if new_os_version is not None and not is_basestring(
                    new_os_version):
                raise Exception("OS version must be of string type")
            if new_kernel is not None:
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
        except Exception as e:
            print str(e)
            return False
        return True


if __name__ == "__main__":
    """This section can be seen for knowing usage."""

    # refer=Distro_operate()
    #refer.edit_distro('test',new_owners='admin, cobbler')
    ref = New_distro(
        'test1',
        'rhel_mount/isolinux/vmlinuz',
        'rhel_mount/isolinux/initrd.img',
        owners='admin, cobbler')
    ref.save_distro()
