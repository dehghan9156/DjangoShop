from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from ...models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=250,write_only=True)
    class Meta:
        model = User
        fields = ["email","password","confirm_password"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"detail": "Passwords do not match"})

        password = attrs.get("password")
        if password:  # ✅ فقط در صورتی که `password` مقدار داشته باشد، بررسی کن
            try:
                validate_password(password)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({"password": list(e.messages)})

        return attrs  # ✅ مقدار اصلاح‌شده را برمی‌گردانیم

    def create(self, validated_data):
        validated_data.pop("confirm_password",None)
        return User.objects.create_user(**validated_data)

class TokenCustomObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)
        data["email"] = self.user.email
        data["user_id"] = self.user.pk
        return data