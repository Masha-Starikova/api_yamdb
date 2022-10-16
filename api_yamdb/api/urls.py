from django.urls import path, include

from rest_framework import routers
from api.views import (
    GenreViewSet, CategoryViewSet, 
    TitleViewSet, CommentViewSet, 
    ReviewViewSet, TokenViewSet,
)
from api.views import Signup, GetToken, UserViewSet


v1_router = routers.DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
#v1_router.register('me', MeViewSet, basename='me')
v1_router.register('token', TokenViewSet)
v1_router.register('users', UserViewSet)
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
    path('v1/auth/token/', GetToken.as_view()),
    path('v1/auth/signup/', Signup.as_view())
]