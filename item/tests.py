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


class AdminItemCheckTestCase(TestCase):
    def setUp(self):
        self.actor = AdminActorTestCase.test_admin_actor_create(self)
        self.editor = AdminEditorTestCase.test_admin_editor_create(self)
        self.item = AdminItemTestCase.test_admin_item_create(self)
        super().setUp()

    def test_admin_item_check(self):
        success_data = {
            'editor_id': self.editor['id'],
            'status': 'success',
            'commission_rate': 0.5,
            'korea_title': '수정'
        }
        request = self.client.patch(
            path=f'/admin/items/{self.item["id"]}/check',
            data=success_data,
            content_type='application/json',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(response['status'], success_data['status'])
        self.assertEqual(response['korea_title'], success_data['korea_title'])
        return response

    def test_admin_item_check_400_error(self):
        data = {
            'editor_id': self.editor['id'],
            'status': 'success'
        }
        request = self.client.patch(
            path=f'/admin/items/{self.item["id"]}/check',
            data=data,
            content_type='application/json',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response, ['수수료를 입력해주세요.'])

        data['editor_id'] = 5
        request = self.client.patch(
            path=f'/admin/items/{self.item["id"]}/check',
            data=data,
            content_type='application/json',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response['editor_id'], ["Invalid pk \"5\" - object does not exist."])

class AdminItemUpdateTestCase(TestCase):
    def setUp(self):
        self.actor = AdminActorTestCase.test_admin_actor_create(self)
        self.editor = AdminEditorTestCase.test_admin_editor_create(self)
        self.item = AdminItemTestCase.test_admin_item_create(self)
        super().setUp()

    def test_admin_item_update(self):
        data = {
            'actor_id': self.actor['id'],
            'korea_title': '수정 두번'
        }
        request = self.client.patch(
            path=f'/admin/items/{self.item["id"]}',
            data=data,
            content_type='application/json',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(response['status'], 'ready')
        self.assertEqual(response['korea_title'], data['korea_title'])
        return response


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
