
from .views import Base64Encryption, AESEncryption, CacheView
from django.urls import path, include

urlpatterns = [
    path('base64/', Base64Encryption.as_view()),
    path('aes/', AESEncryption.as_view()),
    path('cache/', CacheView.as_view()),
]
