from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from configurator.models import DeviceSetting
from configurator.serializers import DeviceSettingSerializer
from logger.serializers import LogSerializer
from logger.models import ConsoleLog   
import ConfigParser

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
# Create your views here.
@csrf_exempt
def device_settings_list(request, dpk):
    """
    List all logs, or create a new log.
    """
    if request.method == 'GET':
        settings = DeviceSetting.objects.filter(device_id=dpk)
        serializer = DeviceSettingSerializer(settings, many=True)
        return JSONResponse(serializer.data)

    
def configure(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("configurator/index.html", c, context_instance=RequestContext(request))

def sample(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("configurator/sample.html", c, context_instance=RequestContext(request))

# ViewSets define the view behavior.
class DeviceSettingViewSet(viewsets.ModelViewSet):
    queryset = DeviceSetting.objects.all()
    serializer_class = DeviceSettingSerializer
    
    
# Temporary binding with server itself ( no need for rest-api for this)
# Settings to be read from user (Configurator input fields)
GENERAL_SETTINGS = {
    'Name Server': ('name-server', 'default-name-server', 'M'),
    'Pool Id': ('pool-id', 'default-pool-id', 'M'),
    'Subrcibe': ('subscribe-id', 'default-id', 'M')
}
# Format <Input Field Label> : (<UCSM_Mapping_Label>, <Default_Value>,
#                                       <Field_Req>, <Field_Type>)
# <UCSM_Mapping_Label> is must for identifying the text control inputting desired field
# <Default_Value> is the one which is displayed as place holder in html page
#               (Default value if no other value provided)
# <Field_Req>: can be any of (Mandator, Basic, Optional, Advanced)
# <Field_Type>: can be any of (ALPHA, NUMERIC, ALPHA_NUMERIC, PASSWORD,
#                               IP, MULTIPLE_IP, COMPOUND, EMAIL, CUSTOM)
FI_SETTINGS = {
    'FI IPADDRESS':['fi-ip-address', '8.8.8.8', 'M'],
    'FI Descrition':['fi-description', 'fi-default-desc', 'M'],
}
COBBLER_SETTINGS = {
    'Compute Hosts': ('compute-hosts', 'compute-default-nodes', 'M'),
    'Network Hosts': ('network-hosts', 'network-default-nodes', 'M'),
}
SWITCH_SETTINGS = {
    'Host Name': ('host-name', 'default-host-name', 'M'),
    'User Name': ('user-name', 'default-user-name', 'M'),
}

SETTINGS = {}
SETTINGS["GENERAL_SETTINGS"] = GENERAL_SETTINGS
SETTINGS["FI_SETTINGS"] = FI_SETTINGS
SETTINGS["COBBLER_SETTINGS"] = COBBLER_SETTINGS
SETTINGS["SWITCH_SETTINGS"] = SWITCH_SETTINGS

@csrf_exempt
def server_binding_sample(request):
    c = {}
    c["request"] = request
    c["SETTINGS"] = SETTINGS
    context = RequestContext(request)
    return render_to_response("configurator/server_binding_sample.html", c, context_instance=RequestContext(request))
    # return HttpResponse("Hello World... This is Sriram's First app")


unified_config = ConfigParser.RawConfigParser()

def set_config_field(section, field, value):
    unified_config.set(section, field, value)
    
@csrf_exempt
def server_binding_post(request):
    print "post came from server_binding"
    data = JSONParser().parse(request)
    unified_config.add_section("general")
    unified_config.add_section("cobbler")
    unified_config.add_section("FI")
    unified_config.add_section("Switch")
    unified_config.add_section("Packstack")
    set_config_field("Default", "pool-id", data["general_pool_id"])
    set_config_field("Default", "name-server", data["general_name_server"])
    set_config_field("Default", "enable-fi", data["general_enable_fi"])
    set_config_field("Default", "hostname_port_mapping_1", data["general_hostname_port_mapping_1"])
    set_config_field("Default", "hostname_port_mapping_2", data["general_hostname_port_mapping_2"])
    set_config_field("Default", "hostname_port_mapping_3", data["general_hostname_port_mapping_3"])
    set_config_field("Default", "rhel_image_url", data["general_rhel_image_url"])
    set_config_field("Cobbler-Configuration", "compute_hosts", data["cobbler_compute_hosts"])
    set_config_field("Cobbler-Configuration", "network_hosts", data["cobbler_network_hosts"])
    set_config_field("Cobbler-Configuration", "profiles", data["cobbler_profiles"])
    set_config_field("Cobbler-Configuration", "cobbler_interface", data["cobbler_interface"])
    set_config_field("Cobbler-Configuration", "cobbler_ipaddress", data["cobbler_ipaddress"])
    set_config_field("Cobbler-Configuration", "cobbler_netmask", data["cobbler_netmask"])
    set_config_field("Cobbler-Configuration", "cobbler_server", data["cobbler_server"])
    set_config_field("Cobbler-Configuration", "cobbler_next_server", data["cobbler_next_server"])
    set_config_field("Cobbler-Configuration", "cobbler_subnet", data["cobbler_subnet"])
    set_config_field("Cobbler-Configuration", "cobbler_option_router", data["cobbler_option_router"])
    set_config_field("Cobbler-Configuration", "cobbler_DNS", data["cobbler_DNS"])
    set_config_field("Cobbler-Configuration", "cobbler_hostname", data["cobbler_hostname"])
    set_config_field("Cobbler-Configuration", "cobbler_web_username", data["cobbler_web_username"])
    set_config_field("Cobbler-Configuration", "cobbler_web_password", data["cobbler_web_password"])
    set_config_field("Cobbler-Configuration", "redhat_username", data["redhat_username"])
    set_config_field("Cobbler-Configuration", "redhat_password", data["redhat_password"])
    set_config_field("Cobbler-Configuration", "redhat_pool", data["redhat_pool"])
    set_config_field("Cobbler-Configuration", "cobbler_netmask", data["cobbler_netmask"])
    set_config_field("Cobbler-Configuration", "proxy", data["cobbler_proxy"])
    set_config_field("Cobbler-Configuration", "power_type", data["cobbler_power_type"])
    set_config_field("FI-Configuration", "fi-Cluster_IP", data["FI_Cluster_IP"])
    set_config_field("FI-Configuration", "fi-Cluster_Username", data["FI_Cluster_Username"])
    set_config_field("FI-Configuration", "fi-Cluster_Password", data["FI_Cluster_Password"])
    set_config_field("FI-Configuration", "fi-Server_Ports", data["FI_Server_Ports"])
    set_config_field("FI-Configuration", "fi-Uplink_Ports", data["FI_Uplink_Ports"])
    set_config_field("FI-Configuration", "fi-Slot_Id", data["FI_Slot_Id"])
    set_config_field("FI-Configuration", "fi-Slot_1_ports", data["FI_Slot_1_ports"])
    set_config_field("FI-Configuration", "fi-UUID_pool_name", data["FI_UUID_pool_name"])
    set_config_field("FI-Configuration", "fi-UUID_pool_start", data["FI_UUID_pool_start"])
    set_config_field("FI-Configuration", "fi-UUID_pool_end", data["FI_UUID_pool_end"])
    set_config_field("FI-Configuration", "fi-MAC_pool_name", data["FI_MAC_pool_name"])
    set_config_field("FI-Configuration", "fi-MAC_pool_start", data["FI_MAC_pool_start"])
    set_config_field("FI-Configuration", "fi-MAC_pool_end", data["FI_MAC_pool_end"])
    set_config_field("FI-Configuration", "fi-vnic_1_name", data["FI_vnic_1_name"])
    set_config_field("FI-Configuration", "fi-vnic_1_vlan_range", data["FI_vnic_1_vlan_range"])
    set_config_field("FI-Configuration", "fi-vnic_2_name", data["FI_vnic_2_name"])
    set_config_field("FI-Configuration", "fi-vnic_2_vlan_range", data["FI_vnic_2_vlan_range"])
    set_config_field("FI-Configuration", "fi-vnic_3_name", data["FI_vnic_3_name"])
    set_config_field("FI-Configuration", "fi-vnic_3_vlan_range", data["FI_vnic_3_vlan_range"])
    set_config_field("FI-Configuration", "fi-Service_profile_name", data["FI_Service_profile_name"])
    set_config_field("FI-Configuration", "general_pool_id", data["general_pool_id"])
    set_config_field("Switch-Configuration", "Available-Switches", data["Switch_available_switches"])
    set_config_field("Switch-Configuration", "9k-ip-address", data["Switch_1_Ip_address"])
    set_config_field("Switch-Configuration", "9k-username", data["Switch_1_username"])
    set_config_field("Switch-Configuration", "9k-password", data["Switch_1_password"])
    set_config_field("Switch-Configuration", "vlan", data["Switch_1_vlan"])
    set_config_field("Switch-Configuration", "trunk_interfaces", data["Switch_1_trunk_interfaces"])
    set_config_field("Switch-Configuration", "vrf", data["Switch_1_VRF"])
    set_config_field("Switch-Configuration", "management-interface", data["Switch_1_Mgmt_interface"])
    set_config_field("Packstack", "Packstack_compute_hosts", data["Packstack_compute_hosts"])
    set_config_field("Packstack", "Packstack_network_hosts", data["Packstack_network_hosts"])
    set_config_field("Packstack", "Packstack_admin_pw", data["Packstack_admin_pw"])
    set_config_field("Packstack", "Packstack_enable_openswitch", data["Packstack_enable_openswitch"])
    set_config_field("Packstack", "Packstack_enable_cisconexus", data["Packstack_enable_cisconexus"])
    set_config_field("Packstack", "Packstack_vlan_mapping_ranges", data["Packstack_vlan_mapping_ranges"])
    
    with open('config.cfg', 'wb') as configfile:
        unified_config.write(configfile)
        
    print "Data: ", data
    print data["general_pool_id"]
    print data["general_name_server"]
    cl = ConsoleLog(console_summary="Posted Genaral_Pool_ID:" + data["general_pool_id"])
    cl.save()
    return HttpResponse(status=201)

