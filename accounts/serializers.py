from rest_framework import serializers

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email")
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user
    
    def validate(self, attrs):
        if len(attrs.get("password")) < 6:
            raise serializers.ValidationError({
                "password": "The lenght of password at least 6 character"
            })
        return attrs