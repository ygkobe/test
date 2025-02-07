from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = ChatMessage
        fields = '__all__'
