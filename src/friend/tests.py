from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.friend.models import User, Friend, FriendRequest


class FriendsTestCase(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='Fill',
            password=make_password('Pas$w0rd')
        )
        user1.save()
        self.client.force_authenticate(user1)
        user2 = User.objects.create_user(
            username='admin',
            password=make_password('Pas$w0rd')
        )
        user2.save()
        user3 = User.objects.create_user(
            username='tima',
            password=make_password('Pas$w0rd')
        )
        user3.save()
        self.friend = Friend.objects.create(
            user=user1,
            friend=user2
        )
        self.friend.save()
        friend2 = Friend.objects.create(
            user=user1,
            friend=user3
        )
        friend2.save()

        self.incoming_request = FriendRequest.objects.create(
            from_whom=user3,
            to_whom=user1
        )
        self.incoming_request.save()

    def test_list_friends(self):
        """ Проверка вывода списка друзей пользователя """
        response = self.client.get(reverse('list_friends'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data  # Получаем список с друзьями
        self.assertEqual(len(data), 2)

    def test_delete_friend(self):
        """ Проверка удаления пользователя из друзей """
        data = {
            "id": self.friend.id
        }
        response = self.client.delete(reverse('delete_friend'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Пользователь удален из друзей!')

    def test_accept_friend_request(self):
        """ Проверка принятия запроса в друзья """
        data = {
            "id": self.incoming_request.id,
            "state": "accept"
        }
        response = self.client.post(reverse('response_to_request'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Пользователь добавлен в друзья!")

    def test_reject_friend_request(self):
        """ Проверка отклонения запроса в друзья """
        data = {
            "id": self.incoming_request.id,
            "state": "reject"
        }
        response = self.client.post(reverse('response_to_request'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Заявка отклонена!")


class FriendRequestsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='Fill',
            password=make_password('Pas$w0rd')
        )
        self.user1.save()

        self.user2 = User.objects.create_user(
            username='admin',
            password=make_password('Pas$w0rd')
        )
        self.user2.save()
        self.user3 = User.objects.create_user(
            username='tima',
            password=make_password('Pas$w0rd')
        )
        self.user3.save()
        self.user4 = User.objects.create_user(
            username='andrey',
            password=make_password('Pas$w0rd')
        )
        self.user4.save()
        friend_request = FriendRequest.objects.create(
            from_whom=self.user1,
            to_whom=self.user2
        )
        friend_request.save()
        friend_request1 = FriendRequest.objects.create(
            from_whom=self.user2,
            to_whom=self.user1
        )
        friend_request1.save()
        friend_request2 = FriendRequest.objects.create(
            from_whom=self.user3,
            to_whom=self.user1
        )
        friend_request2.save()
        friend = Friend.objects.create(
            user=self.user1,
            friend=self.user4
        )
        friend.save()

    def test_outgoing_request(self):
        """ Проверка вывода списка исходящих запросов в друзья """
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('outgoing_request'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)

    def test_incoming_request(self):
        """ Проверка вывода списка входящих запросов в друзья """
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('incoming_request'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 2)

    def test_send_request_already(self):
        """ Проверка отправки запроса в друзья, когда запрос уже существует  """
        data = {
            'username': 'admin'
        }
        self.client.force_authenticate(self.user1)
        response = self.client.post(reverse('send_request'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Заявка уже была отправлена!')

    def test_send_request_accept(self):
        """ Проверка отправки запроса в друзья """
        data = {
            'username': 'tima'
        }
        self.client.force_authenticate(self.user2)
        response = self.client.post(reverse('send_request'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Заявка отправлена!')

    def test_send_mutual_request(self):
        """ Проверка отправки запроса в друзья, когда есть входящий запрос от пользователя"""
        data = {
            "username": "tima"
        }
        self.client.force_authenticate(self.user1)
        response = self.client.post(reverse('send_request'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Пользователь добавлен в друзья!')

    def test_detect_users_state_out_request(self):
        """ Проверить определение связи между пользователями (исходящая заявка) """
        data = {
            "first_user": 'admin',
            "second_user": 'Fill'
        }
        response = self.client.post(reverse('detect_users_state'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Исходящая заявка от admin пользователю Fill')

    def test_detect_users_state_inc_request(self):
        """ Проверить определение связи между пользователями (входящая заявка) """
        data = {
            "first_user": 'Fill',
            "second_user": 'admin'
        }
        response = self.client.post(reverse('detect_users_state'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Исходящая заявка от Fill пользователю admin')

    def test_detect_users_state_friend(self):
        """ Проверить определение связи между пользователями (Друзья) """
        data = {
            "first_user": 'Fill',
            "second_user": 'andrey'
        }
        response = self.client.post(reverse('detect_users_state'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Уже друзья')

    def test_detect_users_state_nothing(self):
        """ Проверить определение связи между пользователями (Ничего нет) """
        data = {
            "first_user": 'admin',
            "second_user": 'andrey'
        }
        response = self.client.post(reverse('detect_users_state'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Ничего нет')
