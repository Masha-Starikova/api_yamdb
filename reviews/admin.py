from django.contrib import admin

from .models import Category, Genre, Title, User

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
