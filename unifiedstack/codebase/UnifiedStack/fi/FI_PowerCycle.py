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

# Configures Power Cycle



from UcsSdk import ucs
from FI_Config_Base import FIConfiguratorBase

class FIPowerCycleServer(FIConfiguratorBase):
    def power_cycle(self, service_profile_name)
        #Power Cycle Server
        handle = self.handle
        handle.StartTranscation()
        obj = handle.GetManagedObject(None, ucs.LsPower.ClassId(), {ucs.LsPower.DN:"org-root/ls-" + service_profile_name +"/power"})
        handle.SetManagedObject(obj, ucs.LsPower.ClassId(), {ucs.LsPower.STATE:"hard-reset-immediate"})
        handle.CompleteTransaction()

    
