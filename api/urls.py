from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet, sign_up,
                       ReviewViewSet, get_token, TitleViewSet, UserViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('user/me', UserViewSet, basename='me')
v1_router.register('users', UserViewSet, basename='username')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', get_token),
    path('v1/auth/signup/', sign_up)
]
