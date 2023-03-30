from random import random

from django.core import cache
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from user import WRONG_CODE_ERROR_MESSAGE, SAME_PHONE_EXISTS
from user.models import User
from user.serializers import CheckCodeSerializer, LoginSerializer, UserSerializer
from user.services.login import login, LoginException
from utils.code_caching import generate_code_and_cache, check_code_from_cache
from utils.validate_phone import validate_phone
from rest_framework.mixins import UpdateModelMixin


class UserViewSet(UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def check_code(self, request, *args, **kwargs):
        serializer = CheckCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        username = data['phone']
        code = data['code']
        if 'update' in request.data and request.data['update'] == "true":
            key = 'username_%s_change_code' % username
            test_code = cache.get(key, None)
            if test_code is None or code != test_code:
                return Response(status=401, data={'isCodeCorrect': False})
            return Response(status=200, data={'isCodeCorrect': True})
        if check_code_from_cache(username, code):
            return Response(status=200, data={'isCodeCorrect': True})
        return Response(status=200, data={'isCodeCorrect': False})

    @action(detail=False, methods=['post'])
    def send_code(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        username = data['phone']
        role = data['role']
        if role == User.ROLES.MASTER or role == User.ROLES.MANAGEMENT_COMPANY:
            user = User.objects.filter(Q(phone__contains=username)).filter(role=role)
            if not user.exists():
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "Пользователь не найден"})
        if 'update' in request.data and request.data['update'] == "true":
            code = generate_code_and_cache(username, True)
        else:
            code = generate_code_and_cache(username)
        return Response(status=status.HTTP_200_OK, data={'phone': username, 'code': code})

    @action(detail=False, methods=["post"])
    def login_or_register(self, request, *args, **kwargs):
        try:
            user_data = login(request, self.get_renderer_context())
            serializer = LoginSerializer
            return Response(data=user_data)
        except LoginException:
            # register if user didn't found
            serializer = CheckCodeSerializer(data=request.data, context=self.get_renderer_context())
            serializer.is_valid()
            username = serializer.data['phone'].strip().lower()
            user = User.objects.create_user(username)
            user_serializer = UserSerializer(user, context=self.get_renderer_context())
            token = RefreshToken.for_user(user=user)
            data = user_serializer.data
            data["token"] = str(token.access_token)
            data['is_new'] = True
            return Response(data=data)

    @action(detail=False, methods=["post"])
    def mc_login(self, request, *args, **kwargs):
        # login for management company
        try:
            user_data = login(request, self.get_renderer_context(), {"role": User.ROLES.MANAGEMENT_COMPANY})
            return Response(data=user_data)
        except LoginException:
            raise AuthenticationFailed()

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        data = UserSerializer(self.request.user, context=self.get_renderer_context()).data
        return Response(status=200, data=data)

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    def update_user(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = user.phone
        print('instance phone', user.phone)
        if phone is not None and phone != user.phone:
            same_phone = User.objects.filter(phone=request.data['phone'])
            if same_phone.exists():
                raise ValueError(SAME_PHONE_EXISTS)
            validate_phone(phone)
            serializer.validated_data['phone'] = phone
        self.perform_update(serializer)
        user = User.objects.get(pk=user.id)
        data = UserSerializer(instance=user, context=self.get_renderer_context())
        return Response(data.data)
