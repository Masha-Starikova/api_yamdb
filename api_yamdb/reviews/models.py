from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Comment(models.Model):
    text = models.TextField()
    autor = models.ForeignKey() #username автора комментария
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:15]


class Review(models.Model):
    SCORE_CHOICES = zip(range(1,10), range(1,10) )
    text = models.TextField()
    autor = models.ForeignKey() #username автора комментария
    score = models.IntegerField(default=1, validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)