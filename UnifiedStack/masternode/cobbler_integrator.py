import cobbler_preInstall
import cobbler_setup
import os
import sys
import shutil
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)

from UnifiedStack.config.Config_Parser import Config


class Cobbler_Integrator():

    def __init__(self):
        pass

    def cobbler_preInstall(self):
        shutil.copyfile(
            root_path +
            "/UnifiedStack/data_static/cobbler.repo",
            "/etc/yum.repos.d/cobbler.repo")
        cobbler_preInstall.enable_repos()
        cobbler_preInstall.disable_SELinux()

    def cobbler_postInstall(self):

        cobbler_setup.cobbler_setup()
        cobbler_setup.enable_services()
        shutil.copyfile(
            root_path +
            "/UnifiedStack/data_static/rsync",
            "/etc/xinetd.d/rsync")
        cobbler_setup.sync()
        cobbler_setup.mount()
        towrite = []
        file = open(root_path + "/UnifiedStack/data_static/rhel7-osp5.ks", "r")
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

        cobbler_setup.create_install_server()


if __name__ == "__main__":
    handle = Cobbler_Integrator()
    handle.cobbler_preInstall()
    handle.cobbler_postInstall()
