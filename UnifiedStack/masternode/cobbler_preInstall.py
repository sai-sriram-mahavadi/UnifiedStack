#!/bin/sh
# exec /share/vim/vim74/vim "$@"

# This File prepares system for cobbler installation.
from general_utils import shell_command, bcolors


def enable_repos():
    # subscription
    print bcolors.OKGREEN + "Register to REDHAT subscription manager\n"\
        + "Enter your credentials when asked"
    shell_command("subscription-manager register")
    shell_command("subscription-manager subscribe --auto")
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

import os


def disable_SELinux():
    #disable SELinux and reboot
    shell_command(
        "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config")
    shell_command("yum -y update && reboot")
    #Write the path of cobbler_setup.py in rc.local
    file = open("/etc/rc.local", "a")
    file.write("python " + os.getcwd() + '/cobbler_setup.py')
    file.close()


if __name__ == "__main__":
    enable_repos()
    disable_SELinux()
