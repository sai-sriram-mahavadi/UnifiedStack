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



from UcsSdk import *
from codebase.UnifiedStack.fi.FI_Config_Base import FIConfiguratorBase
#from codebase.UnifiedStack.fi.FI_Config_Parser import FIConfig
from configurator import fetch_db

class FIPowerCycleServer(FIConfiguratorBase):
    def power_cycle(self):
        #Power Cycle Server
	os.environ['no_proxy']=fetch_db.FI().get('fi-cluster-ip-address')
        handle = self.handle
        handle.StartTransaction()
        for i in range(1, 9):
            obj = handle.GetManagedObject(None, LsPower.ClassId(), {LsPower.DN:"org-root/ls-" + fetch_db.FI().get('fi-service-profile-name') + str(i) +"/power"})
            handle.SetManagedObject(obj, LsPower.ClassId(), {LsPower.STATE:"hard-reset-immediate"})
        handle.CompleteTransaction()
    """
    def power_cycle(self):
	try:
	    handle = UcsHandle()
            handle.Login("19.19.102.10","admin","Cisco12345")
	    handle.StartTransaction()
	    obj = handle.GetManagedObject(None, LsPower.ClassId(), {LsPower.DN:"org-root/ls-demoLS2/power"})
	    handle.SetManagedObject(obj, LsPower.ClassId(), {LsPower.STATE:"hard-reset-immediate"})
 	    handle.CompleteTransaction()
	except exception as e:
	    print str(e)
    """
	    
    
