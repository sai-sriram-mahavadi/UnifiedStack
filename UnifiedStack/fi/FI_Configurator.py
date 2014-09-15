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

# FI_Configurator.py:
# Common interface to access/configure fi from outside

from FI_Port_Setup import FIPortConfigurator


class FIConfigurator:
    def configure_fi_components(self):
        # Configuring Server and Uplink ports
        port_config = FIPortConfigurator()
        port_config.configure_server_port()
        port_config.configure_uplink_port()

ficonfig = FIConfigurator()
ficonfig.configure_fi_components()
    
