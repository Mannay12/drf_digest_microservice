from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Post, Digest, Subscription
from .serializers import UserSerializer, DigestSerializer, PostSerializer, SubscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''
    Фильтрует посты пользователя по популярности
    Обрабатывает GET-запрос на URL вида api/user/1/digest/, где:
    user/1 - уникальный айди пользователя
    digest - дайджест популярных новостей
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=("get",))
    def digest(self, request, pk):
        # Получение всех постов, связанных с пользователем
        posts = Post.objects.filter(subscription__user=int(pk))
        popularity = request.query_params.get("popularity")
        if popularity:
            if popularity.isdigit() and int(popularity) in range(1, 11):
                # Фильтрация постов по популярности, если указан параметр popularity
                sorted_posts = posts.filter(
                    popularity__gte=int(popularity)
                )
                return self.add_digest(sorted_posts, pk)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # Если параметр popularity не указан, создаем дайджест со всеми постами
            return self.add_digest(posts, pk)

    def add_digest(self, posts, pk):
        # Создание/получение объекта модели Digest для пользователя
        digest, _ = Digest.objects.get_or_create(user=User.objects.get(id=int(pk)),)
        digest.posts.set(posts) # Связываем посты с дайджестом
        serializer = DigestSerializer(digest) # Создание сериализатора для дайджеста
        return Response(serializer.data, status=status.HTTP_200_OK)


# Определение класса SubscriptionViewSet для работы с подписками пользователей
class SubscriptionViewSet(viewsets.ViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def list(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Создание постов к подпискам
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    # Создание нового поста(популярность поста ставим сами)
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Просмотр всех дайджестов пользователя по популярности
class DigestViewSet(viewsets.ViewSet):
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer

    def list(self, request):
        subscriptions = Digest.objects.all()
        serializer = DigestSerializer(subscriptions, many=True)
        return Response(serializer.data)
