from django.contrib.auth.models import User
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:  # type: ignore[misc]
        model = User
        fields = ["username", "first_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:  # noqa: PLR6301
        user = User(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
