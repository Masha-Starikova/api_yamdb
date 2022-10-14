from xml.dom import ValidationErr
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title, Comment, Review, User
from reviews.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create(**validated_data, is_active=0)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        lookup_field = 'username'


class UserNotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio')
        read_only_fields = ('role', )
        lookup_field = 'username'


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(max_length=4, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', 'username', 'confirmation_code')
        model = User


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
        exclude = ['review', ]
        model = Comment
    read_only_fields = ('title')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationErr('Нельзя добовлять более одного отзыва.')
        return data

    class Meta:
        exclude = ['title', ]
        model = Review
    read_only_fields = ('title', 'review')