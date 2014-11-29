from logger.models import Log
from configurator.models import DeviceTypeSetting, Device, DeviceSetting

# Util functions for data loading
def values_to_str(arr_stype):
    str_stype = "("    
    for stype in arr_stype:
        str_stype += str(stype) + ";"
    str_stype = str_stype[:-1] + ")"
    return str_stype;



#if __name__=="__main__":
print ""
print "LOADING DATA -- UNIFIEDSTACK"
print "Existing Devices: " + str(Device.objects.all().count());
print "Existing Device Type Settings: " + str(DeviceTypeSetting.objects.all().count());
print "Existing Device Settings: " + str(DeviceSetting.objects.all().count());

print "CLEARING EXISTING SETTINGS"
DeviceTypeSetting.objects.all().delete()
Device.objects.all().delete()
DeviceSetting.objects.all().delete()

# TODO: Some Settings will belong to more than one devices. Try to relate the fields for multiple devices.
# Cobbler - Device
device = Device(
            title = "Cobbler - pxe boot",
            dtype = DeviceTypeSetting.COBBLER_TYPE,
            desc = "Used for life cycle mnanagement of networking devices"
        ).save()

# Cobbler - hostsetting
dtypesetting = DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.IP_TYPE,
                                         DeviceTypeSetting.MAC_TYPE, DeviceTypeSetting.CUSTOM_TYPE,
                                         DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Compute Host(Host Name; IP Address; MAC Address; Interface Type; Interface Name; Profile)",
                  standard_label="compute-host(host-name; ip-address; mac-address; interface-type; interface-name; profile)",
                  desc = "Compute hosts setting for cobbler. Could be also used by packstack.",
                  multiple = True,
                  ).save()

