import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .models import User
from .serializers import GetAuthOTPCode
from bot.management.commands.run_bot import bot
import jwt


class VerifyUserOTPCodeView(APIView):
    serializer_class = GetAuthOTPCode

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = GetAuthOTPCode(data=data)
            if not serializer.is_valid():
                return Response({'message': 'Invalid data'}, status=400)
            code = data['code']
            user_id = cache.get(code)
            if not user_id:
                return Response({'message': 'Code was expired'}, status=400)
            data = bot.get_chat(user_id)
            new_user, created = User.objects.get_or_create(telegram_id=data.id, first_name=data.first_name,
                                                           last_name=data.last_name, username=data.username)
            cache.delete(code)
            user_data = {
                "first_name": new_user.first_name,
                "username": new_user.username,
                "id": new_user.id
            }
            encoded_jwt = jwt.encode({"data": user_data}, "secret", algorithm="HS256")
            return Response(
                {'message': 'User verified successfully', 'data': {"token": encoded_jwt, "user": user_data}}, status=200)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
