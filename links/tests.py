import json
import shutil
import tempfile

from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
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
        Profile.objects.create(
            first_name= 'Harold',
            last_name= 'Finch',
            username= 'admin',
            password=make_password('TestP455word!')
        ).save()

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

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestViews(APITestCase):

    def setUp(self):
        Profile.objects.create(
            first_name= 'Harold',
            last_name= 'Finch',
            username= 'admin',
            password=make_password('TestP455word!1')
        ).save()
        Profile.objects.create(
            first_name= 'John',
            last_name= 'Reese',
            username= 'test',
            password=make_password('TestP455word!2')
        ).save()
        Networks.objects.create(
            id=1,
            logo=SimpleUploadedFile('insta.png', b'insta'),
            name="Instagram"
        ).save()
        Networks.objects.create(
            id=2,
            logo=SimpleUploadedFile('twit.png', b'twit'),
            name="Twitter"
        ).save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def create_link(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!1'
            },
            format='json'
        )
        access_token = access_request.data['access']
        network = Networks.objects.get(name="Twitter")
        response = self.client.post(
            '/api/links/',
            {
                'network': network.id,
                'link': 'https://twitter.com/'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 201)
        profile = Profile.objects.get(username="admin")
        self.assertEqual(
            json.loads(response.content),
            {
                "user": profile.id,
                "network": {
                    'id': network.id,
                    "logo": "/media/logos/twit.png",
                    "name": "Twitter"
                },
                "link": "https://twitter.com/",
                "nsfw": False
            }
        )

    def update_link(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!1'
            },
            format='json'
        )
        access_token = access_request.data['access']
        link = Links.objects.get(network__name='Twitter')
        response = self.client.patch(
            f'/api/links/{link.id}/',
            {
                'link': 'https://twitter.com/HWCCLiverpool'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "network": {
                    "id": link.network.id,
                    "logo": "/media/logos/twit.png",
                    "name": "Twitter"
                },
                "link": "https://twitter.com/HWCCLiverpool",
                "nsfw": False
            }
        )

    def get_networks(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!1'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.get(
            '/api/links/networks/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    'id': 1,
                    "logo": "http://testserver/media/logos/insta.png",
                    "name": "Instagram"
                },
                {
                    'id': 2,
                    "logo": "http://testserver/media/logos/twit.png",
                    "name": "Twitter"
                }
            ]
        )

    def get_profile_exists(self):
        response = self.client.get(
            '/api/links/admin/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                'id': 5,
                "username": "admin",
                "first_name": "Harold",
                "last_name": "Finch",
                "bio": None,
                "profile_picture": None,
                "links": [
                    {
                        "network": {
                            'id': 2,
                            "logo": "/media/logos/twit.png",
                            "name": "Twitter"
                        },
                        "link": "https://twitter.com/HWCCLiverpool",
                        "nsfw": False
                    }
                ]
            }
        )

    def get_profile_404(self):
        response = self.client.get(
            '/api/links/testuser/'
        )
        self.assertEqual(response.status_code, 404)

    def delete_link(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!1'
            },
            format='json'
        )
        access_token = access_request.data['access']
        link = Links.objects.get(network__name='Twitter')
        response = self.client.delete(
            f'/api/links/{link.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 204)
    
    def test_in_order(self):
        self.create_link()
        self.update_link()
        self.get_networks()
        self.get_profile_exists()
        self.get_profile_404()
        self.delete_link()