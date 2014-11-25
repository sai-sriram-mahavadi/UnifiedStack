from UcsSdk import ucs
from FI_Config_Base import FIConfiguratorBase

class FIPowerCycleServer(FIConfiguratorBase):
    def power_cycle(self, service_profile_name)
        #Power Cycle Server
        handle = self.handle
        handle.StartTranscation()
        obj = handle.GetManagedObject(None, ucs.LsPower.ClassId(), {ucs.LsPower.DN:"org-root/ls-" + service_profile_name +"/power"})
        handle.SetManagedObject(obj, ucs.LsPower.ClassId(), {ucs.LsPower.STATE:"hard-reset-immediate"})
        handle.CompleteTransaction()

    
