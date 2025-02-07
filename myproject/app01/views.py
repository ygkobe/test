from django.shortcuts import render
import base64
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache
from .encrypt import aes_encrypt


class Base64Encryption(APIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request):

        # Base64 编码的字符串
        # encoded_str = "SGVsbG8sIFdvcmxkIQ=="
        #
        # # 将编码后的字符串转换为字节
        # encoded_bytes = encoded_str.encode('utf-8')
        #
        # # 对字节数据进行Base64解码
        # decoded_bytes = base64.b64decode(encoded_bytes)
        #
        # # 将解码后的字节数据转换为字符串
        # decoded_str = decoded_bytes.decode('utf-8')

        # 原始数据
        data = "Hello, World!"

        # 将数据编码为字节
        data_bytes = data.encode('utf-8')

        # 对字节数据进行Base64编码
        encoded_bytes = base64.b64encode(data_bytes)

        # 将编码后的字节数据转换为字符串
        encoded_str = encoded_bytes.decode('utf-8')

        # print(f"Decoded: {decoded_str}")
        data = {
            "result": encoded_str
        }

        return Response(data)


class AESEncryption(APIView):
    # permission_classes = (AllowAny,)

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = "Hello, World!"
        result = aes_encrypt(data)
        # data1 = {
        #     "result": result
        # }

        return Response(result)


class CacheView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        # 尝试从缓存中获取数据
        data = cache.get('my_key')
        import datetime
        if not data:
            # 如果缓存中没有数据，执行逻辑生成数据
            data = "cached data:  " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 将数据存储到缓存中，缓存时间为60秒
            cache.set('my_key', data, timeout=5)

        return Response(data)
