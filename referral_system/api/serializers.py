from referall_app.models import (MAX_CONFCODE_LENGTH, MAX_PHONE_NUMBER_LENGTH,
                                 ReferallUser)
from referall_app.validators import validate_phone_number
from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя"""
    phone_number = serializers.CharField(
        max_length=MAX_PHONE_NUMBER_LENGTH,
        required=True
    )

    def validate_phone_number(self, phone_number):
        return validate_phone_number(phone_number)


class TokenSerialiser(serializers.Serializer):
    """Сериализатор авторизации пользователя"""
    confirmation_code = serializers.CharField(
        max_length=MAX_CONFCODE_LENGTH,
        required=True
    )


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя"""
    invitations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReferallUser
        fields = ('username', 'phone_number', 'invited_by', 'invitations')
        read_only_fields = ('invitation_code',)

    def get_invitations(self, user):
        return [
            str(user) for user in ReferallUser.objects.filter(
                invited_by=user.invitation_code
            )
        ]

    def update(self, instance, validated_data):
        invited_by = validated_data.get('invited_by')
        if invited_by and not ReferallUser.objects.filter(
            invitation_code=invited_by
        ).exists():
            raise serializers.ValidationError(
                {'invited_by': 'Такого инвайт-кода не существует'}
            )
        if invited_by and instance.invited_by:
            raise serializers.ValidationError(
                {'invited_by': 'Вы уже ввели инвайт-код'}
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.invited_by:
            del data['invited_by']
        return data
