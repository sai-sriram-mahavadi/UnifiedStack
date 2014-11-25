import os,inspect
import sys,time
import shutil
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config.Config_Parser import Config
from general_utils import shell_command
from foreman_setup import Foreman_Setup, Provision_Host
from netaddr import *

class Foreman_Integrator():

    def __init__(self):
        self.cur=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    def preInstall(self,console,redhat_username,redhat_password,redhat_pool):
        setUpObj=Foreman_Setup()
        setUpObj.enable_repos(console,redhat_username,redhat_password,redhat_pool)
        setUpObj.install_prerequistes(console)
    
    def setup_foreman(self):
	#from config file
        system_ipaddress = Config.get_cobbler_field('cobbler_ipaddress')
	domain_name= "cisco.com"
        nameserver= Config.get_cobbler_field('cobbler_DNS')
	option_router= Config.get_cobbler_field('cobbler_option_router')  #gateway
	system_hostname = Config.get_cobbler_field('cobbler_hostname')
	subnet= Config.get_cobbler_field('cobbler_subnet')          #network address
        netmask = Config.get_cobbler_field('cobbler_netmask')
	subnet_name=system_hostname
	proxy="19.19.0.253"
	rhel_image_url=Config.get_general_field("rhel-image-url")
	#redhat
	redhat_username = Config.get_cobbler_field('redhat_username')
        redhat_password = Config.get_cobbler_field('redhat_password')
        redhat_pool = Config.get_cobbler_field('redhat_pool')
	#foreman
	foreman_web_username = "admin"
	foreman_web_password = "12345678"
	foreman_version="2.0" 
	foreman_url="https://" + system_ipaddress
	#dhcp 
	start_ip="19.19.0.0"
        end_ip="19.19.255.254"
	broadcast_ip="19.19.255.255"
	dhcp_file=self.cur + "/../data_static/dhcpd.conf"    #path to data_static/dhcp.conf
	lease_time="21600"
	max_lease_time="43200"
	#rhel mirror
	mount_path="/var/www/images/RHEL"
	python_http_server_path="/var/www/images/"
	#os 
	os_family="Redhat"
	os_major="7"
	os_minor="0"
	os_name="RHEL"
	environment="production"
	architecture="x86_64"
	#partition table
	ptable_name="rhel7_ptable"
        ptable_file = self.cur + "/../data_static/" + ptable_name
	#host to be provisioned
	status="build"
	root_pass="12345678"
	owner="Admin"
	mac_address=None
	ip_address=None
	host_name=None
	#media
	installation_media_name="Redhat mirror"
	installation_media_url="http://" + system_ipaddress + ":8000/RHEL"
	#templates
	provision_template_name="rhel7-osp5.ks"
	provision_template_path=self.cur+ "/../data_static/" + provision_template_name
	pxelinux_template_name="Kickstart default PXELinux"
	#python foreman version
	python_foreman_version="0.1.2"

	self.modify_kickstart(redhat_username,redhat_password,redhat_pool,nameserver,system_ipaddress,proxy)
        installationObj=Foreman_Setup()
	installationObj.enable_repos(redhat_username,redhat_password,redhat_pool)
	installationObj.foreman_install(system_hostname,system_ipaddress,domain_name,foreman_web_username,foreman_web_password,python_foreman_version)
	installationObj.setup_dhcp_service(dhcp_file,subnet,netmask,start_ip,end_ip,broadcast_ip,domain_name,nameserver,option_router,lease_time,max_lease_time)
	installationObj.mount(mount_path,rhel_image_url)
	self.run_simpleHTTPserver(python_http_server_path)	
        provisionObj=Provision_Host(foreman_url,foreman_web_username,foreman_web_password,foreman_version)
	provisionObj.create_smart_proxy(system_hostname + "." +  domain_name)
	provisionObj.create_environment(environment)
	provisionObj.create_domain(domain_name)	
	provisionObj.create_subnet(subnet_name,network_address=subnet,subnet_mask=netmask,domain_name=domain_name,tftp_smart_proxy=system_hostname + "." +  domain_name)	
        provisionObj.create_os(os_major,os_minor,os_name,os_family)
	provisionObj.create_installation_media(os_family,installation_media_name,installation_media_url)
	provisionObj.create_partition_table(ptable_file,ptable_name,os_family)	
	provisionObj.create_template("provision",provision_template_path,provision_template_name,os_major,os_minor,os_name)
	provisionObj.update_template("pxelinux",pxelinux_template_name,os_major,os_minor,os_name)	
	provisionObj.update_os(ptable_name,os_family,installation_media_name,provision_template_name,pxelinux_template_name,os_major,os_minor,os_name)
	
	systems = Config.get_systems_data()
        for system in systems:
            host_name = system.hostname
            mac_address = system.mac_address
            ip_address = system.ip_address	
	    provisionObj.create_host(host_name,environment,domain_name,mac_address,subnet_name,ip_address,architecture,os_name,os_major,os_minor,status,
	    			 installation_media_name,ptable_name,root_pass,owner)
	    provisionObj.write_host_to_dhcp(host_name,domain_name,mac_address,ip_address)
	self.pxelinux_mac_file_entry(system_ipaddress,mac_address)
	provisionObj.copy_to_tftp_boot(os_name,os_major,os_minor,architecture)
	
    def modify_kickstart(self,redhat_username,redhat_password,redhat_pool,name_server,ipaddress,proxy): 
	#Update kickstart template  
        with open(self.cur+ "/../data_static/rhel7-osp5_aux.ks", "r") as file:
            kickstart=file.readlines()
        towrite = []
        for line in kickstart:
	    if 'url --url' in line:
                towrite.append("url --url=http://" + ipaddress + ":8000/RHEL\n")
                continue
            towrite.append(line)
            if '%post' in line:
            	if http_proxy_ip!='':
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
		if http_proxy_ip!='':
		    towrite.append("/usr/bin/echo 'export http_proxy=http://" + http_proxy_ip + ":80' >> /etc/bashrc\n")
		if https_proxy_ip!='':
                    towrite.append("/usr/bin/echo 'export https_proxy=https://" + https_proxy_ip + ":" + https_port + "' >> /etc/bashrc\n")
                if http_proxy_ip!='':
                    towrite.append("/usr/bin/echo \"export no_proxy=`echo " + self.get_no_proxy_string(cobbler_subnet,cobbler_netmask) + " | sed 's/ /,/g'`\" >> /etc/bashrc\n")
                #towrite.append("/usr/bin/echo 'printf -v no_proxy '%s,' 19.19.{0..255}.{0..255}' >> /etc/bashrc\n")
                #towrite.append("/usr/bin/echo 'export no_proxy=${no_proxy%,}' >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo 'nameserver " + nameserver + "' >> /etc/resolv.conf\n") 
		towrite.append("chkconfig NetworkManager stop\n")
                towrite.append("chkconfig NetworkManager off\n")
        with open(self.cur+ "/../data_static/rhel7-osp5.ks", "w") as file:
            file.writelines(towrite)

    def pxelinux_mac_file_entry(self,system_ip_address,host_mac_address):
	filename='01'
	splitted_list=host_mac_address.split(":")
	for i in splitted_list:
	    if i!=":":
	        filename=filename + "-" + i
        with open("/var/lib/tftpboot/pxelinux.cfg/" + filename,"r") as file:
            lines=file.readlines()
	toWrite=[]
        for line in lines:
            if 'append initrd' in line:	
                i=line.index('http://')
                i=i+len('http://')
                j=line.index(':80/')
                line=line[:i] + system_ip_address + line[j:]
	    toWrite.append(line)
        with open("/var/lib/tftpboot/pxelinux.cfg/" + filename,"w") as file:
                file.writelines(toWrite)

    def run_simpleHTTPserver(self,http_server_path):
        shell_command("pushd " + http_server_path + "; python -m SimpleHTTPServer  > /dev/null 2>&1 &")
        shell_command("popd") 
    
    def copy_to_tftp_boot(self,os_name,os_major,os_minor,architecture):
	filename=os_name + "-" + os_major + "." + os_minor + "-" + architecture + "-"
        src_dir="/var/www/images/RHEL/images/pxeboot/"
	dest_dir="/var/lib/tftpboot/boot/"
	shell_command("cp -f " + src_dir + "vmlinuz" + " " + dest_dir + filename + "vmlinuz")
	shell_command("cp -f " + src_dir + "initrd.img" + " " + dest_dir + filename + "initrd.img")

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
