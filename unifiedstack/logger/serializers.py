from rest_framework import serializers
from logger.models import Log, Device, ConsoleLog
from configurator.models import DeviceSetting

# Serializers define the API representation.
class LogSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(source='device')
    device_title = serializers.SlugRelatedField(source='device', slug_field='title', read_only=True) 
    class Meta:
        model = Log
        fields = ('id', 'level', 'message', 'timestamp', 'device_id', 'device_title')

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    logs = serializers.RelatedField(source='logs', many=True)
    settings = serializers.RelatedField(source='settings', many=True)
    class Meta:
        model = Device
        fields = ('id', 'title', 'desc', 'logs', 'settings')
        
class ConsoleLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
            model = ConsoleLog
            fields = ('id', 'console_summary', 'console_message')