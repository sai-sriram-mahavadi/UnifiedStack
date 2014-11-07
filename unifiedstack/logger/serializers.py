from rest_framework import serializers
from logger.models import Log, Device

# Serializers define the API representation.
class LogSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.PrimaryKeyRelatedField(source='device')
    class Meta:
        model = Log
        fields = ('id', 'log_message', 'log_timestamp', 'device',)

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    logs = serializers.RelatedField(many=True)
    class Meta:
        model = Device
        fields = ('id', 'device_desc', 'logs', )