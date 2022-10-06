from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews', blank=True
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, blank=True
    )
    #title = models.ForeignKey(
    #    Title, on_delete=models.CASCADE,
    #    related_name='reviews', blank=True
    #)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField()
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments', blank=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, blank=True
    )
    #title = models.ForeignKey(
    #    Title, on_delete=models.CASCADE,
    #    related_name='comments', blank=True
    #)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments', blank=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:15]
