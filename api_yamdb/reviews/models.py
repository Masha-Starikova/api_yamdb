from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user')
    )
    role = models.CharField(max_length=20, choices=ROLES, default='user')


class Genre(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=True, null=True,
        help_text='Напишите название жанра'
    )

    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text=('Укажите адрес для нового жанра. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )

    class Meta:
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=True, null=True,
        help_text='Напишите название категории'
    )

    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text=('Укажите адрес для новой категории. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )

    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Title(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Напишите название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        blank=True,
        null=True,
        help_text='Укажите год создания',
        validators=[MinValueValidator(1900), MaxValueValidator(2022)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='категория',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанр',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True, null=True,
        help_text='Добавьте сюда описание произведения'
    )

    class Meta:
        verbose_name_plural = 'Произведения'
        ordering = ['id']


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
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', blank=True
    )

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
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments', blank=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:15]
