import os,sys
root_path = os.path.abspath(r"..")
sys.path.append(root_path)
from masternode import cobbler_integrator as cobb
from UnifiedStack.cli import Console_Output as cli
from masternode import foreman_integrator
from masternode.preboot_installer import Installer 
from masternode.general_utils import shell_command

def configure_cobbler_preboot():
    print "**" * 10 + "ENTER THE SUBSCRIPTION INFORMAION" + "**" * 10
    redhat_username=raw_input("REDHAT_ACOOUNT_USERNAME ?:")
    redhat_password=raw_input("REDHAT_ACOOUNT_PASSWORD ?:")
    print "**" * 10 + "ENTER THE PROXY INFORMAION . ENTER FOR NONE" + "**" * 10
    redhat_pool="8a85f98444de1da50144e5c4aeae67d0"
    nameserver=""
    console = cli.ConsoleOutput()
    if len(sys.argv)== 1:
	foremanObj=foreman_integrator.Foreman_Integrator(console)
        foremanObj.preInstall(redhat_username,redhat_password,redhat_pool)
        #Installer(console).run(redhat_username,redhat_password,redhat_pool)		        
    elif len(sys.argv) == 2  and  (sys.argv[1] != '-C' and sys.argv[1] != '-F'):
        print "USAGE: python preInstall.py -C/-F"
        exit(1)
    elif sys.argv[1]=='-C':
        cobblerObj = cobb.Cobbler_Integrator()
        cobblerObj.cobbler_preInstall(console,redhat_username,redhat_password,redhat_pool,nameserver) 
    elif sys.argv[1]=='-F':
        foremanObj=foreman_integrator.Foreman_Integrator(console)
        foremanObj.preInstall(redhat_username,redhat_password,redhat_pool)
    

if __name__=="__main__": 
    configure_cobbler_preboot()
