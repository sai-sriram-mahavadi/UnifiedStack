import cobbler_preInstall
import cobbler_setup
import os,inspect
import sys,time
import shutil
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config.Config_Parser import Config
from general_utils import shell_command

class Cobbler_Integrator():

    def __init__(self):
        self.cur=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))       

    def cobbler_preInstall(self,console): 
        shutil.copyfile(
            self.cur +
            "/../data_static/cobbler.repo",
            "/etc/yum.repos.d/cobbler.repo")
        cobbler_preInstall.enable_repos(console)
        cobbler_preInstall.disable_SELinux(console)
        #cobbler_preInstall.enable_networking(console)
        #cobbler_preInstall.add_name_server(console)

    def cobbler_postInstall(self,console):
        cobbler_setup.cobbler_setup(console)
        cobbler_setup.enable_services(console)
        shutil.copyfile(
            self.cur +
            "/../data_static/rsync",
            "/etc/xinetd.d/rsync")
        cobbler_setup.sync(console)
        cobbler_setup.mount(console)
        towrite = []
        file = open(self.cur+ "/../data_static/rhe7-osp5.ks", "r")
        lines = file.readlines()
        file.close()
        towrite = []
        redhat_username = Config.get_cobbler_field("redhat_username")
        redhat_password = Config.get_cobbler_field("redhat_password")
        redhat_pool = Config.get_cobbler_field("redhat_pool")
        name_server = Config.get_general_field("name-server")	
        ipaddress=Config.get_cobbler_field("cobbler_ipaddress")
        for line in lines:
	    if 'url --url' in line:
		towrite.append("url --url=http://" + ipaddress + "/cobbler/images/RHEL")
		continue
            towrite.append(line)
            if '%post' in line:
		towrite.append(
		    "subscription-manager config --server.proxy_hostname=19.19.0.253 --server.proxy_port=80")
                towrite.append(
                    "subscription-manager register --username=" +
                    redhat_username +
                    " --password=" +
                    redhat_password )
                towrite.append(
                    "\nsubscription-manager subscribe --pool=" +
                    redhat_pool + "\n")
		#TO DO REMOVE HARD CODING
		towrite.append("/usr/bin/echo \"export http_proxy=http_proxy:19.19.0.253:80\" >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo \"export https_proxy=https_proxy:19.19.0.253:80\" >> /etc/bashrc\n")
	        towrite.append("/usr/bin/echo \"export no_proxy=127.0.0.1,localhost,19.19.100.102,19.*\" >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo \"nameserver " + name_server + "\" >> /etc/resolv.conf\n")
            
	    	
        file = open("/var/lib/cobbler/kickstarts/rhe7-osp5.ks", "w")
        file.writelines(towrite)
        file.close()
        #cobbler_setup.create_install_server(console)
        console.cprint_progress_bar("Creating Distro, Profiles, Systems and restarting Cobbler service",98)
        from cobbler_api_wrapper import Build_Server
        handle=Build_Server()
        handle.create_distro()	
        handle.create_profile()        
        handle.create_system()
        shell_command("/bin/systemctl restart cobblerd.service")
	time.sleep(10)
	shell_command("rm -f /var/lib/dhcpd/dhcpd.leases")
	shell_command("touch /var/lib/dhcpd/dhcpd.leases")
	shell_command("cobbler sync")
	time.sleep(10)
	shell_command("systemctl restart xinetd.service")
	time.sleep(700)
	handle.disable_netboot_systems()
        #handle.power_on_systems()
        console.cprint_progress_bar("Task Completed",100)


if __name__ == "__main__":
    handle = Cobbler_Integrator()
    #handle.cobbler_preInstall()
    #handle.cobbler_postInstall()
   
    

