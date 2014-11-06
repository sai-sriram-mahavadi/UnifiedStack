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

# Configures uuid pools and mac pools.
# Values are hardcoded for the purpose of simplicity as of now.

import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase
from FI_Utils import FIUtils

class FIPoolConfigurator(FIConfiguratorBase):
    
    # Configure UUID Pool
    def configure_uuid_pool(self, uuid_pool, uuid_start, uuid_end):
        # Getting handle from FIConfiguratorBase
        handle = self.handle 
        obj = handle.GetManagedObject(
            None, ucs.OrgOrg.ClassId(), {
                ucs.OrgOrg.DN: "org-root"})
        
        mo = FIUtils.addOrOverrideMO(obj,
                                     ucs.UuidpoolPool.ClassId(),
                                     {ucs.UuidpoolPool.NAME: uuid_pool,
                                      ucs.UuidpoolPool.PREFIX: "derived",
                                      ucs.UuidpoolPool.DN: "org-root/uuid-pool-" + uuid_pool,
                                      ucs.UuidpoolPool.ASSIGNMENT_ORDER: "sequential"})
        mo_1 = FIUtils.addOrOverrideMO(
            mo,
            ucs.UuidpoolBlock.ClassId(),
            {
                ucs.UuidpoolBlock.FROM: uuid_start,
                ucs.UuidpoolBlock.TO: uuid_end,
                ucs.UuidpoolBlock.DN: "org-root/uuid-pool-" + uuid_pool + "/block-from-" +
                                    uuid_start + "-to-" + uuid_end})

    # Configure MAC Pool
    def configure_mac_pool(self, mac_pool, mac_start, mac_end):
        handle = self.handle
        obj = handle.GetManagedObject(
            None, ucs.OrgOrg.ClassId(), {
                ucs.OrgOrg.DN: "org-root"})
        mo = FIUtils.addOrOverrideMO(obj,
                                     ucs.MacpoolPool.ClassId(),
                                     {ucs.MacpoolPool.NAME: mac_pool,
                                      ucs.MacpoolPool.DN: "org-root/mac-pool-" + mac_pool,
                                      ucs.MacpoolPool.ASSIGNMENT_ORDER: "sequential"})
        mo_1 = FIUtils.addOrOverrideMO(
            mo,
            ucs.MacpoolBlock.ClassId(),
            {
                ucs.MacpoolBlock.FROM: mac_start,
                ucs.MacpoolBlock.TO: mac_end,
                ucs.MacpoolBlock.DN: "org-root/mac-pool-"+ mac_pool + "/block-" + mac_start + "-" + mac_end})
