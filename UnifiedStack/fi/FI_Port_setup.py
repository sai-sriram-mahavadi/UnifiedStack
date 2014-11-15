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

# Configures server ports and uplink ports.
# Values are hardcoded for the purpose of simplicity as of now.

import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase
from FI_Utils import FIUtils

FI_FABRIC_SERVER = "fabric/server/"
FI_FABRIC_LAN = "fabric/lan/"
# sw-A, 
class FIPortConfigurator(FIConfiguratorBase):
    
    # Configure Server Port
    # will take params port_id, slot_id
    def configure_server_port(self, server_port, switch, slot_id):
        # Getting handle from FIConfiguratorBase
        handle = self.handle 
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, ucs.FabricDceSwSrv.ClassId(),
                                      {ucs.FabricDceSwSrv.DN:
                                       FI_FABRIC_SERVER + switch})
        handle.CompleteTransaction()
        FIUtils.addOrIgnoreMO(obj, ucs.FabricDceSwSrvEp.ClassId(),
                                {ucs.FabricDceSwSrvEp.ADMIN_STATE: "enabled",
                                ucs.FabricDceSwSrvEp.SLOT_ID: slot_id,
                                ucs.FabricDceSwSrvEp.DN:
                                 FI_FABRIC_SERVER + switch + "/slot-"+
                                 slot_id + "-port-" + server_port,
                                ucs.FabricDceSwSrvEp.PORT_ID: server_port})

    # Configure Uplink Port
    # will take params port_id, slot_id
    def configure_uplink_port(self, uplink_port, switch, slot_id):
        handle = self.handle
        obj = handle.GetManagedObject(None, None, {"dn": "fabric/lan/A"})
        FIUtils.addOrIgnoreMO(obj, ucs.FabricEthLanEp.ClassId(),
                                {ucs.FabricEthLanEp.DN:
                                 FI_FABRIC_LAN + "phys-slot-" + slot_id +
                                 "-port-" + uplink_port,
                                ucs.FabricEthLanEp.ADMIN_SPEED: "10gbps",
                                ucs.FabricEthLanEp.SLOT_ID: slot_id,
                                ucs.FabricEthLanEp.ADMIN_STATE: "enabled",
                                ucs.FabricEthLanEp.PORT_ID: uplink_port})

if __name__ == '__main__':
    fi_conf = FIPortConfigurator()
    fi_conf.configure_server_port()
    fi_conf.configure_uplink_port()

