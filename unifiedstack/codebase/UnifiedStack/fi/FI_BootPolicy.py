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

# Configures Boot Policy.
# PXE boot and local Disk storage configured.


import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase
from FI_Utils import FIUtils
class FIBootPolicy(FIConfiguratorBase):
    def configure_boot_policy(self, boot_policy_name, Vnic_name):	
        handle = self.handle
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, ucs.OrgOrg.ClassId(), {ucs.OrgOrg.DN:"org-root"})
	handle.CompleteTransaction()
        mo = FIUtils.addOrOverrideMO(obj, ucs.LsbootPolicy.ClassId(),
        {ucs.LsbootPolicy.REBOOT_ON_UPDATE:"no",
        ucs.LsbootPolicy.NAME:boot_policy_name,
        ucs.LsbootPolicy.ENFORCE_VNIC_NAME:"yes",
        ucs.LsbootPolicy.DN:"org-root/boot-policy-" + boot_policy_name ,
        ucs.LsbootPolicy.DESCR:"Boot Policy for Cobbler"})	
        mo_1 = FIUtils.addOrOverrideMO(mo, ucs.LsbootLan.ClassId(),
        {ucs.LsbootLan.DN:"org-root/boot-policy-" + boot_policy_name + "/lan",
        ucs.LsbootLan.ORDER:"1", ucs.LsbootLan.PROT:"pxe"}, True)
        mo_1_1 = FIUtils.addOrOverrideMO(mo_1, ucs.LsbootLanImagePath.ClassId(),
         {ucs.LsbootLanImagePath.DN:"org-root/boot-policy-" + boot_policy_name + "/lan/path-primary",
        ucs.LsbootLanImagePath.VNIC_NAME:Vnic_name,
        ucs.LsbootLanImagePath.TYPE:"primary"})
        mo_3 = FIUtils.addOrOverrideMO(mo, ucs.LsbootStorage.ClassId(),
        {ucs.LsbootStorage.DN:"org-root/boot-policy-" + boot_policy_name + "/storage ",
        ucs.LsbootStorage.ORDER:"2"})
        mo_3_1 = FIUtils.addOrOverrideMO(mo_3, ucs.LsbootLocalStorage.ClassId(),
        {ucs.LsbootLocalStorage.DN:"org-root/boot-policy-" + boot_policy_name + "/storage/local-storage"})
	
