import os,inspect
import sys,time
import shutil


from codebase.UnifiedStack.config.Config_Parser import Config
from general_utils import shell_command
from foreman_setup import Foreman_Setup, Provision_Host


class Foreman_Integrator():

    def __init__(self,console,data_source='database'):
        self.cur=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.data_dict={}
	self.read_from_database=False
	if data_source.title()=="Database":
            self.read_from_database=True
	else:
	    self.read_from_database==False
        self.console=console
	
        
    def preInstall(self,redhat_username,redhat_password,redhat_pool):
        setUpObj=Foreman_Setup(self.console)
        setUpObj.enable_repos(redhat_username,redhat_password,redhat_pool)
        setUpObj.install_prerequistes()
    
    def setup_foreman(self):
	
	#from config file
        if self.read_from_database==False:
            self.read_data_from_config_file()
        else:
            self.read_data_from_database()
	for key,value in self.data_dict.items():
	    print key + "   " + str(value)	
	self.modify_kickstart()
        installationObj=Foreman_Setup(self.console)
	installationObj.enable_repos(self.data_dict['redhat_username'],
                                      self.data_dict['redhat_password'],
                                      self.data_dict['redhat_pool'])
	installationObj.foreman_install(self.data_dict['system_hostname'],
                                        self.data_dict['system_ipaddress'],
                                        self.data_dict['domain_name'],
                                        self.data_dict['python_foreman_version'])
	self.extract_web_user_pass()

	installationObj.setup_dhcp_service(self.data_dict['dhcp_file'],
                                           self.data_dict['subnet'],
                                           self.data_dict['netmask'],
                                           self.data_dict['start_ip'],
                                           self.data_dict['end_ip'],
                                           self.data_dict['broadcast_ip'],
                                           self.data_dict['domain_name'],
                                           self.data_dict['nameserver'],
                                           self.data_dict['option_router'],
                                           self.data_dict['lease_time'],
                                           self.data_dict['max_lease_time'])
	
	installationObj.mount(self.data_dict['mount_path'],
                              self.data_dict['rhel_image_url'])
	self.run_simpleHTTPserver()	
        
        provisionObj=Provision_Host(self.console,
                                    self.data_dict['foreman_url'],
                                    self.data_dict['foreman_web_username'],
                                    self.data_dict['foreman_web_password'],
                                    self.data_dict['foreman_version'])
	
	provisionObj.create_smart_proxy(self.data_dict['system_hostname'] +
                                        "." +
                                        self.data_dict['domain_name'])
	provisionObj.create_environment(self.data_dict['environment'])
	provisionObj.create_domain(self.data_dict['domain_name'])	
	provisionObj.create_subnet(self.data_dict['subnet_name'],
                                   network_address=self.data_dict['subnet'],
                                   subnet_mask=self.data_dict['netmask'],
                                   domain_name=self.data_dict['domain_name'],
                                   tftp_smart_proxy=self.data_dict['system_hostname']
                                   + "." + self.data_dict['domain_name'])	
        provisionObj.create_os(self.data_dict['os_major'],self.data_dict['os_minor'],
                               self.data_dict['os_name'],self.data_dict['os_family'])
	provisionObj.create_installation_media(self.data_dict['os_family'],
                                               self.data_dict['installation_media_name'],
                                               self.data_dict['installation_media_url'])
	provisionObj.create_partition_table(self.data_dict['ptable_file'],
                                            self.data_dict['ptable_name'],
                                            self.data_dict['os_family'])	
	provisionObj.create_template("provision",self.data_dict['provision_template_path'],
                                     self.data_dict['provision_template_name'],
                                     self.data_dict['os_major'],
                                     self.data_dict['os_minor'],
                                     self.data_dict['os_name'])
	provisionObj.update_template("pxelinux",self.data_dict['pxelinux_template_name'],
                                     self.data_dict['os_major'],
                                     self.data_dict['os_minor'],
                                     self.data_dict['os_name'])	
	provisionObj.update_os(self.data_dict['ptable_name'],self.data_dict['os_family'],
                               self.data_dict['installation_media_name'],
                               self.data_dict['provision_template_name'],
                               self.data_dict['pxelinux_template_name'],
                               self.data_dict['os_major'],self.data_dict['os_minor'],
                               self.data_dict['os_name'])
	
        for host_name,host_data_dict in self.data_dict['system'].items():
	    provisionObj.create_host(host_name,
                                     self.data_dict['environment'],
                                     self.data_dict['domain_name'],
                                     host_data_dict['mac_address'],
                                     self.data_dict['subnet_name'],
                                     host_data_dict['ip_address'],
                                     self.data_dict['architecture'],
                                     self.data_dict['os_name'],
                                     self.data_dict['os_major'],
                                     self.data_dict['os_minor'],
                                     self.data_dict['status'],
	    			     self.data_dict['installation_media_name'],
                                     self.data_dict['ptable_name'],
                                     self.data_dict['root_pass'],
                                     self.data_dict['owner'])
	    provisionObj.write_host_to_dhcp(host_name,
                                            self.data_dict['domain_name'],
                                            host_data_dict['mac_address'],
                                            host_data_dict['ip_address'])
	    self.pxelinux_mac_file_entry(self.data_dict['system_ipaddress'],host_data_dict['mac_address'])
	
	provisionObj.copy_to_tftp_boot(self.data_dict['os_name'],
                                       self.data_dict['os_major'],
                                       self.data_dict['os_minor'],
                                       self.data_dict['architecture'])
	shell_command("service dhcpd restart")
	# Open up Firewall
        shell_command("service firewalld stop")
	#shell_command("firewall-cmd --zone=public --add-port=69/udp --permanent")
        #shell_command("firewall-cmd --zone=public --add-port=80/tcp --permanent")
        #shell_command("firewall-cmd --zone=public --add-port=443/tcp --permanent")
        #shell_command("firewall-cmd --reload")
	from fi import FI_PowerCycle
        FI_PowerCycle.FIPowerCycleServer().power_cycle()
        time.sleep(400)
	for host_name in self.data_dict['system'].keys():
	    provisionObj.modify_host(host_name)

    def extract_web_user_pass(self):
	answers=[]
	with open("/etc/foreman/foreman-installer-answers.yaml", "r") as file:
	    answers=file.readlines()
	print len(answers)
	for line in answers:
	    if 'admin_username' in line:
		self.data_dict['foreman_web_username']=line.strip().split(":")[1].strip()
	    if 'admin_password' in line:
                self.data_dict['foreman_web_password']=line.strip().split(":")[1].strip()

    def read_data_from_database(self):        
	from configurator import fetch_db
	db_foreman_obj=fetch_db.Foreman()
	db_general_obj=fetch_db.General()
        self.data_dict['system_ipaddress'] = db_foreman_obj.get('foreman-ip-address')
	self.data_dict['domain_name']= db_foreman_obj.get('domain-name')
        self.data_dict['nameserver']= db_foreman_obj.get('DNS')
	self.data_dict['option_router']= db_foreman_obj.get('option-router')
	self.data_dict['system_hostname'] = db_foreman_obj.get('foreman-hostname')
	self.data_dict['subnet']= db_foreman_obj.get('subnet')
        self.data_dict['netmask'] = db_foreman_obj.get('netmask')
	self.data_dict['http_proxy_ip']= db_foreman_obj.get('http-proxy-ip')
	self.data_dict['https_proxy_ip']= db_foreman_obj.get('https-proxy-ip')
	self.data_dict['https_port']= db_foreman_obj.get('https-port')
	self.data_dict['rhel_image_url']= db_general_obj.get('rhel-image-url')
	self.data_dict['isCSeries']=True
	#redhat
	self.data_dict['redhat_username'] = db_foreman_obj.get('redhat-username')
        self.data_dict['redhat_password'] = db_foreman_obj.get('redhat-password')
        self.data_dict['redhat_pool'] = db_foreman_obj.get('redhat-pool')
	#foreman
	self.data_dict['foreman_version']="2.0" 
	self.data_dict['foreman_url']="https://" + self.data_dict['system_ipaddress']
	#dhcp
	self.data_dict['dhcp_file']=self.cur + "/../data_static/dhcpd.conf"    #path to data_static/dhcp.conf
	self.data_dict['lease_time']="21600"
	self.data_dict['max_lease_time']="43200"
        self.data_dict['subnet_name']= self.data_dict['system_hostname']
	#Redhat public OS mounted and accessible through wget
	self.data_dict['mount_path']="/var/www/images/RHEL"
	self.data_dict['python_http_server_path']="/var/www/images/"
	#os 
	self.data_dict['os_family']="Redhat"
	self.data_dict['os_major']="7"
	self.data_dict['os_minor']="0"
	self.data_dict['os_name']="RHEL"
	self.data_dict['environment']="production"
	self.data_dict['architecture']="x86_64"
	#partition table
	self.data_dict['ptable_name']="rhel7_ptable"
        self.data_dict['ptable_file'] = self.cur + "/../data_static/" + self.data_dict['ptable_name']
	#host to be provisioned
	self.data_dict['status']="build"
	self.data_dict['root_pass']="Cisco12345"
	self.data_dict['owner']="Admin"
	#media
	self.data_dict['installation_media_name']="Redhat mirror"
	self.data_dict['installation_media_url']="http://" + self.data_dict['system_ipaddress'] + ":8000/RHEL"
	#templates
	self.data_dict['provision_template_name']="rhel7-osp5.ks"
	self.data_dict['provision_template_path']=self.cur+ "/../data_static/" + self.data_dict['provision_template_name']
	self.data_dict['pxelinux_template_name']="Kickstart default PXELinux"
	#python foreman version
	self.data_dict['python_foreman_version']="0.1.2"
	self.data_dict['system']={}
	systems = db_foreman_obj.get('systems')
        for system in systems:
            self.data_dict['system'][system.hostname]={'mac_address':system.mac_address,
                                                       'ip_address':system.ip_address}

    def read_data_from_config_file(self): 
        self.data_dict['system_ipaddress'] = '192.168.211.174'
        self.data_dict['domain_name']= 'domain.name'
        self.data_dict['nameserver']= '192.168.211.2'
        self.data_dict['option_router']= '192.168.211.2'  #gateway
        self.data_dict['system_hostname'] = 'buildserver-1'
        self.data_dict['subnet']= '192.168.211.0'         #network address
        self.data_dict['netmask'] = '255.255.255.0' 
        self.data_dict['http_proxy_ip']=''
        self.data_dict['https_proxy_ip']=''
        self.data_dict['https_port']='80'
        self.data_dict['rhel_image_url']='http://192.168.211.174:8000/rhel-server-7.0-x86_64-dvd.iso'
        self.data_dict['isCSeries']=False
        #redhat
        self.data_dict['redhat_username'] = 'rahuupad2'
        self.data_dict['redhat_password'] = 'iso*help123'
        self.data_dict['redhat_pool'] = "8a85f98444de1da50144e5c4aeae67d0"
	#foreman
        self.data_dict['foreman_version']="2.0"
        self.data_dict['foreman_url']="https://" + self.data_dict['system_ipaddress']
        #dhcp 
        self.data_dict['dhcp_file']=self.cur + "/../data_static/dhcpd.conf"    #path to data_static/dhcp.conf
        self.data_dict['lease_time']="21600"
        self.data_dict['max_lease_time']="43200"
	self.data_dict['subnet_name']= self.data_dict['system_hostname']

        #Redhat public OS mounted and accessible through wget
        self.data_dict['mount_path']="/var/www/images/RHEL"
        self.data_dict['python_http_server_path']="/var/www/images/"
        #os
        self.data_dict['os_family']="Redhat"
        self.data_dict['os_major']="7"
        self.data_dict['os_minor']="0"
        self.data_dict['os_name']="RHEL"
        self.data_dict['environment']="production"
        self.data_dict['architecture']="x86_64"
        #partition table
        self.data_dict['ptable_name']="rhel7_ptable"
        self.data_dict['ptable_file'] = self.cur + "/../data_static/" + self.data_dict['ptable_name']
        #host to be provisioned
        self.data_dict['status']="build"
        self.data_dict['root_pass']="Cisco12345"
        self.data_dict['owner']="Admin"
        #media
        self.data_dict['installation_media_name']="Redhat mirror"
        self.data_dict['installation_media_url']="http://" + self.data_dict['system_ipaddress'] + ":8000/RHEL"
        #templates
        self.data_dict['provision_template_name']="rhel7-osp5.ks"
        self.data_dict['provision_template_path']= self.cur+ "/../data_static/" + self.data_dict['provision_template_name']
        self.data_dict['pxelinux_template_name']="Kickstart default PXELinux"
        #python foreman version
        self.data_dict['python_foreman_version']="0.1.2"
        self.data_dict['system']={}
        #systems = Config.get_systems_data()
	#self.data_dict['system']['crhel-compute']={'mac_address':'00:25:B5:6A:00:1E',
        #                                            'ip_address':'192.168.211.178'}
	#self.data_dict['system']['nrhel1-network']={'mac_address':'00:25:B5:6A:00:06',
        #                                            'ip_address':'192.168.211.179'}

        for system in systems:
            self.data_dict['system'][system.hostname]={'mac_address':system.mac_address,
                                                       'ip_address':system.ip_address}

    def modify_kickstart(self): 
	#Update kickstart template  
        with open(self.cur+ "/../data_static/rhel7-osp5_aux.ks", "r") as file:
            kickstart=file.readlines()
        towrite = []
        no_proxy_string=self.get_no_proxy_string()
        for line in kickstart:
	    if 'url --url' in line:
                towrite.append("url --url=http://" + self.data_dict['system_ipaddress'] + ":8000/RHEL\n")
                continue
            towrite.append(line)
            if '%post' in line:
            	if self.data_dict['http_proxy_ip']!='':
		    towrite.append(
		        "subscription-manager config --server.proxy_hostname=" + self.data_dict['http_proxy_ip'] + " --server.proxy_port=80 \n")
                towrite.append(
                    "subscription-manager register --username=" +
                    self.data_dict['redhat_username'] +
                    " --password=" +
                    self.data_dict['redhat_password'] )
                towrite.append(
                    "\nsubscription-manager subscribe --pool=" +
                    self.data_dict['redhat_pool'] + "\n")
		#TO DO REMOVE HARD CODING
		if self.data_dict['http_proxy_ip']!='':
		    towrite.append("/usr/bin/echo 'export http_proxy=http://" + self.data_dict['http_proxy_ip'] + ":80' >> /etc/bashrc\n")
		    towrite.append("/usr/bin/echo \"export no_proxy=`echo " + no_proxy_string + " | sed 's/ /,/g'`\" >> /etc/bashrc\n")
		if self.data_dict['https_proxy_ip']!='':
                    towrite.append("/usr/bin/echo 'export https_proxy=https://" + self.data_dict['https_proxy_ip'] + ":" + self.data_dict['https_port'] + "' >> /etc/bashrc\n")
                towrite.append("/usr/bin/echo 'nameserver " + self.data_dict['nameserver'] + "' >> /etc/resolv.conf\n") 
		towrite.append("chkconfig NetworkManager stop\n")
                towrite.append("chkconfig NetworkManager off\n")
                
        with open(self.cur+ "/../data_static/rhel7-osp5.ks", "w") as file:
            file.writelines(towrite)

    def pxelinux_mac_file_entry(self,system_ip_address,host_mac_address):
	filename='01'
	splitted_list=host_mac_address.lower().split(":")
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

    def run_simpleHTTPserver(self):
        shell_command("pushd " + self.data_dict['python_http_server_path'] + "; python -m SimpleHTTPServer  > /dev/null 2>&1 &")
        shell_command("popd") 
    
    def copy_to_tftp_boot(self):
	filename=self.data_dict['os_name'] + "-" + self.data_dict['os_major'] + "." + self.data_dict['os_minor'] + "-" + self.data_dict['architecture'] + "-"
        src_dir="/var/www/images/RHEL/images/pxeboot/"
	dest_dir="/var/lib/tftpboot/boot/"
	shell_command("cp -f " + src_dir + "vmlinuz" + " " + dest_dir + filename + "vmlinuz")
	shell_command("cp -f " + src_dir + "initrd.img" + " " + dest_dir + filename + "initrd.img")

    def get_no_proxy_string(self):
	from netaddr import IPNetwork
        ip=IPNetwork(self.data_dict['subnet'] + "/" + self.data_dict['netmask'])
        length=len(list(ip))
        ip1=str(ip[0])
        ip2=str(ip[length-1])
        self.data_dict['start_ip']=ip1
        self.data_dict['end_ip']=ip2
        self.data_dict['broadcast_ip']=str(ip[length-2])
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

