from django.urls import path, include

from rest_framework import routers
from api.views import CommentViewSet, ReviewViewSet, TokenViewSet, Me
from api.views import Signup1, GetToken, UserViewSet


v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('token', TokenViewSet)
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
    path('v1/users/me/', Me.as_view({'patch': 'partial_update', 'get': 'retrieve'})),
    path('v1/auth/signup/', Signup1.as_view())
]
