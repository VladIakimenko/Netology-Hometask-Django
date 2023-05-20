from rest_framework import serializers

from .models import Sensor, Reading


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description',]


class ReadingSerializer(serializers.ModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all(), write_only=True)

    class Meta:
        model = Reading
        fields = ['sensor', 'temperature', 'created_at', 'photo']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = ReadingSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements',]