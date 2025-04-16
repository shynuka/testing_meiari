from django.test import TestCase
from django.apps import apps
from meiari_v1.apps import MeiariV1Config

class MeiariV1ConfigTestCase(TestCase):
    def test_app_config(self):
        # Check if the app is loaded
        app = apps.get_app_config('meiari_v1')
        self.assertEqual(app.name, 'meiaribe.meiari_v1')
        self.assertEqual(app.default_auto_field, 'django.db.models.BigAutoField')
