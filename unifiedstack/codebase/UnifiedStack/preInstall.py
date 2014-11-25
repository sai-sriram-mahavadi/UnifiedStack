import os,sys
root_path = os.path.abspath(r"..")
sys.path.append(root_path)
from masternode import cobbler_integrator as cobb
from UnifiedStack.cli import Console_Output as cli
from masternode import foreman_integrator

def configure_cobbler_preboot():
        redhat_username="rahuupad2"
        redhat_password="iso*help123"
        redhat_pool="8a85f98444de1da50144e5c4aeae67d0"
        nameserver=""
        console = cli.ConsoleOutput()
        if len(sys.argv) != 2 or sys.argv[1] != '-C' or sys.argv[1] != '-F':
                print "USAGE: python preInstall.py -C/-F"
                exit(1)
        if sys.argv[1]=='C':
                cobblerObj = cobb.Cobbler_Integrator()
                cobblerObj.cobbler_preInstall(console,redhat_username,redhat_password,redhat_pool,nameserver) 
        elif sys.argv[1]=='F':
                foremanObj=foreman_integrator .Foreman_Integrator()
                foremanObj.preInstall(console,redhat_username,redhat_password,redhat_pool)


if __name__=="__main__":
    configure_cobbler_preboot()
