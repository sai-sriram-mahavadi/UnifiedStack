#from masternode import cobbler_integrator as cobb
import os,sys
root_path = os.path.abspath(r"..")
sys.path.append(root_path)
from masternode import cobbler_integrator as cobb
from UnifiedStack.cli import Console_Output as cli
def configure_cobbler_preboot():
        redhat_username="rahuupad2"
        redhat_password="iso*help123"
        redhat_pool="8a85f98444de1da50144e5c4aeae67d0"
        nameserver=""
        console = cli.ConsoleOutput()
        cobbler_config = cobb.Cobbler_Integrator()
        cobbler_config.cobbler_preInstall(console,redhat_username,redhat_password,redhat_pool,nameserver) 
        read_bash = open("/root/.bashrc", "a")  
        shell.execute_command("reboot")

if __name__=="__main__":
    configure_cobbler_preboot()

