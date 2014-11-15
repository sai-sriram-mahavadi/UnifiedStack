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


import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase
# options should include dn
class FIUtils(FIConfiguratorBase):
    @staticmethod
    def addOrOverrideMO(parentObj, classId, options, modifyPresent=False):
        objRsp = None
        handle = FIConfiguratorBase.handle
        try:
            handle.StartTransaction()
            objRsp = handle.AddManagedObject(parentObj, classId, options, modifyPresent)
            handle.CompleteTransaction()
            return objRsp
        except Exception:
            handle.StartTransaction()
            print "Obj to remove... ", objRsp
            for fields in objRsp:
                print fields
            handle.RemoveManagedObject(objRsp)

            print "Overriding existing configuration..."
            handle.CompleteTransaction()
            return FIUtils.addOrOverrideMO(parentObj, classId, options, modifyPresent)

    @staticmethod
    def addOrIgnoreMO(parentObj, classId, options, modifyPresent=False):
        objRsp = None
        handle = FIConfiguratorBase.handle
        try:
            handle.StartTransaction()
            objRsp = handle.AddManagedObject(parentObj, classId, options, modifyPresent)
            handle.CompleteTransaction()
        except Exception:
            print "Existing configuration is taken..."

