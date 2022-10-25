from re import L
import shutil
import tempfile

from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase
from accounts.models import Profile

from .apps import LinksConfig
from .models import Links, Networks

MEDIA_ROOT = tempfile.mkdtemp()

class TestAppConfig(APITestCase):

    def test_app_config(self):
        self.assertEqual('links', LinksConfig.name)

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestModels(APITestCase):
    
    def setUp(self):
        profile = Profile.objects.create(
            first_name= 'Harold',
            last_name= 'Finch',
            username= 'admin',
            password=make_password('TestP455word!')
        )
        profile.save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def network_str(self):
        new_network = Networks.objects.create(
            logo=SimpleUploadedFile('logo.png', b'testimage'),
            name="Instagram"
        )
        new_network.save()
        network = Networks.objects.get(name="Instagram")
        self.assertEqual(str(network), 'Instagram')

    def link_str(self):
        user = Profile.objects.get(username="admin")
        network = Networks.objects.get(name="Instagram")
        new_link = Links.objects.create(
            user=user,
            network=network,
            link="https://www.instagram.com/",
        )
        new_link.save()
        link = Links.objects.get(user=user, network=network)
        self.assertEqual(str(link), "admin for Instagram")

    def test_in_order(self):
        self.network_str()
        self.link_str()
