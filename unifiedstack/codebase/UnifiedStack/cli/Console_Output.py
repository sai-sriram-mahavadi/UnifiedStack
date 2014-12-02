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

# General Utils useful for the purpose of simple
# development of code and presentation of output.
# Presently supported over all *nix systems.

import sys
import time

# Presentation Section: Colorful presentation of output
class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# Conosole Output
class ConsoleOutput:

    def __init__(self):
        self.ISPROGRESSBAR = False
        # Storing progress messages refreshing purpose
        self.PROGRESS_MESSAGE = ""
        self.PROGRESS_PERCENTAGE = 0

    def erase_above_line(self):
        CURSOR_FRONT_COLUMN = '\r'
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        sys.stdout.write(CURSOR_FRONT_COLUMN + CURSOR_UP_ONE + ERASE_LINE)
        sys.stdout.flush()

    def simple_print(self, message):
        if self.ISPROGRESSBAR: 
            # Erasing previous progress
            self.erase_above_line()
        print message
        if self.ISPROGRESSBAR:
            print ""  # To Adjust Automatic clear from progress bar update
            self.cprint_progress_bar(self.PROGRESS_MESSAGE,
                                     self.PROGRESS_PERCENTAGE)

    def cprint_error(self, message):
        self.simple_print(PrintColors.FAIL + message + PrintColors.ENDC)

    def cprint_success(self, message):
        self.simple_print(PrintColors.OKBLUE + message + PrintColors.ENDC)

    def cprint(self, message):
        self.simple_print(message)

    def cprint_header(self, message):
        self.simple_print(PrintColors.HEADER + message + PrintColors.ENDC)
        self.simple_print("`" * len(message))

    def cprint_progress_bar(self, message, percentage):
        if not self.ISPROGRESSBAR:
            self.ISPROGRESSBAR = True
        else:
            self.erase_above_line()
        status_marks = 50
        progress_marks = percentage * status_marks / 100
        b = "[" + "=" * progress_marks
        # Number of '=' denotes the status of event
        b += ">" + " " * (status_marks - progress_marks) + " | "\
            + str(percentage) + "%]"
        b += message + "\r\n"
        self.PROGRESS_MESSAGE = message
        self.PROGRESS_PERCENTAGE = percentage
        sys.stdout.write( b )
        sys.stdout.flush()
        
    def flush(self):
        sys.stdout.flush()
if __name__ == '__main__':
    # Testing Console
    console = ConsoleOutput()
    console.cprint_header("UnifiedStack - Installer")
    time.sleep(1)
    console.cprint_progress_bar("System Config Validation in progress", 5)
    time.sleep(2)
    console.simple_print("Config Validation Complete")
    console.cprint_progress_bar("Cobbler Installation in progress", 20)
    time.sleep(2)
    console.simple_print("Cobbler Installation Complete")
    console.cprint_progress_bar("FI Configuratio in progress", 40)
    time.sleep(2)
    console.cprint_error("FI Configuration Failed")
    console.cprint_progress_bar("Switches Configuration in progress", 50)
    time.sleep(1)
    console.cprint_success("Switch Configuration Succesfully finished")
    console.cprint_progress_bar("Finalizing Setup", 80)
    time.sleep(1)
    console.simple_print("Setup Completed")
    console.cprint_progress_bar("Setup Completed Successfully", 100)

