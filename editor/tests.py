from rest_framework.status import HTTP_201_CREATED
from django.test import TestCase


class AdminEditorTestCase(TestCase):
    def test_admin_editor_create(self):
        request = self.client.post(
            path='/admin/editors',
            data={'name': 'editor'}
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_201_CREATED)
        self.assertEqual(response['name'], 'editor')
        return response


