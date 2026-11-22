from rest_framework import serializers

from .models import Municipality, Position, PublicBody, PublicOfficial


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ["id", "name", "state", "ibge_code", "created_at", "updated_at"]


class PublicBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicBody
        fields = [
            "id",
            "municipality",
            "name",
            "acronym",
            "kind",
            "created_at",
            "updated_at",
        ]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "name", "created_at", "updated_at"]


class PublicOfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOfficial
        fields = [
            "id",
            "name",
            "public_body",
            "position",
            "email",
            "phone",
            "is_active",
            "created_at",
            "updated_at",
        ]
