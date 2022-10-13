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
    get_token, signup, MeViewSet)


v1_router = routers.DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
#v1_router.register('me', MeViewSet, basename='me')
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
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls)),
    path('v1/get_token/', get_token),
    path('v1/signup/', signup),
    path('v1/me/', MeViewSet.as_view({'patch': 'partial_update'}))
]

