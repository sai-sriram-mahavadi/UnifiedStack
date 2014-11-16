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


def enable_repos(console,redhat_username,redhat_password,redhat_pool):
    # Subscription
    console.cprint_progress_bar("Running Subscription manager",1)
    shell_command_true(
        "subscription-manager register --username=" +
        redhat_username +
        " --password=" +
        redhat_password) 
    shell_command_true("subscription-manager attach --pool=" + redhat_pool)
    console.cprint_progress_bar("Updating the System",10)
    # Enabling the XML repos database of linux for installing
    shell_command("yum update -y")
    console.cprint_progress_bar("Enabling the Required Repositories",50)
    shell_command(
        "sudo yum-config-manager --enable rhel-7-server-openstack-5.0-rpms") 
    shell_command(
        "sudo yum-config-manager --enable home_libertas-ict_cobbler26")
    console.cprint_progress_bar("Cleaing the repositories list and populating",60)
   

def install_prerequistes(): 
    shell_command("wget https://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz -O /root/pip_tar_file.tar.gz")
    shell_command("tar -zxvf /root/pip_tar_file.tar.gz -C /root/")
    shell_command("pushd /root/pip-1.2.1; python setup.py install; popd")
    shell_command("pip install django==1.7")
    shell_command("pip install djangorestframework")
    shell_command("wget https://communities.cisco.com/servlet/JiveServlet/download/36899-13-76835/UcsSdk-0.8.3.tar.gz -O /root/UcsSdk-0.8.3.tar.gz")
    shell_command("tar -zxvf /root/UcsSdk-0.8.3.tar.gz -C /root/")
    shell_command("pushd /root/UcsSdk-0.8.3; python setup.py install; popd")
        

def disable_SELinux(console):
    # disable SELinux and reboot
    console.cprint_progress_bar("Disabling the SELinux",80)
    shell_command_true(
        "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config")
    shell_command("yum update -y")
    console.cprint_progress_bar("Reupdating",90)
    console.cprint_progress_bar("TASK COMPLETED",100)    

def enable_networking(console):
    cobbler_interface = Config.get_cobbler_field('cobbler_interface')
    cobbler_ipaddress = Config.get_cobbler_field('cobbler_ipaddress')
    cobbler_netmask = Config.get_cobbler_field('cobbler_netmask')
    file=open("/etc/sysconfig/network-scripts/ifcfg-" + cobbler_interface,"w")
    file.write("DEVICE=" + cobbler_interface + "\n")
    file.write("IPADDR=" + cobbler_ipaddress + "\n")
    file.write("NETMASK=" + cobbler_netmask + "\n" )
    file.close()

def add_name_server(console):
    console.cprint_progress_bar("Reupdating",90)
    name_server=Config.get_general_field("name-server")
    file=open("/etc/resolv.conf","r")
    lines=file.readlines()
    file.close() 
    found=False
    for line in lines:
	if "nameserver" in line:
	    found=True
            break
    if not found:
        file=open("/etc/resolv.conf","w")
        file.writelines(lines)
        file.write("nameserver " + name_server) 
        file.close()
    console.cprint_progress_bar("TASK COMPLETED",100)
 

