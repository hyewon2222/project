from rest_framework.status import HTTP_201_CREATED
from django.test import TestCase


class AdminActorTestCase(TestCase):
    def test_admin_actor_create(self):
        request = self.client.post(
            path='/admin/actors',
            data={'name': 'actor'}
        )
        response = request.json()
        self.assertEqual(request.status_code, HTTP_201_CREATED)
        self.assertEqual(response['name'], 'actor')
        return response


