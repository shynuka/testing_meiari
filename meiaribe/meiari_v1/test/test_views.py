from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from meiari_v1.models import MeiAriUser, WorkGroup
import uuid


class TestUserCreation(APITestCase):
    def test_create_meiari_user(self):
        url = reverse('create-meiari-user')
        data = {
            "mobile_number": "9876543210"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MeiAriUser.objects.count(), 1)
        self.assertEqual(MeiAriUser.objects.first().mobile_number, "9876543210")


class TestWorkGroupCreation(APITestCase):
    def setUp(self):
        self.user = MeiAriUser.objects.create(mobile_number="9876543210")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_workgroup(self):
        url = reverse('workgroup')  # Make sure 'workgroup' is the name in urls.py
        group_id = uuid.uuid4()
        data = {
            "group_id": str(group_id),
            "name": "Sanitation Team",
            "created_by": str(self.user.id),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(WorkGroup.objects.count(), 1)
        self.assertEqual(WorkGroup.objects.first().name, "Sanitation Team")

    def test_create_workgroup_missing_fields(self):
        url = reverse('workgroup')
        data = {
            "group_id": str(uuid.uuid4()),
            # Missing name and created_by
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)


class TestHealthCheckView(APITestCase):
    def test_health_check(self):
        url = reverse('geminiapp-check')  # Make sure 'geminiapp-check' is correct name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "OK")
