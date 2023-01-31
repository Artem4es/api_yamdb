from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Comment, Review, Category, Genre, Title, TitleGenre


User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField(max_length=100)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        user = self.context.get('request').user
        title = Title.objects.get(id=data.get('title_id'))
        if Review.objects.filter(title=title).filter(author=user).exists():
            raise serializers.ValidationError()
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(Avg('score'))
        return int(rating)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitlePostSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    def get_rating(self, obj):  # возможно лишняя
        rating = Review.objects.filter(title=obj).aggregate(Avg('score'))
        return int(rating)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
