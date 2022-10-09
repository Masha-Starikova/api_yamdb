from operator import length_hint
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import Token
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets

from reviews.models import Review, Title
from api.serializers import CommentSerializer, ReviewSerializer, TokenSerializer


User = get_user_model()


#this view for tests
class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    http_method_names = ['get']


def check_body(request):
    if not request.body:
        return None
    data = json.loads(request.body)
    if data.get('username') is not None and len(data) == 1:
        return data.get('username')
    return None


def update_token(username, token):
    user = User.objects.get(username=username)
    token_obj = Token.objects.get(user=user)
    token_obj.token = token
    token_obj.save()


@csrf_exempt
def get_token(request):
    if request.method == 'POST':
        username = check_body(request)
        if username is not None:
            if User.objects.filter(username=username).exists():
                token = get_random_string(length=32)
                update_token(username, token)
                return JsonResponse({'token': token})
            else:
                return JsonResponse({'details':'user does not exist'})
        return JsonResponse({'details':'wrong data'})
    return JsonResponse({'details': 'method not allowed'})


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
