import datetime

from django.core.validators import (
    validate_slug,
    MaxValueValidator,
    MinValueValidator,
)
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )
    bio = models.TextField(
        max_length=254,
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_user(self):
        return self.role == User.USER

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=50,
        validators=(validate_slug,),
        verbose_name='Слаг категории',
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг жанра',
        validators=(validate_slug,),
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(datetime.datetime.now().year)],
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=None,
        related_name='titles',
        blank=False,
    )  # в задании написано:не нужно **удалять свя.Что за **?

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
