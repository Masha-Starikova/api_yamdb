from functools import partial
from multiprocessing import context
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters as SearchFilter
from .filters import TitleFilter
from api.errors import Error
from api.permissions import IsAdmin, IsOwner, IsModerator, IsAuthenticatedOrReadOnly, IsAdminModeratorAuthorOrReadOnly
from api.services import create_user, update_token
from django_filters import rest_framework as filters
from reviews.models import Token, Genre, Category, Title, Review
from api.serializers import (
     CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, TokenSerializer,
    SignupSerializer, AuthSerializer, TitleCreateSerializer,
    UserSerializer, ProfileEditSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
#    search_fields = ("username",)


    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(APIView):
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
#    authentication_classes = (, )
    permission_classes = (IsAdmin, )


class GetToken(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.data.get('confirmation_code')
            if user.check_confirmation_code(confirmation_code):
                token = AccessToken.for_user(user)
                return Response({'token': str(token)})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin, IsAuthenticatedOrReadOnly]
#    filter_backends = (SearchFilter,)

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs['slug'])

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin, IsAuthenticatedOrReadOnly]
#    filter_backends = (SearchFilter,)

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = [IsAdmin, IsAuthenticatedOrReadOnly]
    filterset_class = TitleFilter

#    def get_object(self):
#        return get_object_or_404(
#            self.queryset, slug=self.kwargs['slug'])
   

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
#    lookup_field = "title_id"

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
