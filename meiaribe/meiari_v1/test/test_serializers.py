from django.test import TestCase
from django.utils import timezone
from meiari_v1.models import MeiAriUser, WorkGroup
from meiari_v1.serializers import WorkGroupSerializer, MeiAriUserSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SerializerTests(TestCase):

    def test_workgroup_serializer(self):
        user = MeiAriUser.objects.create(user_id="USR100", name="SName", email="s@example.com", mobile_number="5555555555")
        data = {
            "group_id": "WGX",
            "name": "Serialize Test",
            "created_by": user.id,
            "created_on": timezone.now()
        }
        serializer = WorkGroupSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_meiari_user_serializer_valid(self):
        data = {"mobile_number": "9876543210"}
        serializer = MeiAriUserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_meiari_user_serializer_invalid(self):
        data = {"mobile_number": ""}
        serializer = MeiAriUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_user_serializer_output(self):
        user = User.objects.create_user(username='test', email='test@example.com', password='testpass')
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['username'], 'test')
