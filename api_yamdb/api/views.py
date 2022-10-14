from django.db.models import Avg
import json
from django.views.decorators.csrf import csrf_exempt
from api.services import create_user, update_token
from rest_framework import permissions, pagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, mixins

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import CharFilter
from rest_framework import viewsets
from reviews.models import Category, Genre, Review, Title, Token
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdmin, IsModerator, IsOwner, IsAdminModeratorAuthorOrReadOnly
from api.authenticaton import CustomAuthentication
from api.errors import Error
from django_filters import rest_framework as filters
from reviews.models import User


from api.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, TokenSerializer,
    SignupSerializer, AuthSerializer,
    UserSerializer, UserNotAdminSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (CustomAuthentication, )
    permission_classes=(IsAdmin,)
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'username'
    search_fields = ('username', )
    

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        url_name='me',
        url_path='me'
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer =UserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class =  SignupSerializer

    def perform_create(self, serializer):
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        serializer.save(username=username, email=email)

    @action(
        methods=['POST',],
        detail=False,
        url_name='signup',
        url_path='signup'
    )

    def signup(self, request):
        if request.method == 'POST':
            serializer = SignupSerializer(data=json.loads(request.body))
        
            if serializer.is_valid():
                username = serializer.data.get('username')
                email = serializer.data.get('email')
                if create_user(username, email):
                    return JsonResponse(
                        {'success': f'user {username} created'},
                        status=200
                    )
                return JsonResponse(Error.USER_OR_EMAIL_EXIST, status=400)
            return JsonResponse(Error.WRONG_DATA)
        return JsonResponse(Error.METHOD_NOT_ALLOWED)


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer

    @action(
        methods=['POST',],
        detail=False,
        url_name='token',
        url_path='token'
    )

    def get_token(request):
        if request.method == 'POST':
            serializer = AuthSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                username = serializer.data.get('username')
                confirmation_code = serializer.data.get('confirmation_code')

                if User.objects.filter(username=username).exists():
                    token = update_token(username, confirmation_code)
                    if token is not None:
                        return JsonResponse({'token': token})
                return JsonResponse(Error.USER_DOES_NOT_EXIST)
            return JsonResponse(Error.WRONG_DATA)
        return JsonResponse(Error.METHOD_NOT_ALLOWED)


#this view for tests
class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    http_method_names = ['get']
    authentication_classes = (CustomAuthentication, )
    permission_classes = (IsAdmin, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
    #permission_classes = (IsAdmin | IsReadOnly,)
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

    def get_queryset(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
