from django.db import models
from django.contrib.auth.models import AbstractUser


class UserC(AbstractUser):
    """ Модель пользователя
    """

    my_friend = models.ManyToManyField('self', through='Friend', symmetrical=False, related_name='Друзья')

    # incoming_request = models.ManyToManyField('self', through='FriendRequest', symmetrical=False,
    #                                           related_name='Входящие' + 'запросы')

    # outgoing_requests

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.username}'


class Friend(models.Model):
    """ Модель списка друзей
    """

    user = models.ForeignKey(UserC, on_delete=models.CASCADE, related_name='Пользователь')
    friend = models.ForeignKey(UserC, on_delete=models.CASCADE, related_name='Друг')
    status = models.CharField(max_length=16)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f'{self.user.username} - {self.friend.username}'


class FriendRequest(models.Model):
    """ Модель заявок в друзья
    """
    # STATUSES = (
    #     ('incoming', 'incoming'),
    #     ('outgoing', 'outgoing')
    # )
    #
    # from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Кто')
    # to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Кому')
    # status = models.CharField(max_length=8, choices=STATUSES)
    pass
