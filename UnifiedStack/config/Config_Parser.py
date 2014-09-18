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

# FI_Config_Parser.py:
# Parser to parse config file.
# Provides any additional config details as necessary.

import ConfigParser


class Config:
    
    config = ConfigParser.ConfigParser()
    config.read(r'../data_static/unified_stack.cfg')
    
    @staticmethod
    def get_field(section, field):
        return Config.config.get(section, field, 0)
   
    @staticmethod
    def get_fi_field(field):
        return Config.get_field("FI-Configuration", field)
    
    @staticmethod
    def get_switch_field(field):
        return Config.get_field("Switch-Configuration", field)

    @staticmethod
    def get_cimc_field(field):
        return Config.get_field("CIMC-Configuration", field)

    @staticmethod
    def get_cobbler_field(field):
        return Config.get_field("Cobbler-Configuration", field)
   
    @staticmethod
    def get_packstack_field(field):
        return Config.get_field("Packstack-Configuration", field)
    
if __name__=="__main__":
    print Config.get_cobbler_field("cobbler_ipaddress")
