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
device_cobbler = Device(
                   title = "Cobbler - pxe boot",
                   dtype = DeviceTypeSetting.COBBLER_TYPE,
                   desc = "Used for life cycle mnanagement of networking devices"
                   ).save()
device_foreman = Device(
                   title = "Foreman - pxe boot",
                   dtype = DeviceTypeSetting.FOREMAN_TYPE,
                   desc = "Used for life cycle mnanagement of networking devices"
                   ).save()
device_fi = Device(
                   title = "FI - Physical machine creator",
                   dtype = DeviceTypeSetting.FI_TYPE,
                   desc = "Used for creation of physical machines using Fabric Interface"
                   ).save()
device_switch = Device(
                   title = "Switch - configurator",
                   dtype = DeviceTypeSetting.SWITCH_TYPE,
                   desc = "Used for Configuring Switches"
                   ).save()
device_packstack = Device(
                   title = "Packstack - Openstack installer and Configurator",
                   dtype = DeviceTypeSetting.PACKSTACK_TYPE,
                   desc = "Used for installation of Openstack"
                   ).save()
device_general = Device(
                   title = "General",
                   dtype = DeviceTypeSetting.GENERAL_TYPE,
                   desc = "Used for keeping common values shared by multiple sections"
                   ).save()


# Cobbler - hostsetting
dtypesetting = DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.IP_TYPE,
                                         DeviceTypeSetting.MAC_TYPE, DeviceTypeSetting.CUSTOM_TYPE,
                                         DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Compute Host(Host Name; IP Address; MAC Address; Interface Type; Interface Name; Associated Profile Name)",
                  standard_label="compute-host(host-name; ip-address; mac-address; interface-type; interface-name; profile)",
                  desc = "Compute hosts setting for cobbler. Could be also used by packstack",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.IP_TYPE,
                                         DeviceTypeSetting.MAC_TYPE, DeviceTypeSetting.CUSTOM_TYPE,
                                         DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Network Host(Host Name; IP Address; MAC Address; Interface Type; Interface Name; Associated Profile Name)",
                  standard_label="network-host(host-name; ip-address; mac-address; interface-type; interface-name; profile)",
                  desc = "Network hosts setting for cobbler. Could be also used by packstack.",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Profile(Profile Name; OS Image Name)",
                  standard_label="profile(profile-name; distro)",
                  desc = "Profile to be used by the Hosts.",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "OS Distribution Image Name",
                  standard_label="distro",
                  desc = "Name of the RHEL mirror",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Cobbler Interface",
                  standard_label="cobbler-interface",
                  desc = "Interface which cobbler should use for PXE booting",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Cobbler Server IP ",
                  standard_label="cobbler-server",
                  desc = "IP Address of the system on which cobbler should run",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Cobbler Next Server IP ",
                  standard_label="cobbler-next-server",
                  desc = "IP Address of the system if there is another cobbler server is in the network or same as above",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Subnet IP ",
                  standard_label="cobbler-subnet",
                  desc = "IP address of the subnet in which cobbler should run",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Netmask",
                  standard_label="cobbler-netmask",
                  desc = "Network Mask of the subnet",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Gateway IP Address",
                  standard_label="cobbler-option-router",
                  desc = "Default Gateway IP address",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Domain Name Server IP",
	          standard_label="cobbler-DNS",
                  desc = "Nameserver of the subnet",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Cobbler Hostname",
                  standard_label="cobbler-hostname",
                  desc = "Hostname of the system on which cobbler should run",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.PASSWORD_TYPE]),
                  label = "Cobbler Web(Username; Password)",
                  standard_label="cobbler-web(cobbler-web-username; cobbler-web-password",
                  desc = "Username and Password through which cobbler web will be accessed",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.PASSWORD_TYPE, 
					 DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Redhat Registration and Subscription(Username; Password; Pool ID)",
                  standard_label="redhat-info(redhat-username; redhat-password; redhat-pool)",
                  desc = "Redhat account information through which system should be registered and sunscribed to redhat.",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.OPTIONAL_LEVEL,
                  dtype = DeviceTypeSetting.COBBLER_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE,DeviceTypeSetting.IP_TYPE,DeviceTypeSetting.NUMERIC_TYPE]),
                  label = "Proxy (Http Proxy IP; Https Proxy IP; Https Proxy Port)",
                  standard_label = "proxy(http-proxy-ip; https-proxy-ip; https-port)",
                  desc = "If the network has web proxy ",
                  multiple = False,
                  ).save()

