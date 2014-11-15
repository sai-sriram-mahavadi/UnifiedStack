
import sys
import os

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.cli import Console_Output as con
from Switch_Config_Generator import SwitchConfigGenerator
from UnifiedStack.config import Config_Parser as cfg
import paramiko
# Alias for config parser
Config = cfg.Config

class SwitchConfigurator:
    # Returns SSH connection through which terminal needs to be invoked to send
    # a command and recieve it's output

    def establish_connection(self, ipaddress, username, password):
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(
            ipaddress,
            username=username,
            password=password)
        return remote_conn_pre

    # Used to configure any switch with reference to the topology provided from
    # config file.
    # TODO - Commonds file is later auto-generated and not sent as a parameter
    def configure_device_with_file(self, ip_address, username, password, commands_file):
        remote_conn_client = self.establish_connection(
            ipaddress=ip_address,
            username=username,
            password=password)
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_client.invoke_shell()
        output = remote_conn.recv(1000)
        for line in open(commands_file):
            # error check for ssh connection and send function and retry 3
            # times if fail
            success = False
            attempts = 0
            while (success == False) and (attempts < 3):
                try:
                    remote_conn.send(line)
                    time.sleep(1)
                    success = True
                except Exception as e:
                    # print "Connection is not established : " + e.strerror
                    attempts += 1
        output = remote_conn.recv(5000)

    def configure_switch(self, console):
        sw_gen = SwitchConfigGenerator()
        #sw_gen.generate_config_file("switch-3750")
        sw_gen.generate_config_file("switch-9k")
        console.cprint_progress_bar("Generated config files for switches", 10)

        """# Configuring 3750 Switch
        ip_address_3750 = Config.get_switch_field("3750-ip-address").strip()
        username_3750 = Config.get_switch_field("3750-username").strip()
        password_3750 = Config.get_switch_field("3750-password").strip()
        self.configure_device_with_file(ip_address=ip_address_3750,
                              username=username_3750,
                              password=password_3750,
                              commands_file='switch-3750_commands.cmds')
        console.cprint_progress_bar("Configured the 3750 switch", 50)
        sw_gen = SwitchConfigGenerator()"""
        # Configuring 9k Switch
        ip_address_9k = Config.get_switch_field("9k-ip-address").strip()
        username_9k = Config.get_switch_field("9k-username").strip()
        password_9k = Config.get_switch_field("9k-password").strip()
        self.configure_device_with_file(ip_address=ip_address_9k,
                              username=username_9k,
                              password=password_9k,
                              commands_file='switch-9k_commands.cmds')

        console.cprint_progress_bar("Configured the N9K switch", 100)


if __name__ == "__main__":
    sw_config = SwitchConfigurator()
    # sw_config.configure_switch(con.ConsoleOutput())
    # sw_config.establish_connection("10.106.16.253", "sdu", "1@#$sDu%^7")
