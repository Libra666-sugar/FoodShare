from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def register(request):
    username  = request.data.get('username')
    password = request.data.get('password')
    phone = request.data.get('phone')
    email = request.data.get('email')
    if username is None or password is None or phone is None or email is None:
        return Response({'error': '请把信息补充完整'},status=400)
    else :
        return Response({'message': '创建个人账户成功！'},status=201)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user is None:
        return Response({'error':'用户名不存在，请重新输入'},status=400)
    elif password != user.password:
        return Response({'error':'用户密码错误，请重新输入'},status = 400)
    else :
        return Response({'message':'用户登陆成功！'},status = 200)

@api_view(['GET'])
def info(request): #获取用户信息
    



