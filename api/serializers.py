from rest_framework import serializers


class UserMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)

    def validate_message(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Le champ 'message' ne peut pas etre vide.")
        return cleaned


class AIResponseSerializer(serializers.Serializer):
    response = serializers.CharField()

