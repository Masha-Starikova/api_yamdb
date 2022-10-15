from django.contrib import admin
from .models import User, Genre, Category, Title, Review, Comment

admin.site.register(User)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


admin.site.register(Category, CategoryAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')


admin.site.register(Title, TitleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_id', 'text', 'autor', 'score', 'pub_date')


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_id', 'text', 'autor', 'pub_date')


admin.site.register(Comment, CommentAdmin)

