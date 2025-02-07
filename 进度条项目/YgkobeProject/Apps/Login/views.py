from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.request import Request
from rest_framework import generics, status
from .models import User
from rest_framework.permissions import AllowAny


class Login(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        result = serializer.validated_data
        result['username'] = serializer.user.username
        result['token'] = result.pop('access')

        return Response(result, status=status.HTTP_200_OK)


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1 接收用户参数
        username = request.data.get('username')
        password = request.data.get('password')
        password_confirmation = request.data.get('confirmPassword')

        # 2 校验参数
        if not all([username, password, password_confirmation]):
            return Response({'error': '所有参数不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password_confirmation:
            return Response({'error': '两次输入都密码不一致'}, status=status.HTTP_400_BAD_REQUEST)

        obj = User.objects.create_user(username=username,  password=password)

        response = {
            'username': username,
            'id': obj.id,
        }

        return Response(response, status=status.HTTP_201_CREATED)