#General Section
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Domain Name Server IP",
                  standard_label = "name-server",
                  desc = "IP address of the Domain Name Server in the subnet",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_TYPE]),
                  label = "FI Enabled",
                  standard_label="enable-fi",
                  desc = "Checks whether to enable Fi or not",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Host System IP Address",
                  standard_label="host-ip-address",
                  desc = "IP address  of this system",
                  multiple = False,
                  ).save()
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.PASSWORD_TYPE]),
                  label = "Host System Password",
                  standard_label="host-password",
                  desc = "Password of this system",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "RHEL Image URL",
                  standard_label="rhel-image-url",
                  desc = "URL of the redhat enterprise linux 7 mirror ",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_TYPE]),
                  label = "Life Cycle Manager",
                  standard_label="life-cycle-manager",
                  desc = "Life Cycle manager to be used. Either Foreman or Cobbler",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.GENERAL_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_TYPE]),
                  label = "Openstcack Provisoner",
                  standard_label="openstack-provisioner",
                  desc = "Specify the Openstack Provisioner to be used",
                  multiple = False,
                  ).save()


#Foreman Section
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.IP_TYPE,
                                         DeviceTypeSetting.MAC_TYPE]),
                  label = "Compute Host(Host Name; IP Address; MAC Address)",
                  standard_label="compute-host(host-name; ip-address; mac-address)",
                  desc = "Compute hosts setting for Foreman. Could be also used by packstack",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE, DeviceTypeSetting.IP_TYPE,
                                         DeviceTypeSetting.MAC_TYPE]),
                  label = "Network Host(Host Name; IP Address; MAC Address)",
                  standard_label="network-host(host-name; ip-address; mac-address)",
                  desc = "Network hosts setting for Foreman. Could be also used by packstack.",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Foreman Server IP ",
                  standard_label="foreman-ip-address",
                  desc = "IP address of the foreman system",
                  multiple = False,
                  ).save()
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Foreman Server Hostname ",
                  standard_label="foreman-hostname",
                  desc = "IP address of the foreman system",
                  multiple = False,
                  ).save()


DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Domain Name",
                  standard_label="domain-name",
                  desc = "Domain Name",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Domain Name Server IP",
                  standard_label="DNS",
                  desc = "",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Gateway IP",
                  standard_label="option-router",
                  desc = "IP address of the default gateway in the subnet",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "NETMASK",
                  standard_label="netmask",
                  desc = "Network Mask of the subnet",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Subnet IP",
                  standard_label="subnet",
                  desc = "IP Address of the subnet",
                  multiple = False,
                  ).save()


DeviceTypeSetting(
                  level = DeviceTypeSetting.OPTIONAL_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE,DeviceTypeSetting.IP_TYPE,DeviceTypeSetting.NUMERIC_TYPE]),
                  label = "Proxy (Http Proxy IP; Https Proxy IP; Https Port",
                  standard_label="proxy(http-proxy-ip; https-proxy-ip; https-port)",
                  desc = "If the network has web proxy ",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FOREMAN_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.PASSWORD_TYPE,
                                         DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Redhat Registration and Subscription(Username; Password; Pool ID)",
                  standard_label="redhat-info(redhat-username; redhat-password; redhat-pool)",
                  desc = "Redhat account information through which system should be registered and sunscribed to redhat.",
                  multiple = True,
                  ).save()
