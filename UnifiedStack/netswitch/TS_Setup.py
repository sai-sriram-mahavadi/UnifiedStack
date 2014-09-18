#   Copyright 2014
#
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
#   Establishes an ssh session to the 2960 switch.
#   Configures the 2960 switch.

import paramiko
import time

# TODO ip, username and password will be taken from config file later.
ip = ''
username = ''
password = ''


class TSConfigurator:
    # Create instance of SSHClient object
    # Automatically add untrusted hosts (make sure okay for security policy
    # in your environment)
    # initiate SSH connection
    # Use invoke_shell to establish an 'interactive session'
    # remote_conn = remote_conn_pre.invoke_shell()

    def establish_connection(self, ipaddress, username, password):
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(
            ipaddress,
            username=username,
            password=password)
        # print "SSH connection established to %s" % ipaddress
        # print "Interactive SSH session established"
        return remote_conn_pre

    def configure_TS(self):
        # Calling the function to make the ssh connection
        remote_conn_client = self.establish_connection(
            ipaddress=ip,
            username=username,
            password=password)
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_client.invoke_shell()
        output = remote_conn.recv(1000)
        # print output
        # sending configuration commands to switch from a text file as input
        for line in open('netswitch/TS_commands.txt'):
            # error check for ssh connection and send function and retry 3
            # times if fail
            success = False
            attempts = 0
            while (success == False) and (attempts < 3):
                try:
                    remote_conn.send(line)
                    success = True
                except socket.error as e:
                    # print "Connection is not established : " + e.strerror
                    attempts += 1
        # Adding a delay to let the commands work. Add at the end of all
        # commands
        time.sleep(2)
        output = remote_conn.recv(5000)
        # Use for testing only
        # print output

if __name__ == "__main__":
    TS_config = TSConfigurator()
    TS_config.configure_TS()
