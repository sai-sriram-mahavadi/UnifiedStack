from UcsSdk import *
    handle = UcsHandle()
    handle.Login("19.19.102.10","admin","Cisco12345)"
   

    #Power Cycle Server
    handle.StartTranscation()
    obj = handle.GetManagedObject(None, LsPower.ClassId(), {LsPower.DN:"org-root/ls-testLS1/power"})
    handle.SetManagedObject(obj, LsPower.ClassId(), {LsPower.STATE:"hard-reset-immediate"})
    handle.CompleteTransaction()

    
