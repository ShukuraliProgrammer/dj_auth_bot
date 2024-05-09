from django.urls import path
from .views import VerifyUserOTPCodeView

urlpatterns = [
    path('verify/', VerifyUserOTPCodeView.as_view(), name='verify_user_otp_code')
]