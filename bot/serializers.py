from rest_framework import serializers


class GetAuthOTPCode(serializers.Serializer):
    code = serializers.IntegerField(required=True)
