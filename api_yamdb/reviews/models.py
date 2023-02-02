import datetime

from django.core.validators import (
    validate_slug,
    MaxValueValidator,
    MinValueValidator,
)
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

USER_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):

    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name='фамилия', max_length=150, blank=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email',
    )
    bio = models.TextField(
        max_length=254, verbose_name='Биография', blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default=USER,
        blank=True,
        verbose_name='Роль',
    )
    confirmation_code = models.CharField(
        max_length=50, blank=True, verbose_name='Код авторизации'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username


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

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)


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

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(datetime.datetime.now().year)],
    )
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=None,
        related_name='titles',
        blank=False,
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True,
        db_index=True, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        verbose_name = 'Произведение/жанр'
        verbose_name_plural = 'Произведения/жанры'
        ordering = ('-name',)


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

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(fields=('title', 'author'),
                                    name='unique_review')
        ]


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

    class Meta:
        ordering = ['-pub_date']
