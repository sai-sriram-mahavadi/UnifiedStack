from UcsSdk import *
handle = UcsHandle()
handle.Login("19.19.102.10","admin","Cisco12345")


class FIPoolConfigurator:
    
    #Configure UUID Pool
    def configure_uuid_pool():
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
        mo = handle.AddManagedObject(obj, UuidpoolPool.ClassId(),
             {UuidpoolPool.NAME:"UUID-Test",
             UuidpoolPool.PREFIX:"derived",
             UuidpoolPool.DN:"org-root/uuid-pool-UUID-Test",
             UuidpoolPool.ASSIGNMENT_ORDER:"sequential"})
        mo_1 = handle.AddManagedObject(mo, UuidpoolBlock.ClassId(),
               {UuidpoolBlock.FROM:"0000-000000000001",
               UuidpoolBlock.TO:"0000-0000000003E8",
               UuidpoolBlock.DN:
               "org-root/uuid-pool-UUID-Test/block-from-0000-000000000001-to-0000-0000000003E8"})
        handle.CompleteTransaction()

    #Configure MAC Pool
    def configure_mac_pool():
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
        mo = handle.AddManagedObject(obj, MacpoolPool.ClassId(),
             {MacpoolPool.NAME:"MAC_A",
             MacpoolPool.DN:"org-root/mac-pool-MAC_A",
             MacpoolPool.ASSIGNMENT_ORDER:"sequential"})
        mo_1 = handle.AddManagedObject(mo, MacpoolBlock.ClassId(),
               {MacpoolBlock.FROM:"00:25:B5:6A:00:00",
               MacpoolBlock.TO:"00:25:B5:6A:03:E7",
               MacpoolBlock.DN:"org-root/mac-pool-MAC_A/block-00:25:B5:6A:00:00-00:25:B5:6A:03:E7"})
        handle.CompleteTransaction()

#Create VLAN
def Vlan(id,name):
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, FabricLanCloud.ClassId(), {FabricLanCloud.DN:"fabric/lan"})
    handle.AddManagedObject(obj, FabricVlan.ClassId(),
    {FabricVlan.DN:"fabric/lan/net-" + name,
    FabricVlan.ID:id,
    FabricVlan.NAME:name})
    handle.CompleteTransaction()

for i in range(1,10):
    Vlan(10+i, "test"+str(i))

def associate_vlan_vnic(vlan_name):
    #Create Service Profile
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
    mo = handle.AddManagedObject(obj, LsServer.ClassId(), {LsServer.NAME:"testLS2", LsServer.UUID:"0", LsServer.IDENT_POOL_NAME:"UUID-Test", LsServer.DN:"org-root/ls-testLS2"}, True)
    mo_1 = handle.AddManagedObject(mo, VnicEther.ClassId(), {VnicEther.SWITCH_ID:"A", VnicEther.DN:"org-root/ls-testLS2/ether-vnicfinanceA", VnicEther.NAME:"vnicfinanceA", VnicEther.IDENT_POOL_NAME:"MAC_A"}, True)
    mo_1_1 = handle.AddManagedObject(mo_1, VnicEtherIf.ClassId(), {VnicEtherIf.DN:"org-root/ls-testLS2/ether-vnicfinanceA/if-"+vlan_name, VnicEtherIf.NAME:vlan_name, VnicEtherIf.DEFAULT_NET:"no"}, True)
    mo_4 = handle.AddManagedObject(mo, LsBinding.ClassId(), {LsBinding.DN:"org-root/ls-testLS2", LsBinding.PN_DN:"sys-machine/chassis-1/blade-2"})
    handle.CompleteTransaction()

for i in range(10,11):
    associate_vlan_vnic("test" + str(i))




