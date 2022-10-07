from rest_framework import serializers

from reviews.models import Genre, Category, Title, Comment, Review



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ['review_id', ]
        model = Comment
    read_only_fields = ('title')

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ['title_id', ]
        model = Review
    read_only_fields = ('title', 'review')