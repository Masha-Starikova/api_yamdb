import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.authenticaton import CustomAuthentication
from api.errors import Error
from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    TokenSerializer,
    SignupSerializer,
    AuthSerializer,
    MeSerializer
)
from api.permissions import IsAdmin, IsModerator, IsOwner
from api.services import create_user, update_token
from reviews.models import Review, Title, Token


User = get_user_model()


class Me(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = (IsOwner,)
    authentication_classes = (CustomAuthentication,)
    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = MeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update_user_data(serializer.validated_data, user)
            return JsonResponse({'ok': 'data was updated'})
        return JsonResponse(Error.WRONG_DATA)


class Signup1(APIView):
    def post(self, request):
        print(dir(request))
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            if username == 'me':
                return JsonResponse(Error.INVALID_USERNAME, status=400)
            email = serializer.data.get('email')
            if create_user(username, email):
                return Response(
                    serializer.data,
                    status=200
                )
            return JsonResponse(Error.USER_OR_EMAIL_EXIST, status=400)
        return JsonResponse(Error.WRONG_DATA, status=400)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        print(dir(request))
        serializer = SignupSerializer(data=json.loads(request.body))
          
        if serializer.is_valid():
            username = serializer.data.get('username')
            if username == 'me':
                return JsonResponse(Error.INVALID_USERNAME, status=400)
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


class GetToken(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            get_object_or_404(User, username=request.user.username)
            confirmation_code = serializer.data.get('confirmation_code')
            if User.objects.filter(username=username).exists():
                token = update_token(username, confirmation_code)
                if token is not None:
                    return JsonResponse({'token': token})
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
