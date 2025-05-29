from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login

from app01.models import UserFavourite, Merchant


# Create your views here.
@api_view(['POST'])
def register(request):
    username  = request.data.get('username')
    password = request.data.get('password')
    phone = request.data.get('phone')
    email = request.data.get('email')
    if username is None or password is None or phone is None or email is None:
        return Response({'error': '请把信息补充完整'},status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已存在'}, status=400)
    else :
        user = User.objects.create(
            username=username,
            password=make_password(password),  # 加密密码
            phone=phone,
            email=email
        )
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
        login(request, user)
        return Response({'message':'用户登陆成功！'},status = 200)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def info(request): #返回当前登录用户的所有信息
    user = request.user
    information = {
        'name':user.username,
        'phone':user.phone,
        'email':user.email
    }
    return JsonResponse(information,status=200)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def update(request):
    user = request.user
    username = request.data.get('username')
    password = request.data.get('password')
    phone = request.data.get('phone')
    email = request.data.get('email')
    if username:
        user.username = username
    if password:
        user.password = make_password(password)  # 加密新密码
    if phone:
        user.phone = phone
    if email:
        user.email = email
    user.save()
    return Response({'message':'修改用户信息成功'},status=200)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def favorite_merchant(request):
   user = request.user
   merchant_id = request.data.get('merchant_id')
   if UserFavourite.objects.filter(user_id = user.id , merchant_id=merchant_id).exists():
       return Response({'error':'当前商家已收藏'},status=400)
   UserFavourite.objects.create(user_id = user.id,merchant_id=merchant_id)
   return Response({'message':'收藏商家成功！'},status=200)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def favourite_dish(request):
    user = request.user
    dish_id = request.data.get('dish_id')
    if UserFavourite.objects.filter(user_id = user.id, dish_id=dish_id).exists():
        return Response({'error': '当前菜品已收藏'}, status=400)
    UserFavourite.objects.create(user_id=user.id, dish_id=dish_id)
    return Response({'message': '收藏菜品成功！'}, status=200)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def show_favourite(request):
    user = request.user
    favourite_list = UserFavourite.objects.filter(user_id = user.id)
    





