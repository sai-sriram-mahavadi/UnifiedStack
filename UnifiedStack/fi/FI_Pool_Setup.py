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

# FI_Pool_setup.py:
# Configures uuid pools and mac pools.
# Values are hardcoded for the purpose of simplicity as of now.

import UcsSdk
handle = UcsHandle()
handle.Login("19.19.102.10", "admin", "Cisco12345")


class FIPoolConfigurator:

    # Configure UUID Pool
    def configure_uuid_pool(self):
        handle.StartTransaction()
        obj = handle.GetManagedObject(
            None, OrgOrg.ClassId(), {
                OrgOrg.DN: "org-root"})
        mo = handle.AddManagedObject(obj,
                                     UuidpoolPool.ClassId(),
                                     {UuidpoolPool.NAME: "UUID-Test",
                                      UuidpoolPool.PREFIX: "derived",
                                      UuidpoolPool.DN: "org-root/uuid-pool-UUID-Test",
                                      UuidpoolPool.ASSIGNMENT_ORDER: "sequential"})
        mo_1 = handle.AddManagedObject(
            mo,
            UuidpoolBlock.ClassId(),
            {
                UuidpoolBlock.FROM: "0000-000000000001",
                UuidpoolBlock.TO: "0000-0000000003E8",
                UuidpoolBlock.DN: "org-root/uuid-pool-UUID-Test/block-from-0000-000000000001-to-0000-0000000003E8"})
        handle.CompleteTransaction()

    # Configure MAC Pool
    def configure_mac_pool(self):
        handle.StartTransaction()
        obj = handle.GetManagedObject(
            None, OrgOrg.ClassId(), {
                OrgOrg.DN: "org-root"})
        mo = handle.AddManagedObject(obj,
                                     MacpoolPool.ClassId(),
                                     {MacpoolPool.NAME: "MAC_A",
                                      MacpoolPool.DN: "org-root/mac-pool-MAC_A",
                                      MacpoolPool.ASSIGNMENT_ORDER: "sequential"})
        mo_1 = handle.AddManagedObject(
            mo,
            MacpoolBlock.ClassId(),
            {
                MacpoolBlock.FROM: "00:25:B5:6A:00:00",
                MacpoolBlock.TO: "00:25:B5:6A:03:E7",
                MacpoolBlock.DN: "org-root/mac-pool-MAC_A/block-00:25:B5:6A:00:00-00:25:B5:6A:03:E7"})
        handle.CompleteTransaction()
