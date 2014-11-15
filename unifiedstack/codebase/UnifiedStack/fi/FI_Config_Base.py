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

# Base/Super class to all the FIConfiguration kind of classes
# Maintains the common resources necessary for Configuration objects
# such as login handle, etc.

import UcsSdk as ucs

class FIConfiguratorBase:
   
    # Handle used to login and access FI
    handle = ucs.UcsHandle()
    handle.Login("192.168.131.65", "satroutr", "S6T8UB1i")
    
    @staticmethod
    def login(fi_ip, username, password):
        handle.Login(fi_ip, username, password)
        
    @staticmethod
    def get_handle():
        return handle
    
    # Any methods/attributes used commonly accross all the 
    # FIConfigurator classes need to be here.
