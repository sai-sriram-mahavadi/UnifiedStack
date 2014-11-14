import UcsSdk as ucs
FI_FABRIC_SERVER = "fabric/server/"
FI_FABRIC_LAN = "fabric/lan/"
switch = "sw-A"
server_port = "15"
slot_id = "1"

# Handle used to login and access FI
handle = ucs.UcsHandle()
handle.Login("19.19.102.10", "admin", "Cisco12345")
handle.StartTransaction()
obj = handle.GetManagedObject(None, ucs.FabricDceSwSrv.ClassId(),
                                      {ucs.FabricDceSwSrv.DN:
                                       FI_FABRIC_SERVER + switch})
obj1=handle.AddManagedObject(obj, ucs.FabricDceSwSrvEp.ClassId(),
                                {ucs.FabricDceSwSrvEp.ADMIN_STATE: "disabled",
                                ucs.FabricDceSwSrvEp.SLOT_ID: "1",
                                ucs.FabricDceSwSrvEp.DN:
                                 FI_FABRIC_SERVER + switch + "/slot-"+
                                 slot_id + "-port-" + server_port,
                                ucs.FabricDceSwSrvEp.PORT_ID: server_port})
handle.CompleteTransaction()

    
