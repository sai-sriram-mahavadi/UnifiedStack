from django.db import models
from logger.models import Device
# Create your models here.
# Format <Input Field Label> : (<UCSM_Mapping_Label>, <Default_Value>,
#                                       <Field_Req>, <Field_Type>)
# <UCSM_Mapping_Label> is must for identifying the text control inputting desired field
# <Default_Value> is the one which is displayed as place holder in html page
#               (Default value if no other value provided)
# <Field_Req>: can be any of (Mandator, Basic, Optional, Advanced)
# <Field_Type>: can be any of (ALPHA, NUMERIC, ALPHA_NUMERIC, PASSWORD,
#                               IP, MULTIPLE_IP, COMPOUND, EMAIL, CUSTOM)
class DeviceSetting(models.Model):
    MANDATORY_LEVEL = 'M'
    BASIC_LEVEL = 'B'
    OPTIONAL_LEVEL = 'O'
    ADVANCED_LEVEL = 'A'

    SETTING_LEVEL_CHOICES = (
        (MANDATORY_LEVEL, 'Mandatory'),
        (BASIC_LEVEL, 'Basic'),
        (OPTIONAL_LEVEL, 'Optional'),
        (ADVANCED_LEVEL, 'Advanced'),
    )
    
    ALPHA_TYPE = 'A'
    NUMERIC_TYPE = 'N'
    ALPHA_NUMERIC_TYPE = 'AN'
    PASSWORD_TYPE = 'P'
    IP_TYPE = 'IP'
    MULTIPLE_IP_TYPE = 'MI'
    COMPOUND_TYPE = 'C'
    EMAIL_TYPE = 'E'
    CUSTOM_TYPE = 'CU'
    
    SETTING_TYPE_CHOICES = (
        (ALPHA_TYPE, 'Aphabetic'),
        (NUMERIC_TYPE, 'Numeric'),
        (ALPHA_NUMERIC_TYPE, 'Alpha Numeric'),
        (PASSWORD_TYPE, 'Password'),
        (IP_TYPE, 'IPv4 Address'),
        (MULTIPLE_IP_TYPE, 'Multiple IP Addresses'),
        (COMPOUND_TYPE, 'Compound Setting'),
        (EMAIL_TYPE, 'Email'),
        (CUSTOM_TYPE, 'Custom'),
    )
    
    device = models.ForeignKey(Device, related_name="settings")
    # compond_settings = models.ForeignKey('self', related_name="compound_settings", null=True)
    # compond_settings = models.ManyToManyField('self', null=True)
    label = models.CharField(max_length=50, blank=False)
    desc = models.CharField(max_length=100, blank=True, default="")
    level = models.CharField(max_length=1, choices=SETTING_LEVEL_CHOICES,
                                    default=BASIC_LEVEL)
    stype = models.CharField(max_length=2, choices=SETTING_TYPE_CHOICES,
                                    default=ALPHA_NUMERIC_TYPE)
    standard_label = models.CharField(max_length=50, blank=True, default="")
    value = models.CharField(max_length=200, blank=True, default="") #  compound settings are generally blank
    
    def __str__(self):
        return self.label + ": " + self.level + ", " + self.stype + ", " + self.value


    