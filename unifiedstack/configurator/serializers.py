from rest_framework import serializers
from configurator.models import DeviceSetting, SimpleProperty

# Serializers define the API representation.

class DeviceSettingSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device')
    properties = serializers.RelatedField(source='compound_settings', many=True)
    #setting_id = serializers.PrimaryKeyRelatedField(source='compound_settings', required=False)
    device_title = serializers.SlugRelatedField(source='device', slug_field='title', read_only=True)
    
    class Meta:
        model = DeviceSetting
        # fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'setting_id', 'device_id', 'device_title', )
        fields = ('id', 'label', 'desc', 'standard_label', 'level', 'multiple', 'device_id', 'device_title', 'properties',)
        
class SimplePropertySerializer(serializers.HyperlinkedModelSerializer):
    device_setting_id = serializers.PrimaryKeyRelatedField(source='device_setting')
    #setting_id = serializers.PrimaryKeyRelatedField(source='compound_settings', required=False)
    #device_title = serializers.SlugRelatedField(source='compound_settings', slug_field='title', read_only=True)
    class Meta:
        model = SimpleProperty
        # fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'setting_id', 'device_id', 'device_title', )
        fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'device_setting_id', )
        
        