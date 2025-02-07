from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
import datetime
User = get_user_model()


class CustomTokenObtainPairView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 验证用户凭证
        user = authenticate(request, username=username, password=password)
        # print('auth user.....')
        # print(user)     # wangze
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)
        # print(type(refresh))
        access = refresh.access_token
        # created_at = refresh['iat']
        created_at = refresh['iat']
        # 将时间戳转换为 datetime 对象
        dt_object = datetime.datetime.fromtimestamp(created_at)
        # 格式化日期时间
        created_at = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        expires_at = refresh['exp']
        # 将时间戳转换为 datetime 对象
        dt_object = datetime.datetime.fromtimestamp(expires_at)
        # 格式化日期时间
        expires_at = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        # 自定义返回值
        custom_response_data = {
            # "refresh": str(refresh),
            "token": str(access),
            "username": user.username,
            # "email": user.email,
            "created_at": created_at,
            "expires_at": expires_at


        }
        return Response(custom_response_data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        is_superuser = True if data.get('is_superuser') == "true" else False

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建用户
        try:
            user = User.objects.create(
                username=username,
                password=make_password(password),  # 使用make_password来加密密码
                is_superuser=is_superuser
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': username,
            "is_superuser": is_superuser
        })
