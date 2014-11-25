import UcsSdk as ucs
from FI_Config_Base import FIConfiguratorBase

class FIBootPolicy(FIConfiguratorBase):
    def configure_boot_policy(self, boot_policy_name, Vnic_name)
        handle = self.handle
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, ucs.OrgOrg.ClassId(), {ucs.OrgOrg.DN:"org-root"})
        mo = handle.AddManagedObject(obj, LsbootPolicy.ClassId(),
     {LsbootPolicy.REBOOT_ON_UPDATE:"no",
        LsbootPolicy.NAME:boot_policy_name,
        LsbootPolicy.ENFORCE_VNIC_NAME:"yes",
        LsbootPolicy.DN:"org-root/boot-policy-Boot_" + boot_policy_name ,
        LsbootPolicy.DESCR:"Boot Policy for Cobbler"})
        mo_1 = handle.AddManagedObject(mo, LsbootLan.ClassId(),
       {LsbootLan.DN:"org-root/boot-policy-Boot_Local/lan",
        LsbootLan.ORDER:"1", LsbootLan.PROT:"pxe"}, True)
        mo_1_1 = handle.AddManagedObject(mo_1, LsbootLanImagePath.ClassId(),
         {LsbootLanImagePath.DN:"org-root/boot-policy-" + boot_policy_name +"/lan/path-primary",
        LsbootLanImagePath.VNIC_NAME:Vnic_name,
        LsbootLanImagePath.TYPE:"primary"})
        mo_3 = handle.AddManagedObject(mo, LsbootStorage.ClassId(),
       {LsbootStorage.DN:"org-root/boot-policy-" + boot_policy_name + "/storage ",
        LsbootStorage.ORDER:"2"})
        mo_3_1 = handle.AddManagedObject(mo_3, LsbootLocalStorage.ClassId(),
       {LsbootLocalStorage.DN:"org-root/boot-policy-" + boot_policy_name + "/storage/local-storage"})
