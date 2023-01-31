from rest_framework import serializers

from reviews.models import Category, Genre, Title, TitleGenre


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

    def get_rating(x, y):
        ...

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

    def get_rating(x, y):
        ...

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
