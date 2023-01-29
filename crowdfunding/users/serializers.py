from rest_framework import serializers, validators
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


# Review later??
# ?
class ChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

# Review later???



# class ChangePasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         old_password = serializers.CharField(required=True)
#         new_password = serializers.CharField(required=True)


    # id = serializers.ReadOnlyField()
    # username = serializers.CharField(max_length=150)
    # email = serializers.EmailField()
    # password = serializers.CharField(max_length=150)




