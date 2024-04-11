from rest_framework import serializers

# class SeatSerializer(serializers.Serializer):
#   seat_no = serializers.CharField(max_length =3)

class TheatreSerializer(serializers.Serializer):
  
  theatre_name = serializers.CharField()
  seat_layout = serializers.ListField(child = serializers.ListField(child = serializers.CharField(max_length = 3)))
  
