from rest_framework import serializers
from .models import GeoPin, PinMemo

class PinCreateSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)

    def create(self, validated_data):
        user = self.context['request'].user
        return GeoPin.objects.create(
            author=user,
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude']
        )

class MemoCreateSerializer(serializers.Serializer):
    pin_id = serializers.IntegerField()
    content = serializers.CharField(trim_whitespace=True)

    def validate_pin_id(self, value):
        if not GeoPin.objects.filter(id=value).exists():
            raise serializers.ValidationError("Не существующая точка (по ID).")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        pin = GeoPin.objects.get(id=validated_data['pin_id'])
        return PinMemo.objects.create(
            pin=pin,
            author=user,
            content=validated_data['content']
        )

class PinOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPin
        fields = ['id', 'latitude', 'longitude', 'created_at']

class MemoOutputSerializer(serializers.ModelSerializer):
    pin_id = serializers.IntegerField(source='pin.id')
    latitude = serializers.FloatField(source='pin.latitude')
    longitude = serializers.FloatField(source='pin.longitude')

    class Meta:
        model = PinMemo
        fields = ['id', 'pin_id', 'content', 'created_at', 'latitude', 'longitude']