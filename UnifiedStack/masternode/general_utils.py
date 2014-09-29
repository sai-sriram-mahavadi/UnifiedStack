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


#!/bin/python


####### General Utils #########
import subprocess
import os
import sys
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)
from UnifiedStack.cli import Shell_Interpretter as shi

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def shell_command_true(fully_qualified_command):
    shell=shi.ShellInterpretter()
    shell.execute_command(fully_qualified_command)


def shell_command(command_title, command_args):
    subprocess.call()


def shell_command(fully_qualified_command):
    shell=shi.ShellInterpretter()
    shell.execute_command(fully_qualified_command)


def split_into_words(var):
    var = var.strip(' ')
    partitioned_list = var.partition(' ')
    left_part = partitioned_list[0]
    right_part = partitioned_list[2]
    words_list = []
    while right_part != '':
        words_list.append(left_part)
        var = right_part
        var = var.strip(' ')
        partitioned_list = var.partition(' ')
        left_part = partitioned_list[0]
        right_part = partitioned_list[2]
    words_list.append(left_part)
    return words_list


def is_basestring(var):
    if isinstance(var, basestring):
        return True
    else:
        return False
