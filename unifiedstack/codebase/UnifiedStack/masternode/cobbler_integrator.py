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
    
    def cobbler_preInstall_adapter(self,console):
        redhat_username = Config.get_cobbler_field('redhat_username') 
        redhat_password = Config.get_cobbler_field('redhat_password')   
        redhat_pool = Config.get_cobbler_field('redhat_pool')
	nameserver=Config.get_cobbler_field('cobbler_DNS')
	self.cobbler_preInstall(console,redhat_username,redhat_password,redhat_pool,nameserver)
        
    def cobbler_postInstall_adapter(self,console):
        cobbler_interface = Config.get_cobbler_field('cobbler_interface')
        cobbler_netmask = Config.get_cobbler_field('cobbler_netmask')
        cobbler_server = Config.get_cobbler_field('cobbler_server')
        cobbler_next_server = Config.get_cobbler_field('cobbler_next_server')
        cobbler_subnet = Config.get_cobbler_field('cobbler_subnet')
        cobbler_option_router = Config.get_cobbler_field('cobbler_option_router')
        cobbler_DNS = Config.get_cobbler_field('cobbler_DNS')
        cobbler_hostname = Config.get_cobbler_field('cobbler_hostname')
        cobbler_web_username = Config.get_cobbler_field('cobbler_web_username')
        cobbler_web_password = Config.get_cobbler_field('cobbler_web_password')	
	rhel_image_url=Config.get_general_field('rhel-image-url')
	redhat_username=Config.get_cobbler_field('redhat_username')
	redhat_password=Config.get_cobbler_field('redhat_password')
	redhat_pool=Config.get_cobbler_field('redhat_pool')
	http_proxy_ip=Config.get_cobbler_field('http_proxy_ip')
	https_proxy_ip=Config.get_cobbler_field('https_proxy_ip')
	https_port=Config.get_cobbler_field('https_port')
	distro_name=Config.get_cobbler_field('distro_name')
	systems=Config.get_systems_data()
	profiles = Config.get_profiles_data()
	nameserver=Config.get_cobbler_field('cobbler_DNS')
	
        self.cobbler_postInstall(console,cobbler_interface,cobbler_netmask,cobbler_server,cobbler_next_server,\
                cobbler_subnet,cobbler_option_router,cobbler_DNS,cobbler_hostname,cobbler_web_username,cobbler_web_password,\
                rhel_image_url,redhat_username,redhat_password,redhat_pool,http_proxy_ip,https_proxy_ip,\
                nameserver,distro_name,profiles,systems)
		
    def cobbler_preInstall(self,console,redhat_username,redhat_password,redhat_pool,nameserver): 
        shutil.copyfile(
            self.cur +
            "/../data_static/cobbler.repo",
            "/etc/yum.repos.d/cobbler.repo")
        cobbler_preInstall.enable_repos(console,redhat_username,redhat_password,redhat_pool)
        cobbler_preInstall.install_prerequistes()  
        cobbler_preInstall.disable_SELinux(console)
        #cobbler_preInstall.enable_networking(console)
        #cobbler_preInstall.add_name_server(console)

    def cobbler_postInstall(self,console,cobbler_interface,cobbler_netmask,cobbler_server,cobbler_next_server,\
                cobbler_subnet,cobbler_option_router,cobbler_DNS,cobbler_hostname,cobbler_web_username,cobbler_web_password,\
		rhel_image_url,redhat_username,redhat_password,redhat_pool,http_proxy_ip,https_proxy_ip,\
		nameserver,distro_name,profiles,systems):

        cobbler_setup.cobbler_setup(console,cobbler_interface,cobbler_netmask,cobbler_server,cobbler_next_server,\
		cobbler_subnet,cobbler_DNS,cobbler_hostname,cobbler_web_username,cobbler_web_password,cobbler_option_router)
        cobbler_setup.enable_services(console)
        shutil.copyfile(
            self.cur +
            "/../data_static/rsync",
            "/etc/xinetd.d/rsync")
        cobbler_setup.sync(console)
        cobbler_setup.mount(console,rhel_image_url)
        towrite = []
        file = open(self.cur+ "/../data_static/rhe7-osp5.ks", "r")
        lines = file.readlines()
        file.close()
        towrite = []
        for line in lines:
	    if 'url --url' in line:
		towrite.append("url --url=http://" + cobbler_server + "/cobbler/images/RHEL")
		continue
            towrite.append(line)
            if '%post' in line:
		towrite.append(
		    "subscription-manager config --server.proxy_hostname=" + http_proxy_ip + " --server.proxy_port=80 \n")
                towrite.append(
                    "subscription-manager register --username=" +
                    redhat_username +
                    " --password=" +
                    redhat_password )
                towrite.append(
                    "\nsubscription-manager subscribe --pool=" +
                    redhat_pool + "\n")
		#TO DO REMOVE HARD CODING
		towrite.append("/usr/bin/echo 'export http_proxy=http://" + http_proxy_ip + ":80' >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo 'export https_proxy=https://" + https_proxy_ip + ":" + https_port + "' >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo \"export no_proxy=`echo " + get_no_proxy_string(cobbler_subnet,cobbler_netmask) + " | sed 's/ /,/g'`\" >> /etc/bashrc\n")
                #towrite.append("/usr/bin/echo 'printf -v no_proxy '%s,' 19.19.{0..255}.{0..255}' >> /etc/bashrc\n")
                #towrite.append("/usr/bin/echo 'export no_proxy=${no_proxy%,}' >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo 'nameserver " + nameserver + "' >> /etc/resolv.conf\n") 
		towrite.append("chkconfig NetworkManager stop\n")
                towrite.append("chkconfig NetworkManager off\n") 
	    	
        file = open("/var/lib/cobbler/kickstarts/rhe7-osp5.ks", "w")
        file.writelines(towrite)
        file.close() 
        console.cprint_progress_bar("Creating Distro, Profiles, Systems and restarting Cobbler service. Power Cycle the systems after this",98)
        from cobbler_api_wrapper import Build_Server
        handle=Build_Server()
        handle.create_distro(name=distro_name)	
        handle.create_profile(profiles=profiles)        
        handle.create_system(systems=systems)
        shell_command("/bin/systemctl restart cobblerd.service")
	time.sleep(5)
	shell_command("rm -f /var/lib/dhcpd/dhcpd.leases")
	shell_command("touch /var/lib/dhcpd/dhcpd.leases")
	shell_command("cobbler sync")
	time.sleep(5)
	shell_command("systemctl restart xinetd.service")
	result=handle.power_cycle_systems(systems=systems)
	time.sleep(400)
	handle.disable_netboot_systems(systems=systems)  
        console.cprint_progress_bar("Task Completed",100)

    def get_no_proxy_string(self,cobbler_subnet,cobbler_netmask):
        ip=IPNetwork(cobbler_subnet + "/" + cobbler_netmask)
        length=len(list(ip))
        ip1=str(ip[0])
        ip2=str(ip[length-1])
        print ip1
        ip1_octets=ip1.split(".")
        ip2_octets=ip2.split(".")
        i=0
        while ip1_octets[i] == ip2_octets[i]:
            i=i+1
        j=0
        no_proxy_string=''
        while j < i:
            no_proxy_string = no_proxy_string + ip1_octets[j] + "."
            j=j+1
        while j < len(ip1_octets):
            no_proxy_string=no_proxy_string + "{" + ip1_octets[j] + ".." + ip2_octets[j] + "}"
            if j < len(ip1_octets) - 1:
                no_proxy_string=no_proxy_string + "."
            j=j+1
        return no_proxy_string


if __name__ == "__main__":
    handle = Cobbler_Integrator()
    #handle.cobbler_preInstall()
    #handle.cobbler_postInstall()
   
    

