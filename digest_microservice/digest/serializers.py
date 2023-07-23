from rest_framework import serializers
from .models import User, Post, Digest, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class DigestSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = Digest
        fields = "__all__"

    def to_representation(self, instance):
        # Переопределяем метод to_representation для удобства отображения данных
        data = super().to_representation(instance)
        sorted_data = sorted(data["posts"], key=lambda x: x['popularity'],
                             reverse=True) # Сортируем посты по популярности в порядке убывания
        data["posts"] = [post["content"] for post in sorted_data] # Оставляем только содержание постов
        return data

