import json
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.test import TestCase

from actor.models import Actor
from actor.tests import AdminActorTestCase
from editor.tests import AdminEditorTestCase
from item.models import Item


class AdminItemTestCase(TestCase):
    def setUp(self):
        self.actor = AdminActorTestCase.test_admin_actor_create(self)
        self.editor = AdminEditorTestCase.test_admin_editor_create(self)
        super().setUp()

    def test_admin_item_create(self):
        data = {
            'actor_id': self.actor['id'],
            'korea_title': '3D 사무실',
            'korea_contents': '3D 사무실 입니다.',
            'price': 30000,
            'sale_price': 0
        }
        request = self.client.post(
            path='/admin/items',
            data=data
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_201_CREATED)
        self.assertEqual(response['korea_title'], data['korea_title'])
        self.assertEqual(response['actor_name'], self.actor['name'])
        return response

    def test_admin_item_create_404_error(self):
        data = {
            'actor_id': 5,
            'korea_title': '3D 사무실',
            'korea_contents': '3D 사무실 입니다.',
            'price': 30000,
            'sale_price': 0
        }
        request = self.client.post(
            path='/admin/items',
            data=data
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response['actor_id'],  ['Invalid pk "5" - object does not exist.'])

    def test_admin_item_list(self):
        request = self.client.get(
            path='/admin/items',
        )
        self.assertEqual(request.status_code, HTTP_200_OK)


class ItemListTestCase(TestCase):
    def setUp(self):
        self.actor = AdminActorTestCase.test_admin_actor_create(self)
        super().setUp()

    def test_item_list(self):
        actor = Actor.objects.filter(id=self.actor['id']).first()
        data = {
            'actor_id': actor,
            'korea_title': '3D 사무실',
            'korea_contents': '3D 사무실 입니다.',
            'price': 30000,
            'sale_price': 0,
            'status': 'success'
        }
        Item.objects.create(**data)
        request = self.client.get(path='/items')
        response = request.json()
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(response['results'][0]['actor_id'], self.actor['id'])
        self.assertEqual(response['results'][0]['status'], data['status'])
