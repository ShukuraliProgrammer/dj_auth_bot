from django.contrib import admin

from bot.models import User, AuthSms

admin.site.register(User)
admin.site.register(AuthSms)
