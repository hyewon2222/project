from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.test import TestCase

from actor.models import Actor
from actor.tests import AdminActorTestCase
from editor.tests import AdminEditorTestCase


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
        self.assertEqual(response['status'], 'ready')
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
        item = self.test_admin_item_create()
        request = self.client.get(
            path='/admin/items',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(response['results'][0]['id'], item['id'])
        self.assertEqual(response['results'][0]['status'], item['status'])


class AdminItemCheckTestCase(TestCase):
    def setUp(self):
        self.actor = AdminActorTestCase.test_admin_actor_create(self)
        self.editor = AdminEditorTestCase.test_admin_editor_create(self)
        self.item = AdminItemTestCase.test_admin_item_create(self)
        super().setUp()

    def test_admin_item_check(self):
        success_data = {
            'editor_id': self.editor['id'],
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
        self.assertEqual(self.item['korea_title'], '3D 사무실')
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['korea_title'], success_data['korea_title'])
        return response

    def test_admin_item_check_400_error(self):
        request = self.client.patch(
            path=f'/admin/items/{self.item["id"]}/check',
            data={},
            content_type='application/json',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response['non_field_errors'], ['에디터 정보를 입력해주세요.'])

        data = {
            'editor_id': self.editor['id'],
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

    def test_admin_item_check_404_error(self):
        request = self.client.patch(
            path='/admin/items/4/check',
            data={},
            content_type='application/json',
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(response['detail'], '존재하지 않는 상품입니다.')


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
        self.editor = AdminEditorTestCase.test_admin_editor_create(self)
        self.item = AdminItemTestCase.test_admin_item_create(self)
        super().setUp()

    def test_item_list(self):
        data = AdminItemCheckTestCase.test_admin_item_check(self)
        request = self.client.get(path='/items')
        response = request.json()
        self.assertEqual(request.status_code, HTTP_200_OK)
        self.assertEqual(response['results'][0]['actor_id'], self.actor['id'])
        self.assertEqual(response['results'][0]['status'], data['status'], 'success')
