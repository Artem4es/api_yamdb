from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    USER_ROLES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    ]

    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Логин',
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True
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
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
