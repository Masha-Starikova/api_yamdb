from rest_framework import serializers

from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ['title', 'review' ]
        model = Comment
    read_only_fields = ('title', )

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ['title', ]
        model = Review
    read_only_fields = ('title', 'review')

