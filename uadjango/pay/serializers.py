from rest_framework import serializers
from .models import Reservations

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = '__all__'
