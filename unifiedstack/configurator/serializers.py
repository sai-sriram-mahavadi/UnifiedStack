from rest_framework import serializers
from configurator.models import DeviceSetting

# Serializers define the API representation.

class DeviceSettingSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device')
    #setting_id = serializers.PrimaryKeyRelatedField(source='compound_settings', required=False)
    device_title = serializers.SlugRelatedField(source='device', slug_field='title', read_only=True)
    class Meta:
        model = DeviceSetting
        # fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'setting_id', 'device_id', 'device_title', )
        fields = ('id', 'label', 'desc', 'stype', 'value', 'standard_label', 'device_id', 'device_title', )