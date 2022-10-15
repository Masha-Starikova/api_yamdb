from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,  pagination, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from api.authenticaton import CustomAuthentication
from api.errors import Error
from api.permissions import IsAdmin, IsOwner, IsAdminModeratorAuthorOrReadOnly
from api.services import create_user, update_token
from django_filters import rest_framework as filters
from reviews.models import Token, Genre, Category, Title, Review
from api.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, TokenSerializer,
    SignupSerializer, AuthSerializer,
    MeSerializer, UserSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (CustomAuthentication, )
    permission_classes=(IsAdmin,)
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'username'


class MeViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = (IsOwner,)
    authentication_classes = (CustomAuthentication,)
    
    def retrieve(self, request, pk=None):
        return Response({'1': '1'})

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = MeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update_user_data(serializer.validated_data, user)
            return Response(serializer.validated_data)
        return Response(Error.WRONG_DATA)


class Signup1(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            if username == 'me':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            email = serializer.data.get('email')
            if create_user(username, email):
                return Response(
                    serializer.data,
                    status=200
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#this view for tests
class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    http_method_names = ['get']
    authentication_classes = (CustomAuthentication, )
    permission_classes = (IsAdmin, )


class GetToken(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            get_object_or_404(User, username=username)
            confirmation_code = serializer.data.get('confirmation_code')
            token = update_token(username, confirmation_code)
            if token is not None:
                return Response({'token': token})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (CustomAuthentication, )


class TitleFilter(filters.FilterSet):
    genre = CharFilter(field_name='genre__slug',
                       lookup_expr='icontains')
    category = CharFilter(field_name='category__slug',
                          lookup_expr='icontains')
    name = CharFilter(field_name='name',
                      lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    authentication_classes = (CustomAuthentication, )
    permission_classes = (IsAdmin, )
    filter_backends = (DjangoFilterBackend)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAdminModeratorAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
    
    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = self.request.user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(title_id=title_id,author=author).exists():
            raise ValueError('Нельзя добовлять более одного отзыва.')
        return data


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly]
    authentication_classes = (CustomAuthentication, )

    def get_queryset(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
