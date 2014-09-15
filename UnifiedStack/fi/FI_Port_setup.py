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

# FI_Port_setup.py:
# Configures server ports and uplink ports.
# Values are hardcoded for the purpose of simplicity as of now.

import UcsSdk as ucs
from FI_Configurator_Base import FIConfiguratorBase

class FIPortConfigurator(FIConfiguratorBase):
    
    # Configure Server Port
    # will take params port_id, slot_id
    def configure_server_port(self):
        handle = self.handle # Getting handle from FIConfiguratorBase
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, ucs.FabricDceSwSrv.ClassId(),
                                      {ucs.FabricDceSwSrv.DN:
                                       "fabric/server/sw-A"})
        handle.AddManagedObject(obj, ucs.FabricDceSwSrvEp.ClassId(),
                                {ucs.FabricDceSwSrvEp.ADMIN_STATE: "enabled",
                                ucs.FabricDceSwSrvEp.SLOT_ID: "1",
                                ucs.FabricDceSwSrvEp.DN:
                                 "fabric/server/sw-A/slot-1-port-15",
                                ucs.FabricDceSwSrvEp.PORT_ID: "15"})
        handle.AddManagedObject(obj, ucs.FabricDceSwSrvEp.ClassId(),
                                {ucs.FabricDceSwSrvEp.ADMIN_STATE: "enabled",
                                ucs.FabricDceSwSrvEp.SLOT_ID: "1",
                                ucs.FabricDceSwSrvEp.DN:
                                 "fabric/server/sw-A/slot-1-port-16",
                                ucs.FabricDceSwSrvEp.PORT_ID: "16"})
        handle.CompleteTransaction()

    # Configure Uplink Port
    # will take params port_id, slot_id
    def configure_uplink_port(self):
        handle = self.handle
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, None, {"dn": "fabric/lan/A"})
        handle.AddManagedObject(obj, ucs.FabricEthLanEp.ClassId(),
                                {ucs.FabricEthLanEp.DN:
                                 "fabric/lan/A/phys-slot-1-port-20",
                                ucs.FabricEthLanEp.ADMIN_SPEED: "10gbps",
                                ucs.FabricEthLanEp.SLOT_ID: "1",
                                ucs.FabricEthLanEp.ADMIN_STATE: "enabled",
                                ucs.FabricEthLanEp.PORT_ID: "20"})
        handle.CompleteTransaction()

if __name__ == '__main__':
    fi_conf = FIPortConfigurator()
    fi_conf.configure_server_port()
    fi_conf.configure_uplink_port()

