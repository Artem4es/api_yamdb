from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    search_fields = ('text',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date')
    search_fields = ('title', 'author', 'text')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'description')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    search_fields = ('title__name', 'genre__name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
