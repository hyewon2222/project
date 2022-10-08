import pytest
from django.test import TestCase
from actor.models import Actor
from rest_framework.status import HTTP_201_CREATED


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