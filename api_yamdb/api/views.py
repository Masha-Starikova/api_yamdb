from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework import viewsets
from rest_framework.django_filters import CharFilter
from rest_framework import filters

from reviews.models import Genre, Category, Title, Review
from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer
)


class GenreViewSet(MixinsViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(MixinsViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleFilter(FilterSet):
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
    filter_backends = [rest_framework.DjangoFilterBackend]
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
