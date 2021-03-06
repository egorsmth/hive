from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.models import User
from django.test import TestCase, Client

from django.urls import reverse

from user_profile.models import Profile

HTTP_REDIRECT = 302
HTTP_OK = 200


class UserProfileTestCase(TestCase):
    def get_user_url(self, x):
        return reverse('profile', kwargs={'person_id': x})

    get_login_url = reverse('index')
    get_logout_url = reverse('logout')
    registration_url = reverse('registration')
    post_login_url = reverse('index')

    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        User.objects.create_user('tom', 'tom@jeff.com', 'jeffpass')
        self.c = Client()

    def test_login(self):
        response = self.c.get(self.get_user_url(0))
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        response = self.c.get(self.get_login_url)
        self.assertEqual(response.status_code, HTTP_OK)
        response = self.c.post(self.post_login_url, {
            'username': 'tom',
            'password': 'jeffpass',
        })
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        response = self.c.get(self.get_user_url(1))
        self.assertEqual(response.status_code, HTTP_OK)
        response = self.c.get(self.get_login_url)
        self.assertEqual(response.status_code, HTTP_REDIRECT)

    def test_logout(self):
        response = self.c.post(self.post_login_url, {
            'username': 'tom',
            'password': 'jeffpass',
        })
        response = self.c.get(self.get_login_url)
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        response = self.c.get(self.get_logout_url)
        response = self.c.get(self.get_login_url)
        self.assertEqual(response.status_code, HTTP_OK)
        response = self.c.get(self.get_user_url(0))
        self.assertEqual(response.status_code, HTTP_REDIRECT)

    def test_registration(self):
        new_username = 'new_user_symbols'
        new_user_email = 'new_user@email.com'
        new_user_password = 'pass_123_pass'

        response = self.c.get(self.get_user_url(0))
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        response = self.c.get(self.registration_url)
        self.assertEqual(response.status_code, HTTP_OK)
        response = self.c.post(self.registration_url, {
            'username': new_username,
            'email': new_user_email,
            'password1': new_user_password,
            'password2': new_user_password,
        })
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        response = self.c.get(self.get_user_url(7))
        #self.assertEqual(response.status_code, HTTP_OK)
        registered = User.objects.get(username=new_username)
        self.assertIsNotNone(registered)
        self.assertEqual(registered.email, new_user_email)
        hasher = identify_hasher(registered.password)
        is_correct = hasher.verify(new_user_password, registered.password)
        self.assertTrue(is_correct)
        profile = Profile.objects.get(user_id=registered.id)
        self.assertEqual(profile.avatar, 'system/default_avatar.png')

    def test_register_not_uniq_name(self):
        response = self.c.post(self.registration_url, {
            'username': 'john',
            'email': 'lennon@thebeatles.com',
            'password1': 'johnpassword',
            'password2': 'johnpassword',
        })
        users = User.objects.filter(username='john')
        self.assertEqual(len(users), 1)
