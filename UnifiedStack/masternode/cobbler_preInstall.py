# Copyright 2014 Prakash Kumar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/python


# This File prepares system for cobbler installation.
from general_utils import shell_command, bcolors,exec_sed
import os


def enable_repos():
    #Enabling the XML repos database of linux for installing
    file1 = open("./cobbler.repo")
    file2 = open('/etc/yum.repos.d/cobbler.repo', 'w')
    lines = file1.readlines()
    file1.close()
    for line in lines:
        file2.write(line)
    file2.close()
    shell_command("yum update -y")
    shell_command(
        "sudo yum-config-manager --enable rhel-7-server-openstack-5.0-rpms")
    shell_command(
        "sudo yum-config-manager --enable home_libertas-ict_cobbler26")
    shell_command("yum clean all")
    shell_command("yum repolist all")
    print bcolors.OKGREEN + "Please check if rhel-7-server-openstack-5.0-rpms \
          and home_libertas-ict_cobbler26 is ENABLED. If not enable them by own"


def disable_SELinux():
    #disable SELinux and reboot
    exec_sed(
        "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config")
    shell_command("yum update -y")
    #Write the path of cobbler_setup.py in rc.local
    file = open("/etc/rc.local", "a")
    file.write("python " + os.getcwd() + '/cobbler_setup.py')
    file.close()
    shell_command("reboot")


if __name__ == "__main__":
    #enable_repos()
    disable_SELinux()
