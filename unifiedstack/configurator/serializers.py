from rest_framework import serializers
from configurator.models import DeviceTypeSetting, Device, DeviceSetting

# Serializers define the API representation.
class DeviceSettingSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device')
    device_type_setting_id = serializers.PrimaryKeyRelatedField(source='device_type_setting')
    #setting_id = serializers.PrimaryKeyRelatedField(source='compound_settings', required=False)
    device_title = serializers.SlugRelatedField(source='device', slug_field='title', read_only=True)
    class Meta:
        model = DeviceSetting
        # fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'setting_id', 'device_id', 'device_title', )
        fields = ('id', 'value', 'device_id', 'device_type_setting_id', 'device_title', )

class DeviceTypeSettingSerializer(serializers.HyperlinkedModelSerializer):
    values = serializers.RelatedField(source='values', many=True)
    #setting_id = serializers.PrimaryKeyRelatedField(source='compound_settings', required=False)
    class Meta:
        model = DeviceTypeSetting
        # fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'setting_id', 'device_id', 'device_title', )
        fields = ('id', 'dtype', 'stype', 'label', 'desc', 'standard_label', 'level', 'multiple', 'values',)

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    logs = serializers.RelatedField(source='logs', many=True)
    settings = serializers.RelatedField(source='settings', many=True)
    class Meta:
        model = Device
        fields = ('id', 'dtype', 'title', 'desc', 'logs', 'settings')        