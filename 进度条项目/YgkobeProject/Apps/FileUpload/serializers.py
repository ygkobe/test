from rest_framework import serializers
from .models import CarNumberInfo


class CarNumberInfoSerializers(serializers.ModelSerializer):

    class Meta:
        model = CarNumberInfo
        fields = '__all__'


