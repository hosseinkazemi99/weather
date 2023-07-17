import re
from rest_framework import serializers
from .models import Post


class RegisterUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()

    def validate_mobile_number(self, value):
        if value.startswith('+989'):
            pattern = '^\+989\d{9}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError('Mobile number must be 13 digits and start with +98')
            return value
        elif value.startswith('09'):
            pattern = '^09(1[0-9]|2[1-3]|3[0-9]|0[0-9]|9[0-9])?[0-9]{7}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError('mobile number is not correct')
            value = '+98' + value[1:]
            return value
        else:
            raise serializers.ValidationError('mobile number is not correct')


class ValidatePhoneSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    otp = serializers.CharField()

    def validate_mobile_number(self, value):
        if value.startswith('+989'):
            pattern = '^\+989\d{9}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError('Mobile number must be 13 digits and start with +98')
            return value
        elif value.startswith('09'):
            pattern = '^09(1[0-9]|2[1-3]|3[0-9])?[0-9]{7}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError('mobile number is not correct')
            value = '+98' + value[1:]
            return value
        else:
            raise serializers.ValidationError('mobile number is not correct')

    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6 or not value.strip():
            raise serializers.ValidationError("OTP is not correct")
        return value


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=60)
    text = serializers.CharField(max_length=800)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'text', 'created_at', 'modified_at']
        read_only_fields = ['created_at', 'modified_at', 'id', 'owner']

    def update(self, instance, validated_data):

            instance.title = validated_data.get('title', instance.title)
            instance.text = validated_data.get('text', instance.text)
            instance.save()
            return serializers.ValidationError


