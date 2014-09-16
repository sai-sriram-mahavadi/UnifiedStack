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

# Clones Service Profiles.


import UcsSdk

class FICloneConfigurator:
  # Cloning Service Profile
    def clone_profile(self, name):
        handle = UcsHandle()
        hasndle.Login("19.19.102.10", "admin", "Cisco12345")
        handle.StartTransaction()
        handle.LsClone(
            dn="org-root/ls-testLS1",
            inServerName=name,
            inTargetOrg="org-root",
            inHierarchical="Yes",
            dumpXml=None)
        handle.CompleteTransaction()

ficonfig = FICloneConfigurator()
for i in range(3, 9):
    ficonfig.clone_profile("testLS" + str(i))
