#   Copyright 2014 Aman Sinha
#   Copyright 2014 Venkata Sai Sriram Mahavadi
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

# FI_Config_Parser.py:
# Common interface to access/configure fi from outside
import ConfigParser

class FIConfig:
    config = ConfigParser.ConfigParser()
    config.read(r'..\config\unified_stack.cfg')
    @staticmethod
    def get_cluster_ipaddress():
        return FIConfig.config.get('FI-Configuration', 'fi-cluster-ip-address', 0)
    @staticmethod
    def get_cluster_username():
        return FIConfig.config.get('FI-Configuration', 'fi-cluster-username', 0)
    @staticmethod
    def get_cluster_password():
        return FIConfig.config.get('FI-Configuration', 'fi-cluster-password', 0)
if __name__ == '__main__':
    print FIConfig.get_cluster_ipaddress()
    print FIConfig.get_cluster_username()
    print FIConfig.get_cluster_password()
    
