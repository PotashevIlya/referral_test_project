import random
from http import HTTPStatus

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from referall_app.models import (CHARACTERS_FOR_CONFCODE,
                                 CHARACTERS_FOR_INVITECODE,
                                 MAX_CONFCODE_LENGTH, MAX_INVITE_CODE_LENGTH,
                                 ReferallUser)
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsUserOnly
from .serializers import ProfileSerializer, SignupSerializer, TokenSerialiser
from .utils import send_sms_code

PHONE_NUMBER_EXISTS = 'Пользователь с номером {phone_number} уже существует'


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    """Вью для регистрации пользователя и отправки смс-кода"""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data['phone_number']
    try:
        user = ReferallUser.objects.create(phone_number=phone_number)
    except IntegrityError:
        raise serializers.ValidationError(
            PHONE_NUMBER_EXISTS.format(phone_number=phone_number)
        )
    user.confirmation_code = ''.join(random.choices(
        CHARACTERS_FOR_CONFCODE,
        k=MAX_CONFCODE_LENGTH
    )
    )
    user.save()
    send_sms_code(user.confirmation_code)
    return Response(
        {'phone_number': phone_number},
        status=HTTPStatus.OK
    )


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_token(request):
    """Вью для авторизации пользователя"""
    serializer = TokenSerialiser(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        ReferallUser,
        confirmation_code=serializer.validated_data['confirmation_code']
    )
    if not user.invitation_code:
        user.invitation_code = ''.join(random.choices(
            CHARACTERS_FOR_INVITECODE,
            k=MAX_INVITE_CODE_LENGTH
        )
        )
        user.save()
    return Response(
        data={'token': str(AccessToken.for_user(user))},
        status=HTTPStatus.OK
    )


class ProfileViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin
):
    """Вьюсет профиля пользователя"""
    serializer_class = ProfileSerializer
    queryset = ReferallUser.objects.all()
    permission_classes = (IsUserOnly,)
