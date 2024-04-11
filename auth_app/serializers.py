from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
  
  email = serializers.EmailField()
  name = serializers.CharField(max_length = 100)
  password = serializers.CharField(max_length = 100)
  

class LoginSerializer(serializers.Serializer):
  
  email = serializers.EmailField()
  password = serializers.CharField(max_length = 100)