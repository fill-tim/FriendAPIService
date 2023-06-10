from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Модель пользователя"""
    my_friend = models.ManyToManyField('self', through='Friend', symmetrical=False, related_name='Друзья')
    friend_requests = models.ManyToManyField('self', through='FriendRequest', symmetrical=False,
                                             related_name='Заявки')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.username}'


class Friend(models.Model):
    """ Модель списка друзей"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Пользователь')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Друг')

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f'{self.user.username} - {self.friend.username}'


class FriendRequest(models.Model):
    """ Модель входящих заявок в друзья"""

    from_whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Кого')
    to_whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Получатель')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка пользователю {self.to_whom.username} - от {self.from_whom.username}'
