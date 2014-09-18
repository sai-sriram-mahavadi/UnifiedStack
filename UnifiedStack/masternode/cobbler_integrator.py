import cobbler_preInstall
import cobbler_setup
import os,inspect
import sys
import shutil
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config.Config_Parser import Config


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
        cobbler_preInstall.enable_networking(console)

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
        file = open(self.cur+ "/../data_static/rhel7-osp5.ks", "r")
        lines = file.readlines()
        file.close()
        towrite = []
        redhat_username = Config.get_cobbler_field("redhat_username")
        redhat_password = Config.get_cobbler_field("redhat_password")
        redhat_pool = Config.get_cobbler_field("redhat_pool")
        for line in lines:
            towrite.append(line)
            if '%post' in line:
                towrite.append(
                    "subscription-manager register --username=" +
                    redhat_username +
                    " --password=" +
                    redhat_password)
                towrite.append(
                    "\nsubscription-manager subscribe --pool=" +
                    redhat_pool +
                    "\n")
        file = open("/var/lib/cobbler/kickstarts/rhel7-osp5.ks", "w")
        for line in towrite:
            file.write(line)
        file.close()

        #cobbler_setup.create_install_server(console)


if __name__ == "__main__":
    handle = Cobbler_Integrator()
    #handle.cobbler_preInstall()
    #handle.cobbler_postInstall()
   
    

