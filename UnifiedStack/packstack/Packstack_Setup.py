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

# Sets up packstack makes the intial packstack_configuration settings necessary

import ConfigParser
import sys
import os
import subprocess

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.cli import Shell_Interpretter as shi
from UnifiedStack.cli import Console_Output as cono
from UnifiedStack.config import Config_Parser

AffirmativeList = ['true', 'True', 'TRUE', True, 'yes', 'Yes', 'YES']
Config = Config_Parser.Config


class PackStackConfigurator:

    packstack_config = ConfigParser.ConfigParser(allow_no_value=True)

    def setup_packstack_pre_requisites(self):
        shell = shi.ShellInterpretter()
        shell.execute_command(
            "/usr/bin/yum-packstack_config-manager --enable rhel-7-server-openstack-5.0-rpms")

    def install_packstack(self):
        shell = shi.ShellInterpretter()
        shell.execute_command("/usr/bin/yum install -y openstack-packstack")

    def generate_answer_file(self):
        shell = shi.ShellInterpretter()
        shell.execute_command(
            "/usr/bin/packstack --gen-answer-file=packstack.cfg")
        PackStackConfigurator.packstack_config.read(r'packstack.cfg')

    def setup_packstack(self):
        shell = shi.ShellInterpretter()
        shell.execute_command(
            "/usr/bin/packstack --answer-file=packstack_result.cfg")

    # def setup_passwords(self, password):
    # def setup_passwords(self, password):

    def backup_answer_file(self):
        with open(r'packstack_backup.cfg', 'wb') as packstack_configfile:
            PackStackConfigurator.packstack_config.write(packstack_configfile)

    def enable_packstack_field(self, section, field):
        self.set_packstack_field(section, field, 'y')

    def disable_packstack_field(self, section, field):
        self.set_packstack_field(section, field, 'n')

    def set_packstack_field(self, section, field, value):
        PackStackConfigurator.packstack_config.set(section, field, value)
        with open(r'packstack_result.cfg', 'wb') as packstack_configfile:
            PackStackConfigurator.packstack_config.write(packstack_configfile)

    def get_packstack_field(self, section, field):
        return PackStackConfigurator.packstack_config.get(
            section,
            field,
            0)  # Raw parse

    def is_packstack_field(self, section, field):
        value = self.get_packstack_field(section, field)
        return (value == 'y')

    def configure_packstack(self, console):
        self.setup_packstack_pre_requisites()
        self.install_packstack()
        self.generate_answer_file()
        # For Testing, change packstack_config-rw-pw to Cisco12345
        packstack.set_packstack_field("general", "CONFIG_RH_PW", "Cisco12345")

        # Turn off swift, Turn on Heat, set CVF ntp server
        packstack.disable_packstack_field("general", "CONFIG_SWIFT_INSTALL")
        packstack.enable_packstack_field("general", "CONFIG_HEAT_INSTALL")
        packstack.set_packstack_field(
            "general",
            "CONFIG_NTP_SERVERS",
            "cvf-ntp1")

        # Move networker and compute services to proper nodes
        packstack.set_packstack_field(
            "general",
            "CONFIG_COMPUTE_HOSTS",
            Config.get_packstack_field("COMPUTE-HOSTS"))
        packstack.set_packstack_field(
            "general",
            "CONFIG_NETWORK_HOSTS",
            Config.get_packstack_field("NETWORK-HOSTS"))

        # Customers will want to set admin keystone password to something sane
        packstack.set_packstack_field(
            "general",
            "CONFIG_KEYSTONE_ADMIN_PW",
            Config.get_packstack_field("KEYSTONE-ADMIN-PW"))

        # Set oversubscription based on Karen's requirements
        packstack.set_packstack_field(
            "general",
            "CONFIG_NOVA_SCHED_CPU_ALLOC_RATIO",
            "8.0")
        packstack.set_packstack_field(
            "general",
            "CONFIG_NOVA_SCHED_RAM_ALLOC_RATIO",
            "1.0")

        # Configure neutron mechanism drivers and networking
        packstack.set_packstack_field(
            "general",
            "CONFIG_NEUTRON_ML2_TYPE_DRIVERS",
            "vlan")
        packstack.set_packstack_field(
            "general",
            "CONFIG_NEUTRON_ML2_TENANT_NETWORK_TYPES",
            "vlan")
        drivers_str = ""
        if Config.get_packstack_field("ENABLE-OPENVSWITCH") in AffirmativeList:
            drivers_str += (", " +
                            "openvswitch" if drivers_str == "" else "openvswitch")
        if Config.get_packstack_field("ENABLE-CISCONEXUS") in AffirmativeList:
            drivers_str += (", " +
                            "ciso_nexus" if drivers_str == "" else "cisconexus")
        # Any of the drivers are enabled
        if drivers_str != "":
            packstack.set_packstack_field(
                "general",
                "CONFIG_NEUTRON_ML2_MECHANISM_DRIVERS",
                drivers_str)
        packstack.set_packstack_field(
            "general",
            "CONFIG_NEUTRON_ML2_VLAN_RANGES",
            Config.get_packstack_field("VLAN-MAPPING-RANGES"))

        # Do not packstack_configure demo project/user/network
        packstack.disable_packstack_field("general", "CONFIG_PROVISION_DEMO")
        packstack.setup_packstack()


if __name__ == "__main__":
    packstack = PackStackConfigurator()
    packstack.configure_packstack(cono.ConsoleOutput())
