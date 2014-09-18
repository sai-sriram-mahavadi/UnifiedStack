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
from general_utils import shell_command, bcolors, shell_command_true
import os
import sys

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)
from UnifiedStack.config.Config_Parser import Config


def enable_repos():

    redhat_username = Config.get_cobbler_field('redhat_username')
    redhat_password = Config.get_cobbler_field('redhat_password')
    redhat_pool = Config.get_cobbler_field('redhat_pool')
    # Subscription
    shell_command_true(
        "subscription-manager register --username=" +
        redhat_username +
        " --password=" +
        redhat_password)
    shell_command_true("subscription-manager attach --pool=" + redhat_pool)

    # Enabling the XML repos database of linux for installing
    shell_command("yum update -y")
    shell_command(
        "sudo yum-config-manager --enable rhel-7-server-openstack-5.0-rpms")
    shell_command(
        "sudo yum-config-manager --enable home_libertas-ict_cobbler26")
    shell_command("yum clean all")
    shell_command("yum repolist all")


def disable_SELinux():
    # disable SELinux and reboot
    shell_command_true(
        "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config")
    shell_command("yum update -y")


if __name__ == "__main__":
    enable_repos()
    disable_SELinux()
