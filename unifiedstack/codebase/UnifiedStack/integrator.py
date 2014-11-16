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

# Integrates all the modules to install all modules together
# Final interface to install unifiedstack

import sys
import os
import inspect
import time

root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

# Hardcoded Values
username = "root"
password = "Cisco12345"
MAX_TRIES = 5

#from UnifiedStack.cimc import CIMC_Setup as cimc
from codebase.UnifiedStack.masternode import cobbler_integrator as cobb
from codebase.UnifiedStack.packstack import Packstack_Setup as pst
from codebase.UnifiedStack.cli import Shell_Interpretter as shi
from codebase.UnifiedStack.cli import Console_Output as cli
from codebase.UnifiedStack.config import Config_Parser
from codebase.UnifiedStack.fi import FI_Configurator
# To Add
#name, purpose(networker, compute), os -> name of system
#system, rhel img (access.redhat)(http server), hostname port

Config = Config_Parser.Config


class Integrator:
    
    @staticmethod
    def get_cobbler_integrator_command():
        integrator_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return 'bash -c "cd ' + integrator_path + ' && /usr/bin/python ' + integrator_path + '/integrator.py -switch"'
         
    def configure_cobbler_preboot(self, shell, console):
        cobbler_config = cobb.Cobbler_Integrator()
        cobbler_config.cobbler_preInstall_adapter(console)
        #Write the path of integrator.py in .bashrc
        read_bash = open("/root/.bashrc", "a")
        integrator_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        read_bash.write(Integrator.get_cobbler_integrator_command())
        # read_bash.write('bash -c "cd ' + integrator_path + ' && /usr/bin/python ' + integrator_path + '/integrator.py -cobbler-postboot"')
        read_bash.close()
        shell.execute_command("reboot")
        
    def configure_cobbler_postboot(self, shell, console):
        cobbler_config = cobb.Cobbler_Integrator()
        cobbler_config.cobbler_postInstall_adapter(console)
        read_bash = open("/root/.bashrc","r")
        lines = read_bash.readlines()
        read_bash.close()
        write_bash = open("/root/.bashrc","w")
        for line in lines:
             if line!=Integrator.get_cobbler_integrator_command()+"\n":
                write_bash.write(line)
        # write_bash.writelines([item for item in lines[:-1]])
        write_bash.close()
        
    def configure_packstack(self, shell, console):
        packstack_config = pst.PackStackConfigurator()
        packstack_config.configure_packstack(console)
        
    def configure_switch(self, shell, console):
        from codebase.UnifiedStack.netswitch import Switch_Setup as sw
        sw_config = sw.SwitchConfigurator()
        sw_config.configure_switch(console)
        
    def configure_unifiedstack(self):
        console = cli.ConsoleOutput()
        shi.ShellInterpretter.set_console(console)
        shell = shi.ShellInterpretter()

        console.cprint_header("UnifiedStack - Installer (Beta 1.0)")       
        #runstatusmsg = "-cobbler-preboot" if len(sys.argv)==1 else sys.argv[1]
        #RUNSTATUSCODE = {"-cobbler-preboot":0, "-fi": 1, "-switch": 2, "-cobbler-postboot":3,  "-packstack":4}
        #try:
        #    runstatus = RUNSTATUSCODE[runstatusmsg]
        #except Exception:
        #    print "Give appropriate arguments within [ -cobbler-preboot, -cobbler-postboot, -fi, -switch, -packstack ]"
        
        #if(runstatus <= 0):  # Configuring Cobbler pre-boot
        #    console.cprint_progress_bar("Started Installation of Cobbler-Preboot", 0)
        #    self.configure_cobbler_preboot(shell, console)
        #if(runstatus <= 1):
        
	ficonfig = FI_Configurator.FIConfigurator()
        ficonfig.configure_fi_components() 
        
        shell.execute_command("yum install python-devel python-paramiko -y")
        import paramiko
        console.cprint_progress_bar("Started Configuration of Switch", 0)
        self.configure_switch(shell, console)
       
        console.cprint_progress_bar("Started Installation of Cobbler-Postboot", 0)
        cobbler_config = cobb.Cobbler_Integrator()
        cobbler_config.cobbler_postInstall_adapter(console) 
        tries = 0
        while not self.poll_all_nodes():
            time.sleep(120)
            if tries < MAX_TRIES:
                tries += 1
            else:
                break
        if not self.poll_all_nodes():
            console.cprint("Not all systems could boot!!!")
            exit(0)
        self.configure_nodes(console)
        console.cprint_progress_bar("Started Configuration of Packstack", 0)
        self.configure_packstack(shell, console)
        
        '''           
        # Configuring CIMC
        console.cprint_progress_bar("Started Configuration of CIMC", 0)
        cimc_config = cimc.CIMCConfigurator(console)
        cimc_config.configure_cimc()
        '''

    def establish_connection(self, ipaddress, username, password):
        import paramiko
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(
            ipaddress,
            username=username,
            password=password)
        # print "SSH connection established to %s" % ipaddress
        # print "Interactive SSH session established"
        return remote_conn_pre
    
    def configure_nodes(self, console):
        self.setup_ssh_key()
        for system in Config.get_systems_data():
            # Calling the function to make the ssh co
            self.ssh_key_exchange(system.ip_address, username, password)
            remote_conn_client = self.establish_connection(
                        ipaddress=system.ip_address,
                        username=username,
                        password=password)
            
            remote_conn = remote_conn_client.invoke_shell()
            redhat_username = Config.get_cobbler_field('redhat_username') 
            redhat_password = Config.get_cobbler_field('redhat_password')   
            redhat_pool = Config.get_cobbler_field('redhat_pool')
            remote_conn.send(
                "subscription-manager register --username=" +
                redhat_username +
                " --password=" +
                redhat_password)
            time.sleep(30)
            console.cprint("Subscribed a node.")
            remote_conn.send("subscription-manager attach --pool=" + redhat_pool)
            time.sleep(30)
            console.cprint("Attached pool")
          
            time.sleep(30)
            remote_conn.send(
                "sudo yum-config-manager --enable rhel-7-server-openstack-5.0-rpms")
            time.sleep(10)
            output = remote_conn.recv(5000)
            console.cprint(output)

    def poll_node(self, ipaddress, username, password):
        import paramiko
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            remote_conn_pre.connect(
            ipaddress,
            username=username,
            password=password)
        except Exception :
            return False
        except Exception:
            return False
        return True
    
    def poll_all_nodes(self):
        overall_poll_result = True        
        for system in Config.get_systems_data():
            # Calling the function to make the ssh connection
            result = self.establish_connection(
                                ipaddress=system.ip_address,
                                username=username,
                                password=password)
            overall_poll_result = overall_poll_result and result
            return overall_poll_result
        
    def test_poll(self):
        count = 0
        while not self.poll_all_nodes():
            time.sleep(120)
            if count < MAX_TRIES:
                count += 1
            else:
                break
        if self.poll_all_nodes(): pass
                # Successful
        else: pass
                # UnSuccessful
  
    def setup_ssh_key(self):
	#shell_command("wget https://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz -O /root/pip_tar_file.tar.gz")
	#shell_command("tar -zxvf /root/pip_tar_file.tar.gz -C /root/")
	#shell_command("pushd /root/pip-1.2.1; python setup.py install; popd")
	shell_command("pip install pysftp")
	shell_command('ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa')

    def ssh_key_exchange(self,host,username,password):
	import pysftp
	conObj=pysftp.Connection(host,port=22,username=username,password=password)
	conObj.execute("mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys")
	conObj.put("/root/.ssh/id_rsa.pub","/root/.ssh/authorized_keys")
	conObj.close()
	shell_command("ssh -o StrictHostKeyChecking=no " + username + "@" + host + "echo")	
	
	
        
def shell_command(fully_qualified_command):
    shell=shi.ShellInterpretter()
    shell.execute_command(fully_qualified_command)

if __name__ == "__main__":
    integrator = Integrator()
    integrator.configure_unifiedstack()
    integrator.test_poll()  
   