#FI Section
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_TYPE]),
                  label = "IS Mgmt Native Vlan",
                  standard_label="fi-mgmt-native-vlan",
                  desc = "Should management native vlan be true",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "FI Cluster IP Address",
                  standard_label="fi-cluster-ip-address",
                  desc = "IP Address of the Cluster",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI Cluster Username",
                  standard_label="fi-cluster-username",
                  desc = "Username of the FI Cluster",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.PASSWORD_TYPE]),
                  label = "FI Cluster Password",
                  standard_label="fi-cluster-password",
                  desc = "Password of the FI Cluster",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI Server Ports",
                  standard_label="fi-server-ports",
                  desc = "Comma Separated List of Ports",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI UPLink Ports ",
                  standard_label="fi-uplink-ports",
                  desc = "Comma Separated list of Uplink Ports ",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI Slot(SLOT ID; PORTS)",
                  standard_label="fi-slot(slot-id; slot-ports)",
                  desc = "Slot ID and comma separated list of ports associated with the slot id",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.ALPHA_NUMERIC_TYPE,
					DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI UUID Pool(Name; Range Start; Range End)",
                  standard_label="fi-uuid-pool(fi-uuid-pool-name; fi-uuid-pool-start; fi-uuid-pool-end)",
                  desc = "UUID Pool",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.MAC_TYPE,
					 DeviceTypeSetting.MAC_TYPE]),
                  label = "FI MAC Pool(Name; Range Start; Range End)",
                  standard_label="fi-mac-pool(fi-mac-pool-name; fi-mac-pool-start; fi-mac-pool-end)",
                  desc = "MAC Pool",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.IP_TYPE,
                                         DeviceTypeSetting.IP_TYPE,DeviceTypeSetting.IP_TYPE,
					 DeviceTypeSetting.IP_TYPE]),
                  label = "FI IP Pool(Name; Range Start; Range End; Default-Gateway; Subnet)",
                  standard_label="fi-ip-pool(fi-ip-pool-name; fi-ip-pool-start; fi-ip-pool-end; default-gateway; subnet)",
                  desc = "IP POOL",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.NUMERIC_TYPE,
					DeviceTypeSetting.NUMERIC_TYPE]),
                  label = "fi-vnic(name; Vlan Range Start,Vlan Range End)",
                  standard_label="fi-vnic(name; vlan-range-start;vlan-range-end)",
                  desc = "FI Virtual NIC name and vlan range associated with vnic",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI Service Profile Name",
                  standard_label="fi-service-profile-name",
                  desc = "FI Service Profile Name",
                  multiple = False,
                  ).save()     
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
		  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
		  label = "FI Boot policy Name"
		  standard_label="fi-boot-policy-name"
		  desc = "FI Boot policy Name"
		  multiple = false
		  }.save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.FI_TYPE,
		  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "FI Boot VNIC"
                  standard_label="fi-boot-vnic"
                  desc = "FI Boot VNIC"
                  multiple = false
                  }.save()

#Packstack Section
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.PACKSTACK_TYPE,
                  stype = values_to_str([DeviceTypeSetting.PASSWORD_TYPE]),
                  label = "Keystone Admin Password",
                  standard_label="keystone-admin-pw",
                  desc = "Admin Password for the Keystone Service",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.PACKSTACK_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Enable Openvswitch(True/False)",
                  standard_label="enable-openvswitch",
                  desc = "Enter True if OpenvSwitch is to be enabled else false",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.PACKSTACK_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Enable Cisco Nexus(True:False)",
                  standard_label="enable-cisconexus",
                  desc = "Enter True if Cisco Nexus is to be enabled else fals",
                  multiple = True,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.PACKSTACK_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "vlan-mapping-ranges",
                  standard_label="vlan-mapping-ranges",
                  desc = "Enter the vlan mapping ranges. (start : end)",
                  multiple = True,
                  ).save()


#Switch Section
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Switch Type",
                  standard_label="switch-type",
                  desc = "Switch Type",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "HOSTNAME",
                  standard_label="hostname",
                  desc = "Hostname of the switch",
                  multiple = False,
                  ).save()
DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.IP_TYPE]),
                  label = "Management IP Address",
                  standard_label="ip-address",
                  desc = "IP Address of the management interface",
                  multiple = False,
                  ).save()

DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Username",
                  standard_label="username",
                  desc = "Username",
                  multiple = True,
                  ).save()


DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.PASSWORD_TYPE]),
                  label = "Password",
                  standard_label="password",
                  desc = "password",
                  multiple = False,
                  ).save()


DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.IP_TYPE,
					 DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "VLAN(ID; IP ; Netmask)",
                  standard_label="vlan(id; ip; netmask)",
                  desc = "Vlan specific information",
                  multiple = True,
                  ).save()


DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.ALPHA_NUMERIC_TYPE,
				        DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Interface (Name; Type; Description; Vlan)",
                  standard_label="interface(name; type; description; vlan)",
                  desc = "Information specific to the Interface. Vlan is comma separated list",
                  multiple = True,
                  ).save()


DeviceTypeSetting(
                  level = DeviceTypeSetting.BASIC_LEVEL,
                  dtype = DeviceTypeSetting.SWITCH_TYPE,
                  stype = values_to_str([DeviceTypeSetting.ALPHA_NUMERIC_TYPE,DeviceTypeSetting.ALPHA_NUMERIC_TYPE]),
                  label = "Port Channel(Number; Interfaces)" ,
                  standard_label="port-channel(number; interfaces)",
                  desc = "Port Channel Number and comma separated list of Interfaces associated with the port channel",
                  multiple = True,
                  ).save()


