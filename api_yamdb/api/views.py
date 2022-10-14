from django.db.models import Avg
import json
from django.views.decorators.csrf import csrf_exempt
from api.services import create_user, update_token

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import CharFilter
from rest_framework import viewsets
from reviews.models import Category, Genre, Review, Title
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import (
    IsAdmin,
    IsModerator,
    IsOwner,
    IsAdminModeratorAuthorOrReadOnly
)
from api.authenticaton import CustomAuthentication
from api.models import Token
from api.errors import Error

from api.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, TokenSerializer,
    SignupSerializer, AuthSerializer,
    MeSerializer)


User = get_user_model()


class MeViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = (IsOwner,)
    authentication_classes = (CustomAuthentication, )

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = MeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'ok': 'ok'})
        return JsonResponse({'fail': 'fail'})


@csrf_exempt
def signup(request):
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


#this view for tests
class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    http_method_names = ['get']
    authentication_classes = (CustomAuthentication, )
    permission_classes = (IsAdmin, )


@csrf_exempt
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
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleFilter(viewsets.ModelViewSet):
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
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
