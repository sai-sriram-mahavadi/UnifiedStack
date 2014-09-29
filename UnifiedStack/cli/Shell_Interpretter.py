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

# executes shell commands and prints it's output

import subprocess
from subprocess import Popen, PIPE
from Console_Output import ConsoleOutput


class ShellInterpretter:
    console = ConsoleOutput()
    
    @staticmethod
    def set_console(console):
        console.flush()
        ShellInterpretter.console = console

    def execute_command(self, fully_qualified_command):
        # command_list = fully_qualified_command.split()
        ShellInterpretter.console.cprint("COMMAND: " + fully_qualified_command)
        with open(r'log/unified_stack.log', 'a') as output:
            cmd = Popen(fully_qualified_command, stdout=PIPE, shell=True)
            output.write("[Command]: " + fully_qualified_command + "\r\n")
            text = cmd.communicate()[0]
            output.write(text)

if __name__ == "__main__":
    shi = ShellInterpretter()
    shi.execute_command("echo fun")
    shi.execute_command("echo fun")
    shi.execute_command("echo fun")
