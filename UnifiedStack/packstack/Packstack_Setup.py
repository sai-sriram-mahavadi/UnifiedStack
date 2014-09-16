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

# Packstack_Setup.py:
# Sets up packstack makes the intial configuration settings necessary

import ConfigParser
import sys
import os
import subprocess

root_path = os.path.abspath(r"..\..")
sys.path.append(root_path)

from UnifiedStack.cli import Shell_Interpretter as shi
from UnifiedStack.cli import Console_Output as cono

class PackStackConfigurator:

    config = ConfigParser.ConfigParser(allow_no_value = True)
    config.read(r'packstack_original.cfg')
    
    def setup_packstack_pre_requisites(self):
        shell = shi.ShellInterpretter()
        shell.execute_command("/usr/bin/yum-config-manager --enable rhel-7-server-openstack-5.0-rpms")
        
    # rhel-7-server-openstack-5.0-rpms should be already enabled in yum repolist
    def install_packstack(self):
        #from Shell_Interpretter import ShellInterpretter
        #from ..cli.Shell_Interpretter import ShellInterpretter
        shell = shi.ShellInterpretter()
        shell.execute_command("/usr/bin/yum install -y openstack-packstack")

    def setup_packstack(self):
        shell = shi.ShellInterpretter()
        shell.execute_command("/usr/bin/packstack --answer-file=packstack_result.cfg")
    
    def generate_answer_file(self):
        #from Shell_Interpretter import ShellInterpretter
        shell = shi.ShellInterpretter()
        shell.execute_command("packstack --gen-answer-file=packstack.cfg")
        PackStackConfigurator.config.read(r'packstack.cfg')
    # def setup_passwords(self, password):
    # def setup_passwords(self, password):

    def backup_answer_file(self):
        with open(r'packstack_backup.cfg', 'wb') as configfile:
            PackStackConfigurator.config.write(configfile)
    
    def enable_packstack_field(self, section, field):
        self.set_packstack_field(section, field, 'y')

    def disable_packstack_field(self, section, field):
        self.set_packstack_field(section, field, 'n')

    def set_packstack_field(self, section, field, value):
        PackStackConfigurator.config.set(section, field, value)
        with open(r'packstack_result.cfg', 'wb') as configfile:
            PackStackConfigurator.config.write(configfile)
        
    def get_packstack_field(self, section, field):
        return PackStackConfigurator.config.get(section, field, 0) # Raw parse

    def is_packstack_field(self, section, field):
        value = self.get_packstack_field(section, field)
        return (value=='y')
    
if __name__ == "__main__":
    packstack = PackStackConfigurator()
    packstack.install_packstack()
    packstack.generate_answer_file()
    #packstack.backup_answer_file()
    #For Testing, change config-rw-pw to Cisco12345
    packstack.set_packstack_field("general", "CONFIG_RH_PW", "Cisco12345")

    #Turn off swift, Turn on Heat, set CVF ntp server
    packstack.disable_packstack_field("general", "CONFIG_SWIFT_INSTALL")
    packstack.enable_packstack_field("general", "CONFIG_HEAT_INSTALL")
    packstack.set_packstack_field("general", "CONFIG_NTP_SERVERS", "cvf-ntp1")

    #Move networker and compute services to proper nodes
    packstack.set_packstack_field("general", "CONFIG_COMPUTE_HOSTS", "192.168.131.10,192.168.131.11")
    packstack.set_packstack_field("general", "CONFIG_NETWORK_HOSTS", "192.168.131.9")

    #Customers will want to set admin keystone password to something sane
    packstack.set_packstack_field("general", "CONFIG_KEYSTONE_ADMIN_PW", "Cisco12345")

    #Set oversubscription based on Karen's requirements
    packstack.set_packstack_field("general", "CONFIG_NOVA_SCHED_CPU_ALLOC_RATIO", "8.0")
    packstack.set_packstack_field("general", "CONFIG_NOVA_SCHED_RAM_ALLOC_RATIO", "1.0")

    #Configure neutron mechanism drivers and networking
    packstack.set_packstack_field("general", "CONFIG_NEUTRON_ML2_TYPE_DRIVERS", "vlan")
    packstack.set_packstack_field("general", "CONFIG_NEUTRON_ML2_TENANT_NETWORK_TYPES", "vlan")
    packstack.set_packstack_field("general", "CONFIG_NEUTRON_ML2_MECHANISM_DRIVERS", "openvswitch,cisco_nexus")
    packstack.set_packstack_field("general", "CONFIG_NEUTRON_ML2_VLAN_RANGES", "physnet:2100:2999")

    #Do not configure demo project/user/network
    packstack.disable_packstack_field("general", "CONFIG_PROVISION_DEMO")

    packstack.setup_packstack()
