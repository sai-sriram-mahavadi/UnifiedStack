# Copyright 2014 Prakash Kumar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#!/bin/sh
# exec /share/vim/vim74/vim "$@"

####### General Utils #########
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def shell_command(command_title, command_args):
    subprocess.call()


def shell_command(fully_qualified_command):
    print bcolors.OKBLUE + "COMMAND: " + fully_qualified_command + bcolors.ENDC
    subprocess.call(fully_qualified_command, shell=True)
~
