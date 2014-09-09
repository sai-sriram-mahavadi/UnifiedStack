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
