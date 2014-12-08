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
from codebase.UnifiedStack.masternode import foreman_integrator as fore
from codebase.UnifiedStack.packstack import Packstack_Setup as pst
from codebase.UnifiedStack.cli import Shell_Interpretter as shi
from codebase.UnifiedStack.cli import Console_Output as cli
from codebase.UnifiedStack.config import Config_Parser
from configurator import fetch_db
os.environ['no_proxy']=fetch_db.FI().get("fi-cluster-ip-address")
from configurator.models import Device, DeviceSetting, DeviceTypeSetting
from codebase.UnifiedStack.fi import FI_Configurator
from logger.models import ConsoleLog
Config = Config_Parser.Config

class BackEndMessenger:
    def __init__(self):
        import zmq
        import random
        self.port = "5556"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://localhost:%s" % self.port)

    def send_message(self,msg):
        self.socket.send(msg)



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
        
    def configure_packstack(self, console,compute_host_ip_list,network_host_ip_list,controller_host_ip):	
        packstack_config = pst.PackStackConfigurator()
        packstack_config.configure_packstack(console,compute_host_ip_list,network_host_ip_list,controller_host_ip)
        
    def configure_switch(self, shell, console):	
        from codebase.UnifiedStack.netswitch import Switch_Setup as sw	
        sw_config = sw.SwitchConfigurator()
        sw_config.configure_switch(console)
        
    def configure_unifiedstack(self):
	cobbler_device_list = [] #Device.objects.filter(dtype=DeviceTypeSetting.COBBLER_TYPE)
	if len(cobbler_device_list) != 0:
            system_list=fetch_db.Cobbler().get('systems')
            redhat_username=fetch_db.Cobbler().get('redhat-username')
            redhat_password=fetch_db.Cobbler().get('redhat-password')
            redhat_pool=fetch_db.Cobbler().get('redhat-pool')
            compute_host_ip_list=fetch_db.Cobbler().get_compute_hosts_ip()
            network_host_ip_list=fetch_db.Cobbler().get_network_hosts_ip()
            controller_host_ip=fetch_db.Cobbler().get_controller_host_ip()
	    os.environ['http_proxy']="http://" + fetch_db.Cobbler().get('http-proxy-ip') + ":80"
	    os.environ['https_proxy']="https://" + fetch_db.Cobbler().get('https-proxy-ip') + ":" + fetch_db.Cobbler().get('https-port') 
        else:
            system_list=fetch_db.Foreman().get('systems')
            redhat_username=fetch_db.Foreman().get('redhat-username')
            redhat_password=fetch_db.Foreman().get('redhat-password')
            redhat_pool=fetch_db.Foreman().get('redhat-pool')
            compute_host_ip_list=fetch_db.Foreman().get_compute_hosts_ip()
            network_host_ip_list=fetch_db.Foreman().get_network_hosts_ip()
            controller_host_ip=fetch_db.Foreman().get_controller_host_ip()
	    os.environ['http_proxy']="http://" + fetch_db.Foreman().get('http-proxy-ip') + ":80"
            os.environ['https_proxy']="https://" + fetch_db.Foreman().get('https-proxy-ip') + ":" + fetch_db.Cobbler().get('https-port')
   
        console = cli.ConsoleOutput()
        shi.ShellInterpretter.set_console(console)
        shell = shi.ShellInterpretter()
        console.cprint_header("UnifiedStack - Installer (Beta 1.0)")      	
	#FI
	"""
	proxy=True
	if proxy:
	    os.environ['no_proxy']=fetch_db.FI().get("fi-cluster-ip-address")
	
	ficonfig = FI_Configurator.FIConfigurator()
        ficonfig.configure_fi_components()
	#SWITCH
        shell.execute_command("yum install python-devel python-paramiko -y")
        import paramiko
        console.cprint_progress_bar("Started Configuration of Switch", 0)
        self.configure_switch(shell, console)
	#LIFE_CYCLE
	isCobbler=False
        #Tell the cobbler and Foreman object whether to read the object from databse or from config
        if isCobbler==True:
	    cobbler_config = cobb.Cobbler_Integrator(console,data_source="database")
            cobbler_config.cobbler_postInstall_adapter() 
        else:
	    foreman_config = fore.Foreman_Integrator(console,data_source="database")
	    foreman_config.setup_foreman() 
	
        #PACKSTACK
	
	tries = 0
	#cobbler_device_list = Device.objects.filter(dtype=DeviceTypeSetting.COBBLER_TYPE)
        while not self.poll_all_nodes(system_list): 
            time.sleep(10)
            if tries < MAX_TRIES:
                tries += 1
            else:
                break
        if not self.poll_all_nodes(system_list):
            console.cprint("Not all systems could boot!!!")
            exit(0)	
	"""
        #self.configure_nodes(console,system_list,redhat_username,redhat_password,redhat_pool)
	
	console.cprint_progress_bar("Started Configuration of Packstack", 0)
        self.configure_packstack(console,compute_host_ip_list,network_host_ip_list,controller_host_ip)	
	# Configuring CIMC
	"""
        console.cprint_progress_bar("Started Configuration of CIMC", 0)
        cimc_config = cimc.CIMCConfigurator(console)
        cimc_config.configure_cimc()
        """
    def console_output(self, msg):
        ConsoleLog(console_summary=msg).save()
    def get_output(self):
	print "Started at get_output"
	self.console_output("Software pre installation phase completed")
	self.console_output("FI Configuration Started")
	time.sleep(3)
	self.console_output("FI Port Setup completed")
	time.sleep(2)
	self.console_output("FI Pools Setup completed")
	time.sleep(2)
	self.console_output("FI Service Profiles created")
        time.sleep(3)
	self.console_output("FI Service Profile associated")
        time.sleep(1)
	self.console_output("FI Console IP assigned")
        time.sleep(10)
	self.console_output("Switch Configuration started")
        time.sleep(2)
	self.console_output("Switch Config files generated")
        time.sleep(4)
	self.console_output("Switch 9K configured")
        time.sleep(2)
	self.console_output("Cobbler Postboot installation started")
        time.sleep(3)
        self.console_output("Cobbler distro created")
        time.sleep(2)
        self.console_output("Cobbler Profile created")
        time.sleep(1)
        self.console_output("Cobbler system created")
        time.sleep(10)
        self.console_output("Packstack setup started")
        time.sleep(2)
        self.console_output("Packstack answer file generated")
        time.sleep(2)
        self.console_output("Openstack configured")
        time.sleep(2)

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
    
    def configure_nodes(self, console,system_list,redhat_username,redhat_password,redhat_pool):
	self.setup_ssh_key()	
	self.ssh_key_exchange(fetch_db.General().get('host-ip-address'), 'root',fetch_db.General().get('host-password'))
	cobbler_device_list = Device.objects.filter(dtype=DeviceTypeSetting.COBBLER_TYPE)
        for system in system_list:
            # Calling the function to make the ssh connection
            self.ssh_key_exchange(system.ip_address, username, password)
            remote_conn_client = self.establish_connection(
                        ipaddress=system.ip_address,
                        username=username,
                        password=password)
	    remote_conn = remote_conn_client.invoke_shell()
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
    
    def poll_all_nodes(self,system_list):
	global username
	global password
        overall_poll_result = True      
        for system in system_list:
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
	shell_command("pip install pysftp")
	if os.path.isfile('/root/.ssh/id_rsa') and  os.path.getsize('/root/.ssh/id_rsa')!=0:
	    return
	shell_command('ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa')
    
    def ssh_key_exchange(self,host,username,password):
	import pysftp
	conObj=pysftp.Connection(host,port=22,username=username,password=password)
	conObj.execute("mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys")
	conObj.put("/root/.ssh/id_rsa.pub","/root/.ssh/authorized_keys")
	conObj.close()
	shell_command("ssh -o StrictHostKeyChecking=no " + username + "@" + host + " echo")	
 	
def shell_command(string):
    console = cli.ConsoleOutput()
    shi.ShellInterpretter.set_console(console)
    shell = shi.ShellInterpretter()
    shell.execute_command(string)
        

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unifiedstack.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
    from configurator.models import Device, DeviceTypeSetting, DeviceSetting
    from configurator import fetch_db
    integrator = Integrator()  
    integrator.configure_unifiedstack()
    integrator.test_poll()  

