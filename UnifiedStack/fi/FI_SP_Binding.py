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

# Binding the service profiles with servers (compute blades)

import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase
from FI_Utils import FIUtils


class FIBindingConfigurator(FIConfiguratorBase):

    def configure_bindings(self, service_profile, bladeDn):
        handle = self.handle
        handle.StartTransaction()
        orgObj = handle.GetManagedObject(None, ucs.OrgOrg.ClassId(),
                                         {ucs.OrgOrg.DN: "org-root"})
        lsServerObj = handle.GetManagedObject(
            orgObj, ucs.LsServer.ClassId(), {
                ucs.LsServer.NAME: service_profile})
        lsServerObj = handle.SetManagedObject(
            lsServerObj, ucs.LsServer.ClassId(), {
                ucs.LsServer.STATUS: ucs.Status.MODIFIED})
        lsBindObj = FIUtils.addOrIgnoreMO(lsServerObj,
                                            ucs.LsBinding.ClassId(),
                                            {ucs.LsBinding.PN_DN: bladeDn,
                                             ucs.LsBinding.RESTRICT_MIGRATION: ucs.YesOrNo.NO},
                                            ucs.YesOrNo.TRUE)
        handle.CompleteTransaction()
        
if __name__ == "__main__":
    ficonfig = FIBindingConfigurator()
    for i in range(1, 9):
        p_service_profile = "testLS" + str(i)
        p_bladeDn = "sys/chassis-1/blade-" + str(i)
        ficonfig.configure_bindings(
            service_profile=p_service_profile,
            bladeDn=p_bladeDn)
        print "Completed - " + str(i)
