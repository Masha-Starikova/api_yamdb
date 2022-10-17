from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, Token

User = get_user_model()


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User
        read_only_fields = ("role",)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.IntegerField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_useranme(self, value):
        if value == 'me':
            raise ValidationError('cant user "me"')
        return value


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
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        model = Comment
#        fields = ('id', 'text', 'author', 'pub_date' )
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST':
            if Review.objects.filter(title_id=title_id, author=author).exists():
                raise ValidationError('Нельзя добовлять более одного отзыва.')
        return data
