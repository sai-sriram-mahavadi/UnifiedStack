
import os
import sys
root_path = os.path.abspath(r"../..")
sys.path.append(root_path)
file=open(root_path + "/UnifiedStack/data_static/rhel7-osp5.ks" ,"r")
lines=file.readlines()
file.close()

import shutil
shutil.copyfile(root_path + "/UnifiedStack/data_static/rhel7-osp5.ks","/rhel7-osp5.ks")





