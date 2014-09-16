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

# integrator.py:
# Parser to parse config file.
# Provides any additional config details as necessary.

import sys
import os

root_path = os.path.abspath(r"..")
sys.path.append(root_path)


from UnifiedStack.cimc import CIMC_Setup as cimc
from UnifiedStack.cobbler import Cobbler_Setup as cobb
from UnifiedStack.packstack import Packstack_Setup as pst
from UnifiedStack.netswitch import Switch_Setup as sw

from UnifiedStack.cli import Console_Output as cli


class Integrator:

    def configure_unifiedstack(self):
        console = cli.ConsoleOutput()
        console.cprint_header("UnifiedStack - Installer (Beta 1.0)")

        # Configuring CIMC
        console.cprint_progress_bar("Started Configuration of CIMC", 0)
        cimc_config = cimc.CIMCConfigurator(console)
        cimc_config.configure_cimc()

        # Configuring Cobbler
        console.cprint_progress_bar("Started Installation of Cobbler", 0)
        cobbler_config = cobb.CobblerConfigurator()
        cobbler_config.configure_cobbler(console)

        # Configuring Packstack
        console.cprint_progress_bar("Started Configuration of Packstack", 0)
        packstack_config = pst.PackStackConfigurator()
        packstack_config.configure_packstack(console)

        # Configuring Switch
        console.cprint_progress_bar("Started Configuration of Switch", 0)
        sw_config = sw.SwitchConfigurator()
        sw_config.configure_switch(console)

if __name__ == "__main__":
    integrator = Integrator()
    integrator.configure_unifiedstack()
