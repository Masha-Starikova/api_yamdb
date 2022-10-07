from django.contrib import admin
from .models import User, Genre, Category, Title

admin.site.register(User)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Category, CategoryAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')


admin.site.register(Title, TitleAdmin)
