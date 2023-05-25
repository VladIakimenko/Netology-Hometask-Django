from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'description',
            'creator',
            'status',
            'created_at',
            'draft'
        )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        queryset = Advertisement.objects.filter(
            creator=self.context['request'].user,
            status='OPEN'
        )
        if len(queryset) >= 10:
            raise ValidationError("The limit of 10 open advertisements has been reached.")

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('advertisement',)
        read_only_fields = ('advertisement',)

    def to_representation(self, instance):
        if not self.context['request'].user.is_staff:
            return super().to_representation(instance)
        else:
            return {
                'user': instance.user.id,
                'advertisement': instance.advertisement.id
            }

    def create(self, validated_data):
        user = self.context['request'].user
        adv_id = self.context['request'].query_params.get('adv')
        advertisement = get_object_or_404(Advertisement, id=adv_id)
        favorite, created = Favorite.objects.get_or_create(user=user, advertisement=advertisement)
        if created:
            return favorite
        else:
            raise serializers.ValidationError('Advertisement is already in favorites.')

