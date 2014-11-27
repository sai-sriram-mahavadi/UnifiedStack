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

from .general_utils import shell_command, bcolors, shell_command_true
import inspect
import os
import sys



from codebase.UnifiedStack.config.Config_Parser import Config


class Foreman_Setup():

    def __init__(self,console):
        self.cur=os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        self.console=console

    def enable_repos(self,redhat_username, redhat_password, redhat_pool):
        # Subscription
        self.console.cprint_progress_bar("Subscription", 0)
        shell_command_true(
            "subscription-manager register --username=" +
            redhat_username +
            " --password=" +
            redhat_password)
	shell_command("subscription-manager subscribe --auto")
        shell_command_true("subscription-manager attach --pool=" + redhat_pool)
        self.console.cprint_progress_bar("Updating the System", 5)
        # Enabling the XML repos database of linux for installing
        shell_command("yum update -y")
        self.console.cprint_progress_bar("System updated. Now enabling \
                                         repos", 45)
        shell_command(
            "rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-" + 
	    "el-7.noarch.rpm")
        shell_command(
            "rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/" +
	    "epel-release-7-2.noarch.rpm")
	shell_command(
            "yum-config-manager --enable rhel-7-server-optional-rpms " +
            "rhel-server-rhscl-7-rpms epel")

        self.console.cprint_progress_bar("Required Repos enabled", 50)
	shell_command("yum update -y")
	self.console.cprint_progress_bar("Re-Updated", 65)


    def install_prerequistes(self):
        self.console.cprint_progress_bar("Installting pip", 65)
        shell_command("wget https://pypi.python.org/packages/source/p/pip/"
                      + "pip-1.2.1.tar.gz -O /root/pip_tar_file.tar.gz")
        shell_command("tar -zxvf /root/pip_tar_file.tar.gz -C /root/")
        shell_command("pushd /root/pip-1.2.1; python setup.py install; popd")
        self.console.cprint_progress_bar("Installing virtual Env", 75)
        shell_command("pip install virtualenv")
        self.console.cprint_progress_bar("Setting up virtual Env", 85)
        file_dir=os.path.dirname(os.path.abspath(inspect.getfile
                                                 (inspect.currentframe())))
        UnifiedStack_top_dir= file_dir +  "/../../../.."
	virtual_env_path = UnifiedStack_top_dir + "/UnifiedStackVirtualEnv"
        shell_command("virtualenv " + virtual_env_path)
        shell_command("cp -rf " + UnifiedStack_top_dir +
                      "/unifiedstack  " +  virtual_env_path +  "/")        
	self.console.cprint_progress_bar("Installing Django", 85)
        shell_command(virtual_env_path + "/bin/pip install django==1.7")
        shell_command(virtual_env_path + "/bin/pip install djangorestframework")
	
        self.console.cprint_progress_bar("Installing UcsSdk", 85)
        shell_command("wget https://communities.cisco.com/servlet/" + 
                       "JiveServlet/download/36899-13-76835" + 
                       "/UcsSdk-0.8.2.tar.gz -O /root/UcsSdk-0.8.2.tar.gz")
        shell_command("tar -zxvf /root/UcsSdk-0.8.2.tar.gz -C /root/")
        shell_command("pushd /root/UcsSdk-0.8.2; python setup.py install; popd")
        self.console.cprint_progress_bar("Task Completed", 100)
	
	

    def disable_SELinux(self,console):
        # disable SELinux and reboot
        #console.cprint_progress_bar("Disabling the SELinux", 80)
        shell_command_true(
            "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config")
        shell_command("yum update -y")
        console.cprint_progress_bar("Reupdating", 90)
        console.cprint_progress_bar("TASK COMPLETED", 100)

    def foreman_install(
            self,
            hostname,
            ipaddress,
            domain_name,
            foreman_web_username,
            foreman_web_password,
	    python_foreman_version):
        shell_command(
            "/usr/bin/yum -y install http://yum.theforeman.org/releases/"
            "1.6/el7/x86_64/foreman-release.rpm")
        shell_command_true(
            "/usr/bin/yum -y install foreman-installer")
        with open('/etc/hostname', 'w') as file:
            file.write(hostname)
        with open('/etc/hosts', 'a') as file:
            file.write(ipaddress + " " + hostname + "." + domain_name +
                       " " + hostname)
        shell_command(
            "foreman-installer")
        shell_command(
            "pip install -Iv https://pypi.python.org/packages/source/p/" +
            "python-foreman/python-foreman-" + python_foreman_version + ".tar.gz")

    def setup_dhcp_service(
            self,
            dhcp_file,
            subnet,
            netmask,
            start_ip,
            end_ip,
            broadcast_ip,
            domain_name,
            nameserver,
	    gateway,
            lease_time,
            max_lease_time):
        shell_command_true(
            "/usr/bin/yum -y install dhcp")
        #with open(self.cur+ "/../data_static/" + dhcp_file, "r") as file:
	with open(dhcp_file, "r") as file:
            lines = file.readlines()
        lines_to_write = []
        for line in lines:
            if 'subnet' in line and 'netmask' in line:
                lines_to_write.append(
                    "subnet " +
                    subnet +
                    " netmask " +
                    netmask +
                    " {\n")
            elif 'range' in line:
                lines_to_write.append(
                    "\trange " +
                    start_ip +
                    " " +
                    end_ip +
                    ";\n")
            elif 'option subnet-mask' in line:
                lines_to_write.append(
                    "\t\toption subnet-mask\t\t" +
                    netmask +
                    ";\n")
            elif 'option broadcast-address' in line:
                lines_to_write.append(
                    "\t\toption broadcast-address\t\t" +
                    broadcast_ip +
                    ";\n")
            elif 'option routers' in line:
                lines_to_write.append(
                    "\t\toption routers\t\t" +
                    gateway +
                    ";\n")
            elif 'option domain-name' in line and 'option domain-name-servers' not in line:
                lines_to_write.append(
                    "\t\toption domain-name\t\t\"" +
                    domain_name +
                    "\";\n")
            elif 'option domain-name-servers' in line:
                lines_to_write.append(
                    "\t\toption domain-name-servers\t\t" +
                    nameserver +
                    ";\n")
            elif 'default-lease-time'in line:
                lines_to_write.append(
                    "\tdefault-lease-time\t" +
                    lease_time +
                    ";\n")
            elif 'max-lease-time' in line:
                lines_to_write.append(
                    "\tmax-lease-time\t" +
                    max_lease_time +
                    ";\n")
            else:
                lines_to_write.append(line)
        with open("/etc/dhcp/dhcpd.conf", "w") as file:
            file.writelines(lines_to_write)
        shell_command("systemctl start dhcpd.service")
        shell_command("systemctl enable dhcpd.service")
        shell_command("systemctl status dhcpd.service")
        shell_command("systemctl restart xinetd.service")
       
    def mount(self, mount_path,rhel_image_url):
        """Here goes the code to wget the rhel image in the /root directory"""
        shell_command("mkdir -p " + mount_path)
        shell_command(
            "wget " +
            rhel_image_url +
            " -O  /root/rhel-server-7.0-x86_64-dvd.iso ")
        shell_command(
            "mount -t iso9660  /root/rhel-server-7.0-x86_64-dvd.iso " +
            mount_path)
	
        #shell_command("cp -r /var/www/images/RHEL/images/pxeboot/* /var/lib/tftpboot/boot/")
        # shell_command("rm -rf /root/rhel-server-7.0-x86_64-dvd.iso")
    
    


