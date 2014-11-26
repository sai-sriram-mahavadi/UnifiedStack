import os,sys,inspect
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)
import shutil
from general_utils import shell_command

class Installer:

    def __init__(self,console):
        self.cur=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.console=console

    def run(self,redhat_username, redhat_password, redhat_pool):
        # Subscription
        self.console.cprint_progress_bar("Subscription", 0)
        shell_command(
            "subscription-manager register --username=" +
            redhat_username +
            " --password=" +
            redhat_password)
        shell_command("subscription-manager attach --pool=" + redhat_pool)
        self.console.cprint_progress_bar("Updating", 5)
        shell_command("yum update -y")
        self.console.cprint_progress_bar("Updation done. Enabling repos", 50)
        self.enable_repos_foreman()
        self.enable_repos_cobbler()
	self.install_prerequistes()
        self.disable_SELinux()
        shell_command("reboot")

    def enable_repos_foreman(self):
        # Enabling the XML repos database of linux for installing
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
        self.console.cprint_progress_bar("Foreman repos enabled", 55)


    def enable_repos_cobbler(self):
        shutil.copyfile(
            self.cur +
            "/../data_static/cobbler.repo",
            "/etc/yum.repos.d/cobbler.repo")
        shell_command(
            "sudo yum-config-manager --enable rhel-7-server-openstack-5.0-rpms")
        shell_command(
            "sudo yum-config-manager --enable home_libertas-ict_cobbler26")
        self.console.cprint_progress_bar("Cobbler repos enabled", 60)

    def install_prerequistes(self):
        self.console.cprint_progress_bar("Installting pip", 65)
        shell_command("wget https://pypi.python.org/packages/source/p/pip/"
                      + "pip-1.2.1.tar.gz -O /root/pip_tar_file.tar.gz")
        shell_command("tar -zxvf /root/pip_tar_file.tar.gz -C /root/")
        shell_command("pushd /root/pip-1.2.1; python setup.py install; popd")
        self.console.cprint_progress_bar("Installing virtual Env", 75)
        shell_command("pip install virtualenv netaddr")
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

        self.console.cprint_progress_bar("Installing UcsSdk", 90)
        shell_command("wget https://communities.cisco.com/servlet/" + 
	              "JiveServlet/download/36899-13-78134/UcsSdk-0.8.2.tar.gz"
		      "	-O /root/UcsSdk-0.8.2.tar.gz")
        shell_command("tar -zxvf /root/UcsSdk-0.8.2.tar.gz -C /root/")
        shell_command("pushd /root/UcsSdk-0.8.2; python setup.py install; popd")
	


    def disable_SELinux(self):
        # disable SELinux and reboot
        self.console.cprint_progress_bar("Disabling the SELinux",95)
        shell_command(
            "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config")
        shell_command("yum update -y")
        self.console.cprint_progress_bar("Reupdating",95)
        self.console.cprint_progress_bar("TASK COMPLETED",100)

