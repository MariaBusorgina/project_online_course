from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Balance

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    # TODO
    user = CustomUserSerializer()

    class Meta:
        model = Subscription
        fields = (
            'id',
            'user',
            'course',
            'date_subscribed',
            'group'
        )


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор баланса."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Balance
        fields = (
            'id',
            'user',
            'balance'
        )
