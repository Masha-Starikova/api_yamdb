from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from api.views import (
    GenreViewSet, CategoryViewSet, 
    TitleViewSet, CommentViewSet, 
    ReviewViewSet, TokenViewSet,
    SignupViewSet, AuthViewSet, UserViewSet)


v1_router = routers.DefaultRouter()
v1_router.register('auth/token', AuthViewSet, basename='token')
v1_router.register('auth/signup', SignupViewSet)
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls)),
#    path('v1/auth/token/', get_token),
    #path('v1/auth/signup/', signup),
    path('v1/me/', UserViewSet.as_view({'patch': 'partial_update'}))
]

