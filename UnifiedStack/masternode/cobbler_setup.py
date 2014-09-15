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
from general_utils import shell_command, bcolors,shell_command_true
import inspect

# configurable parameters. These should go in conf file
cobbler_interface="enp0s8"
cobbler_ipaddress="192.168.133.4"
cobbler_netmask="255.255.255.0"
cobbler_server = cobbler_ipaddress
cobbler_next_server = cobbler_ipaddress
cobbler_subnet = "192.168.133.0"
cobbler_option_router = "192.168.133.254"
cobbler_DNS = cobbler_ipaddress


def cobbler_setup():
    shell_command_true(
        "/usr/bin/yum -y install cobbler cobbler-web screen which wget curl pykickstart fence-agents dhcp bind-chroot xinetd")
    shell_command_true("ifconfig " + cobbler_interface + " " + cobbler_ipaddress + " netmask " + cobbler_netmask)
    # setup cobbler
    shell_command_true(
        "sed -i 's/^default_password_crypted.*/default_password_crypted: \"$1$7DMgQ9Ew$5d4IbaDMzVQ0FbqiiOH600\"/' /etc/cobbler/settings")
    shell_command_true(
        "sed -i 's/^manage_dhcp:.*/manage_dhcp: 1/' /etc/cobbler/settings")
    shell_command_true(
        "sed -i 's/^manage_dns:.*/manage_dns: 1/' /etc/cobbler/settings")
    shell_command_true(
        "sed -i 's/^server:.*/server: " + cobbler_server + "/' /etc/cobbler/settings")
    shell_command_true(
        "sed -i 's/^next_server:.*/next_server: " +
        cobbler_next_server +
        "/' /etc/cobbler/settings")
    shell_command_true(
        "sed -i 's/^pxe_just_once:.*/pxe_just_once: 1/' /etc/cobbler/settings")

    shell_command_true(
        "sed -i 's/^module = authn_denyall/module = authn_configfile/' /etc/cobbler/modules.conf")

    print "\n" + bcolors.OKGREEN + "Please provide the password for Cobbler WEB"
    shell_command_true(
        "htdigest /etc/cobbler/users.digest \"Cobbler\" cobbler")
    
    # Setup DHCP template
    shell_command_true(
        "sed -i 's/^subnet 192.168.1.0/subnet " +
        cobbler_subnet +
        "/' /etc/cobbler/dhcp.template")
    shell_command_true(
        "sed -i 's/option routers.*/option routers " +
        cobbler_option_router +
        ";/' /etc/cobbler/dhcp.template")
    shell_command_true(
        "sed -i 's/domain-name-servers.*/domain-name-servers " +
        cobbler_DNS +
        ";/' /etc/cobbler/dhcp.template")
    shell_command_true(
        "sed -i 's/range dynamic-bootp.*/deny unknown-clients;/' /etc/cobbler/dhcp.template")
    shell_command("touch /etc/dhcp/dhcpd.CIMC.conf")
    shell_command_true(
        "sed -i '/^subnet/i include \"/etc/dhcp/dhcpd.CIMC.conf\";' /etc/cobbler/dhcp.template")

    # Add CIMC addresses to DHCP
    shell_command("touch /tmp/dhcpd.CIMC.conf")
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
    
    # Restart xinetd
    shell_command("systemctl restart xinetd.service")
    shell_command("iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT")
    shell_command("iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT")
	    
    #Open up Firewall
    shell_command_true("/sbin/iptables -F")
    shell_command_true("/sbin/iptables-save > /etc/sysconfig/iptables")
    
    #start dhcpd
    shell_command("systemctl start dhcpd.service")
    shell_command("systemctl enable dhcpd.service")
    shell_command("systemctl status dhcpd.service")



def sync():
    shell_command("cobbler get-loaders")
    import cobbler.api as capi
    handle = capi.BootAPI()
    handle.check()
    handle.sync()
    

if __name__ == "__main__":
    cobbler_setup()
    enable_services()
    sync()        
    file = open("/etc/rc.local", "r")
    lines = file.readlines()
    file.close()
    file = open("/etc/rc.local", "w")
    for line in lines:
        if 'python' not in line and inspect.getfile(
                inspect.currentframe()) not in line:
            file.write(line)
    file.close()
    file=open("rhel7-osp5.ks","r")
    lines = file.readlines()
    file.close()
    file = open("/var/lib/cobbler/kickstarts/rhel7-osp5.ks", "w")
    for line in lines:
        file.write(line)
    file.close()

               

