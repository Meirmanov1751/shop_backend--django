from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from user import WRONG_CODE_ERROR_MESSAGE
from user.models import User
from user.serializers import CheckCodeSerializer, UserSerializer
from utils.code_caching import check_code_from_cache


class LoginException(Exception):
    pass


def login(request, context, filterset={}):
    serializer = CheckCodeSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['phone'].strip().lower()
    code = serializer.data.get('code', None)
    if not check_code_from_cache(username, code):
        raise ValidationError(WRONG_CODE_ERROR_MESSAGE)
    try:
        queryset = User.objects.filter(
            Q(phone__contains=username)
        )
        if filterset:
            print(filterset)
            queryset = queryset.filter(**filterset)
            print(queryset)
        user = queryset[0]
        user_serializer = UserSerializer(user, context=context)
        token = RefreshToken.for_user(user=user)
        data = user_serializer.data
        data["token"] = str(token.access_token)
        data['is_new'] = False
        return data
    except IndexError:
        raise LoginException
