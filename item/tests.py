import pytest
from django.test import TestCase
from actor.models import Actor
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class ItemTestCase(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(name='actor')
        super().setUp()

    def test_item_create(self):
        data = {
            'actor_id': self.actor.id,
            'korea_title': '3D 사무실',
            'korea_contents': '3D 사무실 입니다.',
            'price': 30000,
            'sale_price': 0
        }
        request = self.client.post(
            path='/admin/item',
            data=data
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_201_CREATED)
        self.assertEqual(response['korea_title'], data['korea_title'])

    def test_item_create_404_error(self):
        data = {
            'actor_id': 5,
            'korea_title': '3D 사무실',
            'korea_contents': '3D 사무실 입니다.',
            'price': 30000,
            'sale_price': 0
        }
        request = self.client.post(
            path='/admin/item',
            data=data
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response['actor_id'],  ['Invalid pk "5" - object does not exist.'])
