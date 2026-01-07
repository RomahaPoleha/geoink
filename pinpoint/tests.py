from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import GeoPin, PinMemo


class GeoinkApiTests(TestCase):
    """Тесты API """
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_point(self):
        """Создание точки на карте (POST /api/points/)"""
        response = self.client.post('/api/points/', {
            'latitude': 43.1056,
            'longitude': 131.8735
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GeoPin.objects.count(), 1)
        point = GeoPin.objects.first()
        self.assertEqual(point.latitude, 43.1056)
        self.assertEqual(point.longitude, 131.8735)
        self.assertEqual(point.author, self.user)

    def test_create_message_to_point(self):
        """Создание сообщения к заданной точке (POST /api/points/messages/)"""
        point = GeoPin.objects.create(
            author=self.user,
            latitude=55.75,
            longitude=37.62
        )

        response = self.client.post('/api/points/messages/', {
            'pin_id': point.id,
            'content': 'Москва'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PinMemo.objects.count(), 1)
        memo = PinMemo.objects.first()
        self.assertEqual(memo.content, 'Москва')
        self.assertEqual(memo.pin, point)
        self.assertEqual(memo.author, self.user)

    def test_search_points_in_radius(self):
        """Поиск точек в заданном радиусе (GET /api/points/search/)"""
        # Точка во Владивостоке
        GeoPin.objects.create(author=self.user, latitude=43.1056, longitude=131.8735)
        # Точка в Москве (далеко)
        GeoPin.objects.create(author=self.user, latitude=55.75, longitude=37.62)

        # Ищем в радиусе 10 км от Владивостока
        response = self.client.get('/api/points/search/?latitude=43.1056&longitude=131.8735&radius=10')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertAlmostEqual(data[0]['latitude'], 43.1056, places=3)
        self.assertAlmostEqual(data[0]['longitude'], 131.8735, places=3)

    def test_search_messages_in_radius(self):
        """Получение сообщений в заданной области / радиусе"""
        vlad_point = GeoPin.objects.create(author=self.user, latitude=43.1056, longitude=131.8735)
        PinMemo.objects.create(pin=vlad_point, author=self.user, content='Владивосток: много припасов рыбы')

        moscow_point = GeoPin.objects.create(author=self.user, latitude=55.75, longitude=37.62)
        PinMemo.objects.create(pin=moscow_point, author=self.user, content='Москва: необследованно')

        response = self.client.get('/api/points/messages/search/?latitude=43.1056&longitude=131.8735&radius=5')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['content'], 'Владивосток: много припасов рыбы')
        self.assertEqual(data[0]['latitude'], 43.1056)
        self.assertEqual(data[0]['longitude'], 131.8735)

    def test_all_endpoints_require_authentication(self):
        """Все эндпоинты требуют авторизации"""
        client = APIClient()

        responses = [
            client.post('/api/points/', {'latitude': 1, 'longitude': 1}),
            client.post('/api/points/messages/', {'pin_id': 999, 'content': 'test'}),
            client.get('/api/points/search/?latitude=0&longitude=0&radius=1'),
            client.get('/api/points/messages/search/?latitude=0&longitude=0&radius=1'),
        ]

        for resp in responses:
            self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)