class Provision_Host():
    def __init__(self,console,foreman_url,foreman_username,
                 foreman_password,foreman_version):
	import foreman.client
        self.connectObj = foreman.client.Foreman(
            url=foreman_url,
            auth=(
                foreman_username,
                foreman_password),
                version=foreman_version
		)
        for template in self.connectObj.index_template_kinds():
            if template['template_kind']['name'] == 'PXELinux':
                self.pxelinux_template_kind_id = template[
                    'template_kind']['id']
        for template in self.connectObj.index_template_kinds():
            if template['template_kind']['name'] == 'provision':
                self.provision_template_kind_id = template[
                    'template_kind']['id']


    def create_host(
            self,
            host_name,
            host_environment,
            domain_name,
            host_mac_address,
            subnet_name,
            host_ip_address,
            host_architecture,
            os_name,
            os_major,
            os_minor,
            host_status,
            installation_media_name,
            ptable_name,
            host_root_pass,
            host_owner):

        for ptable in self.connectObj.index_ptables(
                search=ptable_name):
            if ptable['ptable']['name'] == ptable_name:
                ptable_id = ptable['ptable']['id']
        for medium in self.connectObj.index_media(
                search=installation_media_name):
            if medium['medium']['name'] == installation_media_name:
                medium_id = medium['medium']['id']
        for os in self.connectObj.index_operatingsystems(
                search=os_name +
                " " +
                os_major +
                " " +
                os_minor):
            if os['operatingsystem']['name'] == os_name and os['operatingsystem']['major'] == os_major and os['operatingsystem']['minor'] == os_minor:
                host_operating_system_id = os['operatingsystem']['id']
        for user in self.connectObj.index_users(search=host_owner):
            if user['user']['firstname'] == host_owner:
                owner_id = user['user']['id']
        for subnet in self.connectObj.index_subnets(search=subnet_name):
            if subnet['subnet']['name']==subnet_name:
                subnet_id=subnet['subnet']['id']

        host = {
            'name': host_name,
            'environment_id':self.connectObj.index_environments(
                search=host_environment)[0]['environment']['id'],
            'domain_id': self.connectObj.index_domains(
                search=domain_name)[0]['domain']['id'],
            'mac': host_mac_address,
            'subnet_id':subnet_id,
            'ip': host_ip_address,
            'architecture_id': self.connectObj.index_architectures(
                search=host_architecture)[0]['architecture']['id'],
            'operatingsystem_id': host_operating_system_id,
            'build': host_status=='build',
            'medium_id': medium_id,
            'ptable_id': ptable_id,
            'root_pass': host_root_pass,
            'owner_id': owner_id,
        }
        self.connectObj.create_hosts(host)
 
    def write_host_to_dhcp(self,host_name,
                           domain_name,host_mac_address,host_ip_address):
        with open("/etc/dhcp/dhcpd.conf","r") as file:
            dhcp_conf=file.readlines()
        while dhcp_conf.pop()=='\n':pass
        dhcp_conf.append("host " + host_name + "." + domain_name + "{\n")
        dhcp_conf.append("\thardware ethernet " + host_mac_address + ";\n")
        dhcp_conf.append("\tfixed-address " + host_ip_address + ";\n")
        dhcp_conf.append('\tfilename "pxelinux.0";\n\t}\n}')
        with open("/etc/dhcp/dhcpd.conf","w") as file:
            file.writelines(dhcp_conf)
	shell_command("service dhcpd restart")

    def create_os(self, os_major, os_minor, os_name, os_family):
        os = {
            'name': os_name,
            'major': os_major,
            'minor': os_minor,
            'family': os_family}
        self.connectObj.create_operatingsystems(os)

    def update_os(
            self,
            ptable_name,
            os_family,
            installation_media_name,
            provision_template_name,
            pxelinux_template_name,
            os_major,
            os_minor,
            os_name):
        ptable_id = []
        medium_id = []
        architecture_id = []
        config_templates_id = []
        provision_template_id = None
        pxelinux_template_id = None
        os_id = None
        for ptable in self.connectObj.index_ptables(
                search=ptable_name +
                " " +
                os_family):
            if ptable['ptable']['name'] == ptable_name and ptable[
                    'ptable']['os_family'] == os_family:
                ptable_id.append(ptable['ptable']['id'])
        for medium in self.connectObj.index_media(
                search=installation_media_name +
                " " +
                os_family):
            if medium['medium']['name'] == installation_media_name and medium[
                    'medium']['os_family'] == os_family:
                medium_id.append(medium['medium']['id'])
        page_no=1
	templates=self.connectObj.index_config_templates(page=page_no)
	while templates:
            for template in templates:
	        if 'template_kind' not in template['config_template'].keys():
		    continue
                if template['config_template']['template_kind']['id'] == self.provision_template_kind_id and template[
                        'config_template']['name'] == provision_template_name:
                    config_templates_id.append(template['config_template']['id'])
                    provision_template_id = template['config_template']['id']
                if template['config_template']['template_kind']['id'] == self.pxelinux_template_kind_id and template[
                        'config_template']['name'] == pxelinux_template_name:
                    config_templates_id.append(template['config_template']['id'])
                    pxelinux_template_id = template['config_template']['id']
	    page_no=page_no + 1
	    templates=self.connectObj.index_config_templates(page=page_no)
        for arch in self.connectObj.index_architectures():
            architecture_id.append(arch['architecture']['id'])
        
        os = {'ptable_ids': ptable_id,
              'medium_ids': medium_id,
              'config_template_ids': config_templates_id,
              'architecture_ids': architecture_id,
              'os_default_templates_attributes': {0: {'template_kind_id': self.provision_template_kind_id,
                                                       'config_template_id': provision_template_id}}}
                                              
        for oss in self.connectObj.index_operatingsystems(
                search=os_name +
                " " +
                os_major +
                " " +
                os_minor):
            if oss['operatingsystem']['name'] == os_name and oss['operatingsystem'][
                    'major'] == os_major and oss['operatingsystem']['minor'] == os_minor:
                os_id = oss['operatingsystem']['id']
        	
        self.connectObj.update_operatingsystems(os, id=os_id)
	os= {'os_default_templates_attributes':{0:{'template_kind_id': self.pxelinux_template_kind_id,
                                                      'config_template_id': pxelinux_template_id}}}
        self.connectObj.update_operatingsystems(os, id=os_id)


    def create_installation_media(
            self,
            os_family,
            installation_media_name,
            installation_media_url):
        medium = {
            'os_family': os_family,
            'name': installation_media_name,
            'path': installation_media_url}
        self.connectObj.create_media(medium)

    def create_partition_table(
            self,
            ptable_layout_file,
            ptable_name,
            os_family):
        with open(ptable_layout_file, "r") as file:
            layout = file.read()
        ptable = {
            'name': ptable_name,
            'os_family': os_family,
            'layout': layout}
        self.connectObj.create_ptables(ptable)

    def create_template(
            self,
            type,
            template_path,
            template_name,
            os_major,
            os_minor,
            os_name):
        with open(template_path, "r") as file:
            template_file = file.read()
        os_search_list = self.connectObj.index_operatingsystems(
            search=os_major +
            " " +
            os_minor +
            " " +
            os_name)
        os_ids = []
        for os in os_search_list:
	    if os['operatingsystem']['name'] == os_name and os['operatingsystem'][
                    'major'] == os_major and os['operatingsystem']['minor'] == os_minor:
                os_ids.append(os['operatingsystem']['id'])
        if type == "pxelinux":
            template_kind_id = self.pxelinux_template_kind_id
        elif type == "provision":
            template_kind_id = self.provision_template_kind_id
        cfg_template = {
            'name': template_name,
            'operatingsystem_ids': os_ids,
            'template_kind_id': template_kind_id,
            'template': template_file}
        self.connectObj.create_config_templates(cfg_template)

    def update_template(
            self,
            type,
            template_name,
            os_major,
            os_minor,
            os_name):
        templates = self.connectObj.index_config_templates(
            search=template_name)
        if type == "pxelinux":
            template_kind_id = self.pxelinux_template_kind_id
        elif type == "provision":
            template_kind_id = self.provision_template_kind_id
        for template in templates:
            if template['config_template']['name'] == template_name and template[
                    'config_template']['template_kind']['id'] == template_kind_id:
                id = template['config_template']['id']
        os_search_list = self.connectObj.index_operatingsystems(
            search=os_major +
            " " +
            os_minor +
            " " +
            os_name)
        os_ids = []
        for os in os_search_list:
	    if os['operatingsystem']['name'] == os_name and os['operatingsystem']['major'] == os_major and os['operatingsystem']['minor'] == os_minor:
                os_ids.append(os['operatingsystem']['id'])
        self.connectObj.update_config_templates(
            {'operatingsystem_ids': os_ids}, id)


    def create_smart_proxy(self,full_hostname):
	for proxy in self.connectObj.index_smart_proxies():
	    if proxy['smart_proxy']['name']==full_hostname:
		return
	self.connectObj.create_smart_proxies(
            {'name':full_hostname,'url':"https://" + full_hostname + ":8443"})

    def create_environment(self,environment):
	for envir in self.connectObj.index_environments(search=environment):
	    if envir['environment']['name']==environment:
		return 
	self.connectObj.create_environments({'name':environment})

    def create_domain(self,domain_name):
	for domain in self.connectObj.index_domains(search=domain_name):
	    if domain['domain']['name']==domain_name:
		return
	self.connectObj.create_domains({'name':domain_name})

    def create_subnet(self,subnet_name,
                      network_address,subnet_mask,
                      domain_name,tftp_smart_proxy):
	for subnet in self.connectObj.index_subnets(search=
                                                    subnet_name
                                                    + " " +
                                                    network_address
                                                    + " " +
                                                    subnet_mask):
	    if subnet['subnet']['name']==subnet_name or subnet['subnet']['network']==network_address:
		return
	domain_ids=[]
	for domain in self.connectObj.index_domains(search=domain_name):
	    if domain['domain']['name']==domain_name:
		domain_ids.append(domain['domain']['id'])
	proxy_id=None
	for proxy in self.connectObj.index_smart_proxies():
	    if proxy['smart_proxy']['name']==tftp_smart_proxy:
		proxy_id=proxy['smart_proxy']['id']
	print proxy_id
	subnet={'name':subnet_name,'network':network_address,'mask':subnet_mask,
                'domain_ids':domain_ids,'tftp_id':proxy_id}
	self.connectObj.create_subnets(subnet)

    def copy_to_tftp_boot(self,os_name,os_major,os_minor,architecture):
        filename=os_name + "-" + os_major + "." + os_minor + "-" + architecture + "-"
        src_dir="/var/www/images/RHEL/images/pxeboot/"
        dest_dir="/var/lib/tftpboot/boot/"
	if os.path.getsize(dest_dir + filename + "vmlinuz") == 0:
            shell_command("cp -f " + src_dir + "vmlinuz" + " " +
                          dest_dir + filename + "vmlinuz")
        if os.path.getsize(dest_dir + filename + "initrd.img") == 0):
	    shell_command("cp -f " + src_dir + "initrd.img" + " " +
                          dest_dir + filename + "initrd.img")

