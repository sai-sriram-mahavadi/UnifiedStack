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

# This File sets up the cobbler node.
from general_utils import shell_command, bcolors,exec_sed

# configurable parameters. These should go in conf file
server = "10.0.2.15"
next_server = "10.0.2.15"
subnet = "10.0.2.0"
option_router = "10.0.2.254"
DNS = "10.0.2.0"


def cobbler_setup():
    exec_sed(
        "yum -y install cobbler cobbler-web screen which wget curl pykickstart fence-agents dhcp bind-chroot iptables.service")
    # setup cobbler
    exec_sed(
        "sed -i 's/^default_password_crypted.*/default_password_crypted: \"$1$7DMgQ9Ew$5d4IbaDMzVQ0FbqiiOH600\"/' /etc/cobbler/settings")
    exec_sed(
        "sed -i 's/^manage_dhcp:.*/manage_dhcp: 1/' /etc/cobbler/settings")
    exec_sed(
        "sed -i 's/^manage_dns:.*/manage_dns: 1/' /etc/cobbler/settings")
    exec_sed(
        "sed -i 's/^server:.*/server: " + server + "/' /etc/cobbler/settings")
    exec_sed(
        "sed -i 's/^next_server:.*/next_server: " +
        next_server +
        "/' /etc/cobbler/settings")
    exec_sed(
        "sed -i 's/^pxe_just_once:.*/pxe_just_once: 1/' /etc/cobbler/settings")

    exec_sed(
        "sed -i 's/^module = authn_denyall/module = authn_configfile/' /etc/cobbler/modules.conf")

    print "\n" + bcolors.OKGREEN + "Please provide the password for Cobbler WEB"
    exec_sed(
        "htdigest /etc/cobbler/users.digest \"Cobbler\" cobbler")
    
    # Setup DHCP template
    exec_sed(
        "sed -i 's/^subnet 192.168.1.0/subnet " +
        subnet +
        "/' /etc/cobbler/dhcp.template")
    exec_sed(
        "sed -i 's/option routers.*/option routers " +
        option_router +
        ";/' /etc/cobbler/dhcp.template")
    exec_sed(
        "sed -i 's/domain-name-servers.*/domain-name-servers " +
        DNS +
        ";/' /etc/cobbler/dhcp.template")
    exec_sed(
        "sed -i 's/range dynamic-bootp.*/deny unknown-clients;/' /etc/cobbler/dhcp.template")
    exec_sed(
        "sed -i '/^subnet/i include \"/etc/dhcp/dhcpd.CIMC.conf\";' /etc/cobbler/dhcp.template")

    # Add CIMC addresses to DHCP
    shell_command("cp /tmp/dhcpd.CIMC.conf /etc/dhcp/")


def enable_services():
    # Turn on cobbler
    shell_command("systemctl start cobblerd.service")
    shell_command("systemctl enable cobblerd.service")
    shell_command("systemctl status cobblerd.service")

    # Turn on apache
    shell_command("systemctl start httpd.service")
    shell_command("systemctl enable httpd.service")
    shell_command("systemctl status httpd.service")
    """
    # Restart xinetd
    shell_command("systemctl restart xinetd.service")

    # Allow traffic on ports 80 and 443
    shell_command(
        "/sbin/iptables -A INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT")
    shell_command(
        "/sbin/iptables -A INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT")
 
    # Restart iptables
    shell_command("systemctl restart xinetd.service")
    shell_command("systemctl status xinetd.service")
    """
    # Open up Firewall
    shell_command("/sbin/iptables -F")
    shell_command("/sbin/iptables-save > /etc/sysconfig/iptables")




def sync():
    shell_command("cobbler get-loaders")
    import cobbler.api as capi
    handle = capi.BootAPI()
    handle.check()
    handle.sync()
    print "Sync Successful"

def setup_Install_Server():
    # Assuming the RHEL dvd.iso is already downloaded in the /root directory
    # So the lines below has been commented
    # shell_command("wget https://access.cdn.redhat.com/content/origin/files\
    #       /sha256/85/85a9fedc2bf0fc825cc7817056aa00b3ea87d7e111e0cf8de77d3ba643f8646c/\
    #        rhel-server-7.0-x86_64-dvd.iso?_auth_=1406320140_25139854a8d910baebec0c004b2\
    #        a4ad9 -O /root/rhel-server-7.0-x86_64-dvd.iso")

    #import RHEL
    shell_command(
        "mount -t iso9660 -o loop,ro /root/rhel-server-7.0-x86_64-dvd.iso /mnt")
    shell_command("cobbler import --name=RHEL7 --arch=x86_64 --path=/mnt")
    shell_command("umount /mnt")
    #shell_command("rm /root/rhel-server-7.0-x86_64-dvd.iso")
    shell_command(
        "sed -i '/^\%packages/a wget' /var/lib/cobbler/kickstarts/sample_end.ks")

import inspect
if __name__ == "__main__":
    #cobbler_setup()
    enable_services()
    sync()
    setup_Install_Server()
    file = open("/etc/rc.local", "r")
    lines = file.readlines()
    file.close()
    file = open("/etc/rc.local", "w")
    for line in lines:
        if 'python' not in line and inspect.getfile(
                inspect.currentframe()) not in line:
            file.write(line)
    file.close()
                       

