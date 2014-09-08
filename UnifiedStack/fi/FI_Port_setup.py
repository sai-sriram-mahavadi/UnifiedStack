# FI_Port_setup.py:
# Configures server ports and uplink ports.
# Values are hardcoded for the purpose of simplicity as of now.

from UcsSdk import *

class FIConfigurator:

    # Login to FI
    # will take params ip_address, username, password
    def login_fi(self):
        handle = UcsHandle()
        handle.Login("19.19.102.10", "admin", "Cisco12345")

    # Configure Server Port
    # will take params port_id, slot_id
    def configure_server_port(self):
        handle = UcsHandle()
        handle.Login("19.19.102.10", "admin", "Cisco12345")
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, FabricDceSwSrv.ClassId(),
                                      {FabricDceSwSrv.DN:
                                       "fabric/server/sw-A"})
        handle.AddManagedObject(obj, FabricDceSwSrvEp.ClassId(),
                                {FabricDceSwSrvEp.ADMIN_STATE: "enabled",
                                FabricDceSwSrvEp.SLOT_ID: "1",
                                FabricDceSwSrvEp.DN:
                                 "fabric/server/sw-A/slot-1-port-15",
                                FabricDceSwSrvEp.PORT_ID: "15"})
        handle.AddManagedObject(obj, FabricDceSwSrvEp.ClassId(),
                                {FabricDceSwSrvEp.ADMIN_STATE: "enabled",
                                FabricDceSwSrvEp.SLOT_ID: "1",
                                FabricDceSwSrvEp.DN:
                                 "fabric/server/sw-A/slot-1-port-16",
                                FabricDceSwSrvEp.PORT_ID: "16"})
        handle.CompleteTransaction()

    # Configure Uplink Port
    # will take params port_id, slot_id
    def configure_uplink_port(self):
        handle = UcsHandle()
        handle.Login("19.19.102.10", "admin", "Cisco12345")
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, None, {"dn": "fabric/lan/A"})
        handle.AddManagedObject(obj, FabricEthLanEp.ClassId(),
                                {FabricEthLanEp.DN:
                                 "fabric/lan/A/phys-slot-1-port-20",
                                FabricEthLanEp.ADMIN_SPEED: "10gbps",
                                FabricEthLanEp.SLOT_ID: "1",
                                FabricEthLanEp.ADMIN_STATE: "enabled",
                                FabricEthLanEp.PORT_ID: "20"})
        handle.CompleteTransaction()

"""
USAGE:
`````
fi_conf = FIConfigurator()
fi_conf.login_fi()
fi_conf.configure_server_port()
fi_conf.configure_uplink_port()
"""
