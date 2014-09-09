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

# FI_Service_Profile_setup.py:
# Configures Service Profiles.
# Adds Vlans and asscociates vlans to vnic.

class FIServiceProfileConfigurator:
    
    # Create VLAN
    def add_vlan(self, id, name):
        handle = UcsHandle()
        handle.Login("19.19.102.10", "admin", "Cisco12345")
        handle.StartTransaction()
        obj = handle.GetManagedObject(
            None, FabricLanCloud.ClassId(), {
                FabricLanCloud.DN: "fabric/lan"})
        handle.AddManagedObject(obj, FabricVlan.ClassId(),
                                {FabricVlan.DN: "fabric/lan/net-" + name,
                                 FabricVlan.ID: id,
                                 FabricVlan.NAME: name})
        handle.CompleteTransaction()

    def associate_vlan_vnic(self, vlan_name):
        # Create Service Profile
        handle = UcsHandle()
        handle.Login("19.19.102.10", "admin", "Cisco12345")
        handle.StartTransaction()
        obj = handle.GetManagedObject(
            None, OrgOrg.ClassId(), {
                OrgOrg.DN: "org-root"})
        mo = handle.AddManagedObject(obj,
                                     LsServer.ClassId(),
                                     {LsServer.NAME: "testLS2",
                                      LsServer.UUID: "0",
                                      LsServer.IDENT_POOL_NAME: "UUID-Test",
                                      LsServer.DN: "org-root/ls-testLS2"},
                                     True)
        mo_1 = handle.AddManagedObject(mo,
                                       VnicEther.ClassId(),
                                       {VnicEther.SWITCH_ID: "A",
                                        VnicEther.DN: "org-root/ls-testLS2/ether-vnicfinanceA",
                                        VnicEther.NAME: "vnicfinanceA",
                                        VnicEther.IDENT_POOL_NAME: "MAC_A"},
                                       True)
        mo_1_1 = handle.AddManagedObject(
            mo_1,
            VnicEtherIf.ClassId(),
            {
                VnicEtherIf.DN: "org-root/ls-testLS2/ether-vnicfinanceA/if-" +
                vlan_name,
                VnicEtherIf.NAME: vlan_name,
                VnicEtherIf.DEFAULT_NET: "no"},
            True)
        mo_4 = handle.AddManagedObject(
            mo, LsBinding.ClassId(), {
                LsBinding.DN: "org-root/ls-testLS2", LsBinding.PN_DN: "sys-machine/chassis-1/blade-2"})
        handle.CompleteTransaction()

sp_config = FIServiceProfileConfigurator()
for i in range(1, 10):
    sp_config.add_vlan(10 + i, "test" + str(i))
for i in range(10, 11):
    sp_config.associate_vlan_vnic("test" + str(i))
