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

# Configures Service Profiles.
# Adds Vlans and asscociates vlans to vnic.

import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase
from FI_Utils import FIUtils

FI_FABRIC_SERVER = "fabric/server/"
FI_FABRIC_LAN = "fabric/lan/"


class FIServiceProfileConfigurator(FIConfiguratorBase):
    
    # Create VLAN
    def add_vlan(self, vlan_id, vlan_name):
        handle = self.handle
        obj = handle.GetManagedObject(
            None, ucs.FabricLanCloud.ClassId(), {
                ucs.FabricLanCloud.DN: FI_FABRIC_LAN})
        FIUtils.addOrOverrideMO(obj, ucs.FabricVlan.ClassId(),
                                {ucs.FabricVlan.DN: FI_FABRIC_LAN + "net-" + vlan_name,
                                 ucs.FabricVlan.ID: vlan_id,
                                 ucs.FabricVlan.NAME: vlan_name})

    def associate_vlan_vnic(self, vlan_name, uuid_name, mac_name, vnic_name, service_profile_name, switch_id):
        # Create Service Profile
        handle = self.handle
        handle.StartTransaction()
        obj = handle.GetManagedObject(
            None, ucs.OrgOrg.ClassId(), {
                ucs.OrgOrg.DN: "org-root"})
        mo = FIUtils.addOrOverrideMO(obj,
                                     ucs.LsServer.ClassId(),
                                     {ucs.LsServer.NAME: service_profile_name,
                                      ucs.LsServer.UUID: "0",
                                      ucs.LsServer.IDENT_POOL_NAME: uuid_name,
                                      ucs.LsServer.DN: "org-root/ls-" + service_profile_name}, True) 
        mo_1 = FIUtils.addOrOverrideMO(mo,
                                       ucs.VnicEther.ClassId(),
                                       {ucs.VnicEther.SWITCH_ID: switch_id,
                                        ucs.VnicEther.DN: "org-root/ls-"+service_profile_name + "/ether-" + vnic_name,
                                        ucs.VnicEther.NAME: vnic_name,
                                        ucs.VnicEther.IDENT_POOL_NAME: mac_name}, True)
        mo_1_1 = FIUtils.addOrOverrideMO(
            mo_1,
            ucs.VnicEtherIf.ClassId(),
            {
                ucs.VnicEtherIf.DN: "org-root/ls-" + service_profile_name + "/ether-"+ vnic_name +
                                    "/if-" + vlan_name,
                ucs.VnicEtherIf.NAME: vlan_name,
                ucs.VnicEtherIf.DEFAULT_NET: "no"}, True) 
        handle.CompleteTransaction()

if __name__ == "__main__":
    sp_config = FIServiceProfileConfigurator()
    for i in range(1, 10):
        sp_config.add_vlan(10 + i, "test" + str(i))
    for i in range(10, 11):
        sp_config.associate_vlan_vnic("test" + str(i))
